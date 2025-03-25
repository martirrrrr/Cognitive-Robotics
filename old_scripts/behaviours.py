import time
import random
import threading

class Behaviours:
    JOKES = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why don't eggs tell jokes? They might crack up.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What did the zero say to the eight? Nice belt!",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "What do you call cheese that isn't yours? Nacho cheese.",
        "How does a penguin build its house? Igloos it together!",
        "Why did the bicycle fall over? It was two-tired.",
        "What's orange and sounds like a parrot? A carrot!",
        "What did one wall say to the other wall? 'I'll meet you at the corner.'",
        "Why can't you give Elsa a balloon? Because she'll let it go.",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Why was the math book sad? It had too many problems.",
        "How does a snowman get around? By riding an 'icicle.'",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "Why don't some couples go to the gym? Because some relationships don't work out.",
        "What did one ocean say to the other ocean? Nothing, they just waved.",
        "What's a skeleton's least favorite room? The living room.",
        "Why don't tomatoes talk? Because they are always red from embarrassment!",
        "What's the worst thing for an electrician? Never sparking a conversation with anyone.",
        "What does a mathematician do in the jungle? Looks for the least common multiple!",
        "Why do geese always walk? Because they don't have the car keys!",
        "Do you know why the math book is sad? Because it has too many problems!"
    ]

    SOUND_FILES = {
        "bells": "/home/nao/CR/bells.mp3",
        "birds": "/home/nao/CR/birds.mp3",
        "seashore": "/home/nao/CR/seashore.mp3",
        "quick_meditation": "/home/nao/CR/quick_meditation.mp3",
        "full_meditation": "/home/nao/CR/full_meditation.mp3",
        "house": "/home/nao/CR/techno.mp3",
        "classical": "/home/nao/CR/classic.mp3",
        "rock": "/home/nao/CR/rock2.mp3",
        "comedy": "/home/nao/CR/comedy.mp3"
    }

    def __init__(self, text_to_speech, poses_module):
        self.text_to_speech = text_to_speech
        self.poses_module = poses_module

    def perform_neutral(self, play_sound_callback, recognize_speech_callback):
        try:
            print("[INFO] Pepper is listening...\n")
            self.text_to_speech.say("What would you like to do?")
            print("[PEPPER] What would you like to do?\n")
            self.text_to_speech.say("Please, choose music, relax or joke .")
            print("[PEPPER] Please, choose music, joke or relax.\n")
            
            while True:
                recognized_word = recognize_speech_callback()

                choices = {"relax": 0, "music": 1, "joke": 2}
                result = choices.get(recognized_word, None)

                if result is not None:
                    if result == 0:
                        self.perform_angry(play_sound_callback, recognize_speech_callback)
                        break
                        
                    elif result == 1:
                        self.perform_happy(play_sound_callback, recognize_speech_callback)
                        break
                        
                    elif result == 2:
                        self.perform_sad(play_sound_callback, recognize_speech_callback)
                        break
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")
                    print("Answer not allowed, retry!\n")

        except Exception as e:
            print("Error: ", str(e))
            return None 

    def perform_happy(self, play_sound_callback, recognize_speech_callback):
        try:
            flag_second_choice = False
            
            self.text_to_speech.say("Hello! Would you like to listen to a song?")
            print("[PEPPER] Hello! Would you like to listen to a song?\n")
            
            while True:
                if not flag_second_choice:
                    user_selection = recognize_speech_callback()
                    time.sleep(1.0)

                if user_selection == "yes":
                    self.text_to_speech.say("Great choice!")
                    print("[PEPPER] Great choice!\n")
                    time.sleep(1.0)
                    if not flag_second_choice:
                        self.poses_module.perform_stretching()
                    
                    while True:
                        self.text_to_speech.say("Tell me what kind of music you prefer: house, classical, or rock.")
                        print("[PEPPER] Tell me what kind of music you prefer: house, classical, or rock.\n")
                        user_choice = recognize_speech_callback()
                        time.sleep(1.0)

                        dance_functions = {
                            "house": self.poses_module.perform_techno_dance,
                            "classical": self.poses_module.perform_classic_dance,
                            "rock": self.poses_module.perform_rock_dance
                        }

                        dance_function = dance_functions.get(user_choice, None)

                        if Behaviours.SOUND_FILES and dance_function:
                            music_thread = threading.Thread(target=play_sound_callback, args=(user_choice,))
                            dance_thread = threading.Thread(target=dance_function)

                            music_thread.start()                        
                            dance_thread.start()

                            music_thread.join()
                            dance_thread.join()

                            self.text_to_speech.say("I hope you liked the song!")
                            print("[PEPPER] I hope you liked the song!\n")
                            time.sleep(1.0)
                            break
                            
                        else:
                            self.text_to_speech.say("Sorry, I could not recognize the requested music genre, retry.")
                            print("[PEPPER] Sorry, I could not recognize the requested music genre, retry.\n")

                    self.text_to_speech.say("Would you like to listen to another song? Please answer yes or no.")
                    print("[PEPPER] Would you like to listen to another song? Please answer yes or no.\n")
                
                    while True:      
                        repeat_choice = recognize_speech_callback()

                        if repeat_choice == "no":
                            self.text_to_speech.say("Alright, goodbye!")
                            print("[PEPPER] Alright, goodbye!\n")
                            time.sleep(1.0)
                            return
                        
                        elif repeat_choice == "yes":
                            flag_second_choice = True
                            break
                            
                        else:
                            self.text_to_speech.say("Answer not allowed, retry!")
                            print("Answer not allowed, retry!\n")
                            
                elif user_selection == "no":
                    self.text_to_speech.say("See you soon!")
                    print("[PEPPER] See you soon\n")
                    time.sleep(1.0)
                    break
                
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")
                    print("Answer not allowed, retry!\n")

        except Exception as e:
            print("[ERROR] An error occurred:", e)

    def perform_angry(self, play_sound_callback, recognize_speech_callback):
        try:
            while True:
                self.perform_intro(play_sound_callback, recognize_speech_callback)
                if not self.get_user_feedback(recognize_speech_callback):
                    break
            
        except Exception as e:
            print("[ERROR] Some problems happened:", e)

    def get_user_feedback(self, recognize_speech_callback):
        self.text_to_speech.say("How are you? Do you want to continue?")
        print("[PEPPER] How are you? Do you want to continue?\n")
        time.sleep(1.0)
    
        self.text_to_speech.say("Answer with yes or no.")
        print("[PEPPER] Answer with yes or no.\n")

        while True:
            choice = recognize_speech_callback()
    
            if choice == "yes":
                self.text_to_speech.say("Great, let's continue!")
                print("[PEPPER] Great, let's continue!\n")
                time.sleep(2.0)
                return True
            
            elif choice == "no":
                self.text_to_speech.say("Okay! Goodbye!")
                print("[PEPPER] Okay! Goodbye!\n")
                self.poses_module.bye()
                return False

            else:
                self.text_to_speech.say("Answer not allowed, retry!")
                print("Answer not allowed, retry!\n")

    def breathing_guide(self):
        self.text_to_speech.say("Now, continue to breathe slowly.")
        print("[PEPPER] Now, continue to breathe slowly.\n")
        time.sleep(1.0)

        self.text_to_speech.say("Inhale counting to 4...")
        print("[PEPPER] Inhale counting to 4...\n")
        time.sleep(4.0)
        
        self.text_to_speech.say("Hold for 2...")
        print("[PEPPER] Hold for 2...\n")
        time.sleep(2.0)
        
        self.text_to_speech.say("Now exhale counting to 6.")
        print("[PEPPER] Now exhale counting to 6.\n")
        time.sleep(6.0)
        
        return

    def full_immersion(self, play_sound_callback, recognize_speech_callback):
        self.text_to_speech.say("Relax every part of your body, starting from the head.")
        print("[PEPPER] Relax every part of your body, starting from the head.\n")
        time.sleep(5.0)
        
        self.text_to_speech.say("Relax your forehead, eyes, cheeks...")
        print("[PEPPER] Relax your forehead, eyes, cheeks...\n")    
        time.sleep(5.0)

        self.text_to_speech.say("Slowly move down to the shoulders, chest, and arms...")
        print("[PEPPER] Slowly move down to the shoulders, chest, and arms...\n")
        time.sleep(5.0)

        play_sound_callback("bells")
        time.sleep(5.0)
        
        self.text_to_speech.say("Imagine yourself in a peaceful place, like a beach at sunset or a green forest.")
        print("[PEPPER] Imagine yourself in a peaceful place, like a beach at sunset or a green forest.\n")
        time.sleep(5.0)
        
        self.text_to_speech.say("Focus on the sound of the waves or the birds singing. Which do you prefer, forest or sea?")
        print("[PEPPER] Focus on the sound of the waves or the birds singing. Which do you prefer, forest or sea?\n")
        time.sleep(5.0)    
        
        while True:
            selection = recognize_speech_callback()

            if selection == "forest":
                play_sound_callback("birds")
                break

            elif selection == "sea":
                play_sound_callback("seashore")
                break
                
            else:
                self.text_to_speech.say("Answer not allowed, retry!")
                print("Answer not allowed, retry!\n")
        
        play_sound_callback("bells")
        time.sleep(2.0)

        self.text_to_speech.say("When you're ready, slowly move your fingers, then open your eyes.")
        print("[PEPPER] When you're ready, slowly move your fingers, then open your eyes.\n")
        time.sleep(5.0)

        return

    def quick_meditation(self, play_sound_callback):
        self.text_to_speech.say("Let's take a moment to relax.")
        print("[PEPPER] Let's take a moment to relax.\n")
        time.sleep(2.0)

        self.text_to_speech.say("Find a comfortable position, sitting or standing.")
        print("[PEPPE] Find a comfortable position, sitting or standing.\n")
        time.sleep(2.0)
        self.poses_module.perform_meditation_pose()

        self.text_to_speech.say("Close your eyes if you like, or focus on a calm point in front of you.")
        print("[PEPPER] Close your eyes if you like, or focus on a calm point in front of you.\n")
        time.sleep(2.0)
        self.poses_module.perform_meditation_pose()

        self.breathing_guide()
        self.text_to_speech.say("Now try it on your own!")
        print("[PEPPER] Now try it on your own!\n")
        time.sleep(5.0)

        play_sound_callback("bells")
        play_sound_callback("quick_meditation")

        self.text_to_speech.say("When you're ready, slowly open your eyes.")
        print("[PEPPER] When you're ready, slowly open your eyes.\n")
        time.sleep(5.0)

        play_sound_callback("bells")  
        self.text_to_speech.say("Thank you for taking this moment for yourself.")
        print("[PEPPER] Thank you for taking this moment for yourself.\n")
        
        return
           
    def full_meditation(self, play_sound_callback, recognize_speech_callback):
        self.quick_meditation(play_sound_callback)

        self.text_to_speech.say("Let's continue!")
        print("[PEPPER] Let's continue!\n")
        time.sleep(1.0)

        self.full_immersion(play_sound_callback, recognize_speech_callback)
        time.sleep(1.0)

        self.text_to_speech.say("Great job! I hope it was a positive experience.")
        print("[PEPPER] Great job! I hope it was a positive experience.\n")
        time.sleep(1.0)

        return

    def perform_intro(self, play_sound_callback, recognize_speech_callback):
        self.text_to_speech.say("Hello! Welcome to this guided meditation session.")
        print("[PEPPER] Hello! Welcome to this guided meditation session.\n")
        time.sleep(1.0)
        
        self.text_to_speech.say("If you feel agitated or angry, this might help you.")
        print("[PEPPER] If you feel agitated or angry, this might help you.\n")
        time.sleep(1.0)
        
        self.text_to_speech.say("Tell me, do you prefer a short or long session?")
        print("[PEPPER] Tell me, do you prefer a short or long session?\n")
        
        while True:
            user_selection = recognize_speech_callback()

            if user_selection == "short":
                self.quick_meditation(play_sound_callback)
                break
            
            elif user_selection == "long":
                self.full_meditation(play_sound_callback, recognize_speech_callback)
                break
            
            else:
                self.text_to_speech.say("Answer not allowed, retry!")
                print("Answer not allowed, retry!\n")
                time.sleep(2.0)

    def perform_sad(self, play_sound_callback, recognize_speech_callback):
        try:
            self.text_to_speech.say("If you're feeling sad, a joke might lift your spirits!")
            print("[PEPPER] If you're feeling sad, a joke might lift your spirits!\n")
            time.sleep(2.0)

            joke_index = 0 # random.randint(0, len(Behaviours.JOKES) - 1)

            self.text_to_speech.say(Behaviours.JOKES[joke_index])
            print("[PEPPER] " + Behaviours.JOKES[joke_index] + ".\n") 
            play_sound_callback("comedy")
            joke_index += 1
            
            while True:
                self.text_to_speech.say("Do you want to hear another one? Reply yes or no.")
                print("[PEPPER] Do you want to hear another one? Reply yes or no.\n")
                print("[INFO] Waiting for a response from the user...\n")

                recognized_word = recognize_speech_callback()

                if recognized_word == "yes":
                    self.text_to_speech.say(Behaviours.JOKES[joke_index])
                    print("[PEPPER] " + Behaviours.JOKES[joke_index] + ".\n") 
                    play_sound_callback("comedy")
                    joke_index += 1
                    time.sleep(2.0)

                elif recognized_word == "no":
                    self.text_to_speech.say("Alright, I hope you had fun! See you next time!")
                    print("[PEPPER] Alright, I hope you had fun! See you next time!\n")
                    time.sleep(2.0)
                    break
                    
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")
                    print("[PEPPER] Answer not allowed, retry!\n")     
        except Exception as e:
            print("[ERROR] A problem occurred:", e)


