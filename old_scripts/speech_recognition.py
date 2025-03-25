import qi
import sys
import time
import utils


class PepperSpeechRecognition:
    def __init__(self, session):
        try:
            self.asr_service = session.service("ALSpeechRecognition")
            self.memory_service = session.service("ALMemory")
            self.asr_service.pause(True)
            self.asr_service.setLanguage("English")
            self.asr_service.setVocabulary(utils.vocabulary, False)
            self.asr_service.pause(False)
            self.subscriber = self.memory_service.subscriber("WordRecognized")
            self.signal_id = self.subscriber.signal.connect(self.on_word_recognized)
            print("[INFO] Speech recognition initialized.\n")

        except Exception as e:
            print("[ERROR] Error happened during initialization: ", str(e))


    def start_listening(self):
        try:
            print("[INFO] Pepper is listening...")
            self.asr_service.subscribe("SingleRecognition")

        except Exception as e:
            print("[ERROR] Error happened during listening: ", str(e))

 
    def stop_listening(self):
        try:
            self.asr_service.unsubscribe("SingleRecognition")
            print("[INFO] Speech recognition stopped.\n")

        except Exception as e:
            print("[ERROR] Error happened during speech recognition stopping: ", str(e))

    
    def on_word_recognized(self, value):
        if value and len(value) > 0:
            word = value[0]
            confidence = value[1]
            print("[INFO] Recognized word: " + word + ".\n")
            print("[INFO] Confidence: " + str(confidence) + ".\n")

            if confidence > 0.4:
                print("[INFO] Stopping speech recognition after detected: " + word + ".\n")


    def clean_up(self):
        try:
            self.subscriber.signal.disconnect(self.signal_id)
            self.stop_listening()
            print("[INFO]Clean up completed.\n")

        except Exception as e:
            print("[ERROR] Error happened during clean up: " + str(e))


if __name__ == "__main__":
    try:
        session = qi.Session()
        session.connect("tcp://192.168.1.104:9559")
        speech_recognizer = PepperSpeechRecognition(session)

        while True:
            speech_recognizer.start_listening()
            time.sleep(1)

    except KeyboardInterrupt:
        speech_recognizer.clean_up()

    except RuntimeError:
        print("ERROR")
