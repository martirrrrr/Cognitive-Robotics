import time
import threading
import utils
import poses_old


def main():
    try:
        flag_second_choice = False
        
        utils.text_to_speech.say("Hello! Would you like to listen to a song?")
        print("[PEPPER] Hello! Would you like to listen to a song?\n")
        
        while True:
            if not flag_second_choice:
                time.sleep(2.0)
                user_selection = utils.recognize_speech()
                time.sleep(2.0)
            
            if user_selection == "yes":
                utils.text_to_speech.say("Great choice!")
                print("[PEPPER] Great choice!\n")
                time.sleep(2.0)
                if not flag_second_choice:
                    poses_old.perform_stretching()
                
                while True:
                    utils.text_to_speech.say("Tell me what kind of music you prefer: techno, classical, or rock.")
                    print("[PEPPER] Tell me what kind of music you prefer: techno, classical, or rock.\n")
                    time.sleep(2.0)
                    
                    user_choice = utils.recognize_speech()
                    time.sleep(2.0)

                    dance_functions = {
                        "techno": poses_old.perform_techno_dance,
                        "classical": poses_old.perform_classic_dance,
                        "rock": poses_old.perform_rock_dance
                    }

                    dance_function = dance_functions.get(user_choice, None)

                    if utils.sound_files and dance_function:
                        music_thread = threading.Thread(target=utils.play_sound, args=(user_choice,))
                        dance_thread = threading.Thread(target=dance_function)

                        music_thread.start()                        
                        dance_thread.start()

                        music_thread.join()
                        dance_thread.join()

                        utils.text_to_speech.say("I hope you liked the song!")
                        print("[PEPPER] I hope you liked the song!\n")
                        time.sleep(2.0)
                        break
                        
                    else:
                        utils.text_to_speech.say("Sorry, I could not recognize the requested music genre, retry.")
                        print("[PEPPER] Sorry, I could not recognize the requested music genre, retry.\n")
                        time.sleep(2.0)

                utils.text_to_speech.say("Would you like to listen to another song? Please answer yes or no.")
                print("[PEPPER] Would you like to listen to another song? Please answer yes or no.\n")
                time.sleep(2.0)
              
                while True:      
                    repeat_choice = utils.recognize_speech()
                    time.sleep(2.0)

                    if repeat_choice == "no":
                        utils.text_to_speech.say("Alright, goodbye!")
                        print("[PEPPER] Alright, goodbye!\n")
                        time.sleep(2.0)
                        return
                     
                    elif repeat_choice == "yes":
                        flag_second_choice = True
                        break
                        
                    else:
                        utils.text_to_speech.say("Answer not allowed, retry!")
                        print("Answer not allowed, retry!\n")
                        time.sleep(2.0)
                        
            elif user_selection == "no":
                utils.text_to_speech.say("See you soon!")
                print("[PEPPER] See you soon\n")
                time.sleep(2.0)
                break
               
            else:
                utils.text_to_speech.say("Answer not allowed, retry!")
                print("Answer not allowed, retry!\n")
                time.sleep(2.0)

    except Exception as e:
        print("[ERROR] An error occurred:", e)

