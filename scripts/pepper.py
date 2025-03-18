import time
import qi
import poses
import behaviours

class Pepper:
    # Define Pepper's IP address and port for connection
    IP = "192.168.1.104"
    PORT = 9559
    
    # Define a vocabulary for speech recognition
    VOCABULARY = [
        "yes",
        "no",
        "forest", 
        "sea",
        "short",
        "long",
        "rock", 
        "house", 
        "classical",
        "relax", 
        "music", 
        "joke"
    ]

    def __init__(self):
        """
        Initializes the Pepper robot by connecting to it and setting up various services.
        """
        self.session = self.connect_to_pepper()  # Establish connection to Pepper
        self.text_to_speech = self.session.service("ALTextToSpeech")  # Text-to-Speech service
        self.motion = self.session.service("ALMotion")  # Motion control service
        self.audio_player = self.session.service("ALAudioPlayer")  # Audio playback service
        self.speech_recognition = self.session.service("ALSpeechRecognition")  # Speech recognition service
        self.memory = self.session.service("ALMemory")  # Memory service for event handling
        self.robot_posture = self.session.service("ALRobotPosture")  # Controls robot posture
        self.video_recorder = self.session.service("ALVideoRecorder")  # Video recording service
        self.audio_recorder = self.session.service("ALAudioRecorder")  # Audio recording service
        self.robot_posture = self.session.service("ALRobotPosture")  # Posture service (duplicate reference)

        self.set_speech_service()  # Configure speech recognition settings

        # Load the Poses and Behaviours modules
        self.poses_module = poses.Poses(self.motion, self.robot_posture, self.text_to_speech)
        self.behaviours_module = behaviours.Behaviours(self.text_to_speech, self.poses_module)

    def connect_to_pepper(self):
        """
        Establishes a connection to the Pepper robot using the IP and port.
        """
        session = qi.Session()
        try:
            session.connect("tcp://" + Pepper.IP + ":" + str(Pepper.PORT))
            print("[INFO] Robot connection established.\n")
            return session
        
        except RuntimeError as e:
            print("[ERROR] Unable to connect to Pepper. Check the IP address or network connection.\n")
            raise e
        
    def recognize_speech(self):
        """
        Uses Pepper's speech recognition to detect and return a spoken word from the predefined vocabulary.
        """
        recognized_word = None

        try:
            while recognized_word is None:
                # Retrieve recognized words from memory
                event_data = self.memory.getData("WordRecognized")
                if event_data and isinstance(event_data, list) and len(event_data) > 1:
                    word, confidence = event_data[0], event_data[1]
                    if confidence >= 0.4:  # Only accept words with confidence >= 40%
                        recognized_word = word
                        print("[INFO] Detected word: " + str(recognized_word) + ".\n")
                        self.text_to_speech.say("You have said: " + str(recognized_word))
                        print("[PEPPER] You have said: " + str(recognized_word) + ".\n")
                        self.memory.removeData("WordRecognized")  # Clear memory entry to prepare for next input
                time.sleep(0.1)  # Prevent excessive polling
            
        except Exception as e:
            print("[ERROR] An error occurred during speech recognition: ", e)
    
        return recognized_word

    def set_speech_service(self):
        """
        Configures Pepper's speech recognition service with the predefined vocabulary.
        """
        self.speech_recognition.pause(True)  # Pause recognition while setting it up
        self.speech_recognition.setLanguage("English")  # Set speech recognition language
        self.text_to_speech.setLanguage("English")  # Set text-to-speech language
        self.speech_recognition.setVocabulary(Pepper.VOCABULARY, False)  # Set vocabulary without word spotting
        self.speech_recognition.subscribe("Recognizer")  # Activate speech recognition
        self.speech_recognition.pause(False)  # Resume recognition

    def play_sound(self, sound_file):
        """
        Plays a sound file using Pepper's audio system.
        """
        self.audio_player.playFile(self.behaviours_module.SOUND_FILES.get(sound_file, None))

    def start_video_recording(self, filename):
        """
        Starts recording a video with predefined settings.
        """
        try:
            self.video_recorder.setCameraID(0)  # Use front camera
            self.video_recorder.setResolution(2)  # Set video resolution
            self.video_recorder.setFrameRate(10)  # Set frame rate
            self.video_recorder.setVideoFormat("MJPG")  # Set video format

            print("[PEPPER] Video recording started...\n")
            
            self.video_recorder.startRecording("/home/nao/transfer", filename)  # Start recording
        except Exception as e:
            print("[ERROR] An issue occurred during video setup:", e)

    def start_audio_recording(self, filename):
        """
        Starts recording audio using Pepper's microphone.
        """
        audio_channels = [0, 0, 1, 0]  # Enable only one microphone for recording
        print("[PEPPER] Audio recording started...\n")
        self.audio_recorder.startMicrophonesRecording(
            "/home/nao/transfer/" + filename + ".wav", 
            "wav", 
            16000, 
            audio_channels
        )

    def stop_video_recording(self):
        """
        Stops the ongoing video recording.
        """
        try:
            video_info = self.video_recorder.stopRecording()
        except Exception as e:
            print("[ERROR] An issue occurred while stopping video recording:", e)

    def stop_audio_recording(self):
        """
        Stops the ongoing audio recording.
        """
        self.audio_recorder.stopMicrophonesRecording()

    def stop_recording(self):
        """
        Stops both audio and video recording.
        """
        self.stop_video_recording()
        self.stop_audio_recording()   
        print("[INFO] Audio and video recording successfully completed!\n")

    def record_audio_video(self, video_filename, audio_filename):
        """
        Stops any ongoing recording and starts a new audio and video recording session.
        """
        try:
            self.stop_video_recording()
            self.stop_audio_recording()
            
            self.start_video_recording(video_filename)
            self.start_audio_recording(audio_filename)
           
        except Exception as e:
            print("[ERROR] An issue occurred:", e)     

    def perform_behaviours(self, behaviour):
        """
        Performs a predefined behavior based on the detected emotion.
        0 - Neutral
        1 - Happy
        2 - Angry
        3 - Sad
        """
        if behaviour == 0:
            self.behaviours_module.perform_neutral(self.play_sound, self.recognize_speech)
        elif behaviour == 1:
            self.behaviours_module.perform_happy(self.play_sound, self.recognize_speech)
        elif behaviour == 2:
            self.behaviours_module.perform_angry(self.play_sound, self.recognize_speech)
        else:
            self.behaviours_module.perform_sad(self.play_sound, self.recognize_speech)
