import utils
import time
import random


def main():
    try:
        utils.text_to_speech.say("If you're feeling sad, a joke might lift your spirits!")
        print("[PEPPER] If you're feeling sad, a joke might lift your spirits!\n")
        time.sleep(2.0)

        joke_index = random.randint(0, len(utils.jokes) - 1)

        utils.text_to_speech.say(utils.jokes[joke_index])
        print("[PEPPER] " + utils.jokes[joke_index] + ".\n") 
        utils.play_sound("comedy")

        while True:
            utils.text_to_speech.say("Do you want to hear another one? Reply yes or no.")
            print("[PEPPER] Do you want to hear another one? Reply yes or no.\n")
            time.sleep(2.0)
            print("[INFO] Waiting for a response from the user...\n")

            recognized_word = utils.recognize_speech()

            if recognized_word == "yes":
                utils.text_to_speech.say(utils.jokes[joke_index])
                print("[PEPPER] " + utils.jokes[joke_index] + ".\n") 
                utils.play_sound("comedy")
                time.sleep(2.0)

            elif recognized_word == "no":
                utils.text_to_speech.say("Alright, I hope you had fun! See you next time!")
                print("[PEPPER] Alright, I hope you had fun! See you next time!\n")
                time.sleep(2.0)
                break
                
            else:
                utils.text_to_speech.say("Answer not allowed, retry!")
                print("[PEPPER] Answer not allowed, retry!\n")
                time.sleep(2.0)     

    except Exception as e:
        print("[ERROR] A problem occurred:", e)
