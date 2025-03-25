# Import required libraries
import time  # For timing and delays
import random  # For random selection functionality
import threading  # For parallel execution of tasks

class Behaviours:
    """
    A class that encapsulates various interactive behaviors for Pepper robot,
    including joke telling, music playback, and relaxation techniques.
    """
    
    # Class-level constant containing a comprehensive list of jokes
    JOKES = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        # ... (other jokes remain the same)
        "Do you know why the math book is sad? Because it has too many problems!"
    ]

    # Dictionary mapping sound categories to their file paths on Pepper
    SOUND_FILES = {
        "bells": "/home/nao/CR/bells.mp3",  # Bell sounds for meditation
        "birds": "/home/nao/CR/birds.mp3",  # Forest ambiance
        # ... (other sound files remain the same)
        "comedy": "/home/nao/CR/comedy.mp3"  # Laugh track for jokes
    }

    def __init__(self, text_to_speech, poses_module):
        """
        Initialize the Behaviours class with required modules.
        
        Args:
            text_to_speech: Module for converting text to speech
            poses_module: Module for controlling robot movements and poses
        """
        self.text_to_speech = text_to_speech
        self.poses_module = poses_module

    def perform_neutral(self, play_sound_callback, recognize_speech_callback):
        """
        Main interaction menu that lets users choose between activities.
        
        Args:
            play_sound_callback: Function to play audio files
            recognize_speech_callback: Function for speech recognition
            
        Flow:
            1. Presents options (music, relax, joke)
            2. Waits for user input
            3. Routes to appropriate behavior based on choice
        """
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
        """
        Music and dance interaction flow.
        
        Features:
            - Music genre selection
            - Synchronized dancing
            - Repeat functionality
        """
        try:
            flag_second_choice = False  # Flag for repeated interactions
            
            self.text_to_speech.say("Hello! Would you like to listen to a song?")
            
            while True:
                if not flag_second_choice:
                    user_selection = recognize_speech_callback()
                    time.sleep(1.0)

                if user_selection == "yes":
                    self.text_to_speech.say("Great choice!")
                    if not flag_second_choice:
                        self.poses_module.perform_stretching()
                    
                    while True:
                        self.text_to_speech.say("Tell me what kind of music you prefer: house, classical, or rock.")
                        user_choice = recognize_speech_callback()

                        # Map music genres to corresponding dance functions
                        dance_functions = {
                            "house": self.poses_module.perform_techno_dance,
                            "classical": self.poses_module.perform_classic_dance,
                            "rock": self.poses_module.perform_rock_dance
                        }

                        dance_function = dance_functions.get(user_choice, None)

                        if dance_function:
                            # Run music and dance in parallel threads
                            music_thread = threading.Thread(
                                target=play_sound_callback, 
                                args=(user_choice,)
                            )
                            dance_thread = threading.Thread(
                                target=dance_function
                            )

                            music_thread.start()                        
                            dance_thread.start()

                            music_thread.join()
                            dance_thread.join()

                            self.text_to_speech.say("I hope you liked the song!")
                            break
                        else:
                            self.text_to_speech.say("Sorry, I could not recognize the requested music genre, retry.")

                    # Offer to play another song
                    self.text_to_speech.say("Would you like to listen to another song?")
                
                    while True:      
                        repeat_choice = recognize_speech_callback()

                        if repeat_choice == "no":
                            self.text_to_speech.say("Alright, goodbye!")
                            return
                        elif repeat_choice == "yes":
                            flag_second_choice = True
                            break
                        else:
                            self.text_to_speech.say("Answer not allowed, retry!")
                            
                elif user_selection == "no":
                    self.text_to_speech.say("See you soon!")
                    break
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")

        except Exception as e:
            print("[ERROR] An error occurred:", e)

    def perform_angry(self, play_sound_callback, recognize_speech_callback):
        """
        Relaxation and meditation flow for stress/anger management.
        """
        try:
            while True:
                self.perform_intro(play_sound_callback, recognize_speech_callback)
                if not self.get_user_feedback(recognize_speech_callback):
                    break
        except Exception as e:
            print("[ERROR] Some problems happened:", e)

    def get_user_feedback(self, recognize_speech_callback):
        """
        Gets user feedback about continuing the session.
        
        Returns:
            bool: True if user wants to continue, False otherwise
        """
        self.text_to_speech.say("How are you? Do you want to continue?")
        self.text_to_speech.say("Answer with yes or no.")

        while True:
            choice = recognize_speech_callback()
    
            if choice == "yes":
                self.text_to_speech.say("Great, let's continue!")
                return True
            elif choice == "no":
                self.text_to_speech.say("Okay! Goodbye!")
                self.poses_module.bye()
                return False
            else:
                self.text_to_speech.say("Answer not allowed, retry!")

    def breathing_guide(self):
        """Guides user through a basic breathing exercise."""
        self.text_to_speech.say("Now, continue to breathe slowly.")
        self.text_to_speech.say("Inhale counting to 4...")
        time.sleep(4.0)
        self.text_to_speech.say("Hold for 2...")
        time.sleep(2.0)
        self.text_to_speech.say("Now exhale counting to 6.")
        time.sleep(6.0)

    def full_immersion(self, play_sound_callback, recognize_speech_callback):
        """Full meditation experience with nature sound selection."""
        self.text_to_speech.say("Relax every part of your body...")
        time.sleep(5.0)
        
        play_sound_callback("bells")
        time.sleep(5.0)
        
        self.text_to_speech.say("Imagine yourself in a peaceful place...")
        
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
        
        play_sound_callback("bells")
        self.text_to_speech.say("When you're ready, slowly open your eyes.")

    def quick_meditation(self, play_sound_callback):
        """Short meditation session with basic guidance."""
        self.text_to_speech.say("Let's take a moment to relax.")
        self.poses_module.perform_meditation_pose()
        self.breathing_guide()
        play_sound_callback("quick_meditation")
        self.text_to_speech.say("Thank you for taking this moment for yourself.")
           
    def full_meditation(self, play_sound_callback, recognize_speech_callback):
        """Extended meditation combining quick meditation and full immersion."""
        self.quick_meditation(play_sound_callback)
        self.text_to_speech.say("Let's continue!")
        self.full_immersion(play_sound_callback, recognize_speech_callback)
        self.text_to_speech.say("Great job! I hope it was a positive experience.")

    def perform_intro(self, play_sound_callback, recognize_speech_callback):
        """Introduction to meditation session with duration selection."""
        self.text_to_speech.say("Hello! Welcome to this guided meditation session.")
        self.text_to_speech.say("Tell me, do you prefer a short or long session?")
        
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

    def perform_sad(self, play_sound_callback, recognize_speech_callback):
        """
        Joke-telling interaction to improve mood.
        
        Features:
            - Sequential joke telling
            - Option to hear more jokes
            - Comedy sound effects
        """
        try:
            self.text_to_speech.say("If you're feeling sad, a joke might lift your spirits!")
            joke_index = 0

            self.text_to_speech.say(Behaviours.JOKES[joke_index])
            play_sound_callback("comedy")
            joke_index += 1
            
            while True:
                self.text_to_speech.say("Do you want to hear another one? Reply yes or no.")
                recognized_word = recognize_speech_callback()

                if recognized_word == "yes":
                    self.text_to_speech.say(Behaviours.JOKES[joke_index])
                    play_sound_callback("comedy")
                    joke_index += 1
                elif recognized_word == "no":
                    self.text_to_speech.say("Alright, I hope you had fun! See you next time!")
                    break
                else:
                    self.text_to_speech.say("Answer not allowed, retry!")
        except Exception as e:
            print("[ERROR] A problem occurred:", e)