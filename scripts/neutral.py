import happy, sad, angry
import utils
import time


def main():
    try:
        print("[INFO] Pepper is listening...\n")
        utils.text_to_speech.say("What would you like to do?")
        print("[PEPPER] What would you like to do?\n")
        time.sleep(2.0)
        utils.text_to_speech.say("Please, choose music, relax or joke .")
        print("[PEPPER] Please, choose music, joke or relax.\n")
        
        while True:
            time.sleep(4.0)
            recognized_word = utils.recognize_speech()

            choices = {"relax": 0, "music": 1, "joke": 2}
            result = choices.get(recognized_word, None)

            if result is not None:
                if result == 0:
                    angry.main()
                    break
                    
                elif result == 1:
                    happy.main()
                    break
                    
                elif result == 2:
                    sad.main()
                    break
            else:
                utils.text_to_speech.say("Answer not allowed, retry!")
                print("Answer not allowed, retry!\n")
                time.sleep(2.0)

    except Exception as e:
        print("Error: " + str(e))
        return None 
