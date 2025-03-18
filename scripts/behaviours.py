import threading

class Behaviours:
    # List of jokes that the robot can tell
    JOKES = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why don't eggs tell jokes? They might crack up.",
        # More jokes...
    ]

    # Dictionary of available sound files categorized by type
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
        # Initialize the robot's text-to-speech and pose control modules
        self.text_to_speech = text_to_speech
        self.poses_module = poses_module

    def perform_neutral(self, play_sound_callback, recognize_speech_callback):
        """Guides the user through selecting an activity: music, relaxation, or jokes."""
        try:
            print("[INFO] Pepper is listening...\n")
            self.text_to_speech.say("What would you like to do?")
            self.text_to_speech.say("Please, choose music, relax or joke.")
            
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
        except Exception as e:
            print("Error:", str(e))

    def perform_happy(self, play_sound_callback, recognize_speech_callback):
        """Handles the happy behavior by playing music and dancing."""
        try:
            self.text_to_speech.say("Hello! Would you like to listen to a song?")
            while True:
                user_selection = recognize_speech_callback()
                if user_selection == "yes":
                    self.text_to_speech.say("Great choice!")
                    self.poses_module.perform_stretching()
                    
                    # Ask for the preferred music genre
                    while True:
                        self.text_to_speech.say("Tell me what kind of music you prefer: house, classical, or rock.")
                        user_choice = recognize_speech_callback()
                        
                        dance_functions = {
                            "house": self.poses_module.perform_techno_dance,
                            "classical": self.poses_module.perform_classic_dance,
                            "rock": self.poses_module.perform_rock_dance
                        }
                        
                        dance_function = dance_functions.get(user_choice, None)
                        if dance_function:
                            music_thread = threading.Thread(target=play_sound_callback, args=(user_choice,))
                            dance_thread = threading.Thread(target=dance_function)
                            
                            music_thread.start()
                            dance_thread.start()
                            
                            music_thread.join()
                            dance_thread.join()
                            
                            self.text_to_speech.say("I hope you liked the song!")
                            break
                        else:
                            self.text_to_speech.say("Sorry, I could not recognize the requested music genre, retry.")
                elif user_selection == "no":
                    self.text_to_speech.say("See you soon!")
                    break
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")
        except Exception as e:
            print("[ERROR] An error occurred:", e)

    def perform_sad(self, play_sound_callback, recognize_speech_callback):
        """Tells jokes to cheer up the user."""
        try:
            self.text_to_speech.say("If you're feeling sad, a joke might lift your spirits!")
            joke_index = 0 
            
            while True:
                self.text_to_speech.say(Behaviours.JOKES[joke_index])
                play_sound_callback("comedy")
                joke_index = (joke_index + 1) % len(Behaviours.JOKES)
                
                self.text_to_speech.say("Do you want to hear another one? Reply yes or no.")
                recognized_word = recognize_speech_callback()

                if recognized_word == "no":
                    self.text_to_speech.say("Alright, I hope you had fun! See you next time!")
                    break
                elif recognized_word != "yes":
                    self.text_to_speech.say("Answer not allowed, retry!")
        except Exception as e:
            print("[ERROR] A problem occurred:", e)
