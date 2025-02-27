import time
import qi
import poses
import behaviours

class Pepper:
    IP = "192.168.1.104"
    
    PORT = 9559
    
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
        self.session = self.connect_to_pepper()
        self.text_to_speech = self.session.service("ALTextToSpeech")
        self.motion = self.session.service("ALMotion")
        self.audio_player = self.session.service("ALAudioPlayer")
        self.speech_recognition = self.session.service("ALSpeechRecognition")
        self.memory = self.session.service("ALMemory")
        self.robot_posture = self.session.service("ALRobotPosture")
        self.video_recorder = self.session.service("ALVideoRecorder")
        self.audio_recorder = self.session.service("ALAudioRecorder")
        self.robot_posture = self.session.service("ALRobotPosture")
        self.set_speech_service()
        self.poses_module = poses.Poses(self.motion, self.robot_posture, self.text_to_speech)
        self.behaviours_module = behaviours.Behaviours(self.text_to_speech, self.poses_module)

    def connect_to_pepper(self):
        session = qi.Session()
        try:
            session.connect("tcp://" + Pepper.IP + ":" + str(Pepper.PORT))
            print("[INFO] Robot connection established.\n")
            return session
        
        except RuntimeError as e:
            print("[ERROR] It's impossible to connect to Pepper. Check IP address or connetction to network\n.")
            raise e
        
    def recognize_speech(self):
        recognized_word = None

        try:
            # self.text_to_speech.say("Waiting for user's input")
            # print("[PEPPER] Waiting for user's input.\n")

            while recognized_word is None:
                event_data = self.memory.getData("WordRecognized")
                if event_data and isinstance(event_data, list) and len(event_data) > 1:
                    word, confidence = event_data[0], event_data[1]
                    if confidence >= 0.5:
                        recognized_word = word
                        print("[INFO] Detected word: " + str(recognized_word) + ".\n")
                        self.text_to_speech.say("You have said: " + str(recognized_word))
                        print("[PEPPER] You have said: " + str(recognized_word) + ".\n")
                        self.memory.removeData("WordRecognized")
                time.sleep(0.1)
            
        except Exception as e:
            print("[ERROR] Some problems happened during speech recognition: ", e)
    
        return recognized_word

    def set_speech_service(self):
        self.speech_recognition.pause(True)
        self.speech_recognition.setLanguage("English")
        self.text_to_speech.setLanguage("English")
        self.speech_recognition.setVocabulary(Pepper.VOCABULARY, False)
        self.speech_recognition.subscribe("Recognizer")
        self.speech_recognition.pause(False)

    def play_sound(self, sound_file):
        self.audio_player.playFile(self.behaviours_module.SOUND_FILES.get(sound_file, None))

    def start_video_recording(self, filename):
        try:
            self.video_recorder.setCameraID(0)
            self.video_recorder.setResolution(2)
            self.video_recorder.setFrameRate(10)
            self.video_recorder.setVideoFormat("MJPG") 

            # utils.text_to_speech.say("Video recording started...")
            print("[PEPPER] Video recording started...\n")
            
            self.video_recorder.startRecording("/home/nao/transfer", filename)
        except Exception as e:
            print("[ERROR] An issue occurred during video setup:", e)


    def start_audio_recording(self, filename):
        audio_channels = [0, 0, 1, 0]
        # utils.text_to_speech.say("Audio recording started...")
        print("[PEPPER] Audio recording started...\n")
        self.audio_recorder.startMicrophonesRecording("/home/nao/transfer/" + filename + ".wav", "wav", 16000, audio_channels)


    def stop_video_recording(self):
        try:
            video_info = self.video_recorder.stopRecording()
            # utils.text_to_speech.say("Video recording completed!\n")
            # print("[PEPPER] Video recording completed!\n")
            # print("[INFO] Video saved in: " + str(video_info[1]) + ".\n")
            # print("[INFO] Number of frames recorded: " + str(video_info[0]) + ".\n")
            
        except Exception as e:
            print("[ERROR] An issue occurred while stopping video recording:", e)

    def stop_audio_recording(self):
        self.audio_recorder.stopMicrophonesRecording()
        # utils.text_to_speech.say("Audio recording completed!\n")
        # print("[PEPPER] Audio recording completed!\n")
        # print("[INFO] Audio saved in: " + str(audio_info[1]) + ".\n")
        # print("[INFO] Number of frames recorded: " + str(audio_info[0]) + ".\n")

    def record_audio_video(self, video_filename, audio_filename):
        try:
            self.stop_video_recording()
            self.stop_audio_recording()
            
            self.start_video_recording(video_filename)
            self.start_audio_recording(audio_filename)
        
            time.sleep(4)
            
            self.stop_video_recording()
            self.stop_audio_recording()
            
            print("[INFO] Audio and video recording successfully completed!\n")
        
        except Exception as e:
            print("[ERROR] An issue occurred:", e)     

    def perform_behaviours(self, behaviour):
        if behaviour == 0:
            self.behaviours_module.perform_neutral(self.play_sound, self.recognize_speech)
        elif behaviour == 1:
            self.behaviours_module.perform_happy(self.play_sound, self.recognize_speech)
        elif behaviour == 2:
            self.behaviours_module.perform_angry(self.play_sound, self.recognize_speech)
        else:
            self.behaviours_module.perform_sad(self.play_sound, self.recognize_speech)

    
