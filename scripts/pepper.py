import time
import qi
import poses
import behaviours

class Pepper:
    """
    Main class for controlling Pepper robot's functionalities including:
    - Speech recognition and synthesis
    - Audio/video recording
    - Movement and behavior control
    - Interaction with various NAOqi services
    """
    
    # Static configuration parameters
    IP = "192.168.0.67"  # Default IP address for Pepper
    PORT = 9559  # Default port for NAOqi services
    
    # Vocabulary for speech recognition (limited set for better accuracy)
    VOCABULARY = [
        "yes", "no", 
        "forest", "sea",
        "short", "long",
        "rock", "house", "classical",
        "relax", "music", "joke"
    ]

    def __init__(self):
        """
        Initializes connection to Pepper and sets up all required services.
        Services initialized:
        - ALTextToSpeech: For speech output
        - ALMotion: For movement control
        - ALAudioPlayer: For playing sounds
        - ALSpeechRecognition: For voice commands
        - ALMemory: For event handling
        - ALRobotPosture: For posture control
        - ALVideoRecorder/ALAudioRecorder: For media recording
        """
        try:
            # Establish connection to Pepper
            self.session = self.connect_to_pepper()
            
            # Initialize all NAOqi services
            self.text_to_speech = self.session.service("ALTextToSpeech")
            self.motion = self.session.service("ALMotion")
            self.audio_player = self.session.service("ALAudioPlayer")
            self.speech_recognition = self.session.service("ALSpeechRecognition")
            self.memory = self.session.service("ALMemory")
            self.robot_posture = self.session.service("ALRobotPosture")
            self.video_recorder = self.session.service("ALVideoRecorder")
            self.audio_recorder = self.session.service("ALAudioRecorder")

            # Configure speech recognition settings
            self.set_speech_service()

            # Initialize helper modules
            self.poses_module = poses.Poses(self.motion, self.robot_posture, self.text_to_speech)
            self.behaviours_module = behaviours.Behaviours(self.text_to_speech, self.poses_module)

        except Exception as e:
            print(f"[ERROR] Initialization failed: {str(e)}")
            raise

    def connect_to_pepper(self):
        """
        Establishes connection to Pepper robot via NAOqi middleware.
        
        Returns:
            qi.Session: Active session with Pepper
            
        Raises:
            RuntimeError: If connection fails
        """
        session = qi.Session()
        try:
            connection_url = f"tcp://{Pepper.IP}:{str(Pepper.PORT)}"
            session.connect(connection_url)
            print("[INFO] Successfully connected to Pepper.\n")
            return session
            
        except RuntimeError as e:
            print("[ERROR] Connection failed. Please check:")
            print("- Pepper is powered on")
            print("- Network connectivity")
            print("- IP address configuration")
            raise RuntimeError("Connection to Pepper failed") from e

    def recognize_speech(self):
        """
        Listens for and recognizes speech using Pepper's microphone.
        Uses predefined vocabulary for better accuracy.
        
        Returns:
            str: Recognized word or None if nothing recognized
            
        Note:
            Only returns words with confidence >= 40%
            Clears recognition memory after successful detection
        """
        recognized_word = None
        confidence_threshold = 0.4  # Minimum confidence level to accept recognition

        try:
            while not recognized_word:
                # Get recognition results from memory
                event_data = self.memory.getData("WordRecognized")
                
                # Check if valid recognition data exists
                if event_data and isinstance(event_data, list) and len(event_data) > 1:
                    word, confidence = event_data[0], event_data[1]
                    
                    if confidence >= confidence_threshold:
                        recognized_word = word.lower()
                        print(f"[INFO] Recognized: {recognized_word} (confidence: {confidence:.2f})\n")
                        
                        # Provide audible feedback
                        self.text_to_speech.say(f"You said: {recognized_word}")
                        
                        # Clear memory for next recognition
                        self.memory.removeData("WordRecognized")
                
                # Small delay to prevent CPU overload
                time.sleep(0.1)
                
        except Exception as e:
            print(f"[ERROR] Speech recognition failed: {str(e)}")
        
        return recognized_word

    def set_speech_service(self):
        """
        Configures speech recognition service with:
        - English language
        - Predefined vocabulary
        - Proper subscription
        """
        try:
            # Temporarily pause recognition during configuration
            self.speech_recognition.pause(True)
            
            # Set language for both recognition and synthesis
            self.speech_recognition.setLanguage("English")
            self.text_to_speech.setLanguage("English")
            
            # Configure vocabulary (without word spotting)
            self.speech_recognition.setVocabulary(Pepper.VOCABULARY, False)
            
            # Activate recognition service
            self.speech_recognition.subscribe("Recognizer")
            self.speech_recognition.pause(False)
            
        except Exception as e:
            print(f"[ERROR] Failed to configure speech service: {str(e)}")
            raise

    def play_sound(self, sound_type):
        """
        Plays a sound file from Pepper's predefined sound library.
        
        Args:
            sound_type (str): Key from behaviours.SOUND_FILES dictionary
            
        Returns:
            None: If sound file not found
        """
        sound_file = self.behaviours_module.SOUND_FILES.get(sound_type)
        if sound_file:
            try:
                self.audio_player.playFile(sound_file)
            except Exception as e:
                print(f"[ERROR] Failed to play sound: {str(e)}")
        else:
            print(f"[WARNING] Sound type '{sound_type}' not found")

    def start_video_recording(self, filename):
        """
        Starts video recording with Pepper's front camera.
        
        Configuration:
        - Camera ID 0 (front camera)
        - Resolution 2 (640x480)
        - 10 FPS frame rate
        - MJPG video format
        - Saves to /home/nao/transfer directory
        
        Args:
            filename (str): Name for output video file (without extension)
        """
        try:
            self.video_recorder.setCameraID(0)
            self.video_recorder.setResolution(2)
            self.video_recorder.setFrameRate(10)
            self.video_recorder.setVideoFormat("MJPG")
            
            full_path = f"/home/nao/transfer/{filename}.avi"
            self.video_recorder.startRecording("/home/nao/transfer", filename)
            print(f"[INFO] Started video recording: {full_path}")
            
        except Exception as e:
            print(f"[ERROR] Video recording failed: {str(e)}")

    def start_audio_recording(self, filename):
        """
        Starts audio recording using Pepper's microphones.
        
        Configuration:
        - WAV format
        - 16kHz sample rate
        - Single channel recording
        - Saves to /home/nao/transfer directory
        
        Args:
            filename (str): Name for output audio file (without extension)
        """
        try:
            # Channel configuration: [FrontLeft, FrontRight, RearLeft, RearRight]
            audio_channels = [0, 0, 1, 0]  # Only rear left microphone active
            
            full_path = f"/home/nao/transfer/{filename}.wav"
            self.audio_recorder.startMicrophonesRecording(
                full_path, 
                "wav", 
                16000, 
                audio_channels
            )
            print(f"[INFO] Started audio recording: {full_path}")
            
        except Exception as e:
            print(f"[ERROR] Audio recording failed: {str(e)}")

    def stop_video_recording(self):
        """Stops any ongoing video recording and returns recording info."""
        try:
            return self.video_recorder.stopRecording()
        except Exception as e:
            print(f"[ERROR] Failed to stop video recording: {str(e)}")
            return None

    def stop_audio_recording(self):
        """Stops any ongoing audio recording."""
        try:
            self.audio_recorder.stopMicrophonesRecording()
        except Exception as e:
            print(f"[ERROR] Failed to stop audio recording: {str(e)}")

    def stop_recording(self):
        """Convenience method to stop both audio and video recording."""
        self.stop_video_recording()
        self.stop_audio_recording()
        print("[INFO] Stopped all recordings")

    def record_audio_video(self, video_filename, audio_filename):
        """
        Starts synchronized audio and video recording.
        
        Args:
            video_filename (str): Name for video file
            audio_filename (str): Name for audio file
        """
        try:
            # Stop any existing recordings first
            self.stop_recording()
            
            # Start new recordings
            self.start_video_recording(video_filename)
            self.start_audio_recording(audio_filename)
            
        except Exception as e:
            print(f"[ERROR] Recording failed: {str(e)}")

    def perform_behaviours(self, emotion_code):
        """
        Executes appropriate behavior based on detected emotion.
        
        Args:
            emotion_code (int): 
                0 - Neutral behavior
                1 - Happy behavior (music/dance)
                2 - Angry behavior (relaxation)
                3 - Sad behavior (jokes)
        """
        try:
            if emotion_code == 0:
                self.behaviours_module.perform_neutral(self.play_sound, self.recognize_speech)
            elif emotion_code == 1:
                self.behaviours_module.perform_happy(self.play_sound, self.recognize_speech)
            elif emotion_code == 2:
                self.behaviours_module.perform_angry(self.play_sound, self.recognize_speech)
            elif emotion_code == 3:
                self.behaviours_module.perform_sad(self.play_sound, self.recognize_speech)
            else:
                print(f"[WARNING] Unknown emotion code: {emotion_code}")
                
        except Exception as e:
            print(f"[ERROR] Behavior execution failed: {str(e)}")