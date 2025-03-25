import time
import poses_old
import utils


def user_feedback():
    utils.text_to_speech.say("How are you? Do you want to continue?")
    print("[PEPPER] How are you? Do you want to continue?\n")
    time.sleep(1.0)
    
    utils.text_to_speech.say("Answer with yes or no.")
    print("[PEPPER] Answer with yes or no.\n")

    while True:
        time.sleep(2.0)
        choice = utils.recognize_speech()
  
        if choice == "yes":
            utils.text_to_speech.say("Great, let's continue!")
            print("[PEPPER] Great, let's continue!\n")
            time.sleep(2.0)
            return True
        
        elif choice == "no":
            utils.text_to_speech.say("Okay! Goodbye!")
            print("[PEPPER] Okay! Goodbye!\n")
            poses_old.bye()
            return False

        else:
            utils.text_to_speech.say("Answer not allowed, retry!")
            print("Answer not allowed, retry!\n")
            time.sleep(2.0)


def breathing_guide():
    utils.text_to_speech.say("Now, continue to breathe slowly.")
    print("[PEPPER] Now, continue to breathe slowly.\n")
    time.sleep(1.0)

    utils.text_to_speech.say("Inhale counting to 4...")
    print("[PEPPER] Inhale counting to 4...\n")
    time.sleep(4.0)
    
    utils.text_to_speech.say("Hold for 2...")
    print("[PEPPER] Hold for 2...\n")
    time.sleep(2.0)
    
    utils.text_to_speech.say("Now exhale counting to 6.")
    print("[PEPPER] Now exhale counting to 6.\n")
    time.sleep(6.0)
    
    return


def full_immersion():
    utils.text_to_speech.say("Relax every part of your body, starting from the head.")
    print("[PEPPER] Relax every part of your body, starting from the head.\n")
    time.sleep(5.0)
    
    utils.text_to_speech.say("Relax your forehead, eyes, cheeks...")
    print("[PEPPER] Relax your forehead, eyes, cheeks...\n")    
    time.sleep(5.0)

    utils.text_to_speech.say("Slowly move down to the shoulders, chest, and arms...")
    print("[PEPPER] Slowly move down to the shoulders, chest, and arms...\n")
    time.sleep(5.0)

    utils.play_sound("bells")
    time.sleep(5.0)
    
    utils.text_to_speech.say("Imagine yourself in a peaceful place, like a beach at sunset or a green forest.")
    print("[PEPPER] Imagine yourself in a peaceful place, like a beach at sunset or a green forest.\n")
    time.sleep(5.0)
    
    utils.text_to_speech.say("Focus on the sound of the waves or the birds singing. Which do you prefer, forest or sea?")
    print("[PEPPER] Focus on the sound of the waves or the birds singing. Which do you prefer, forest or sea?\n")
    time.sleep(5.0)    
    
    while True:
        time.sleep(2.0)
        
        selection = utils.recognize_speech()

        if selection == "forest":
            utils.play_sound("birds")
            break

        elif selection == "sea":
            utils.play_sound("seashore")
            break
            
        else:
             utils.text_to_speech.say("Answer not allowed, retry!")
             print("Answer not allowed, retry!\n")
             time.sleep(2.0)
    
    utils.play_sound("bells")
    time.sleep(2.0)

    utils.text_to_speech.say("When you're ready, slowly move your fingers, then open your eyes.")
    print("[PEPPER] When you're ready, slowly move your fingers, then open your eyes.\n")
    time.sleep(5.0)

    return


def quick_meditation():

    utils.text_to_speech.say("Let's take a moment to relax.")
    print("[PEPPER] Let's take a moment to relax.\n")
    time.sleep(2.0)

    utils.text_to_speech.say("Find a comfortable position, sitting or standing.")
    print("[PEPPE] Find a comfortable position, sitting or standing.\n")
    time.sleep(2.0)
    poses_old.perform_meditation_pose()

    utils.text_to_speech.say("Close your eyes if you like, or focus on a calm point in front of you.")
    print("[PEPPER] Close your eyes if you like, or focus on a calm point in front of you.\n")
    time.sleep(2.0)
    poses_old.perform_meditation_pose()

    breathing_guide()
    utils.text_to_speech.say("Now try it on your own!")
    print("[PEPPER] Now try it on your own!\n")
    time.sleep(5.0)

    utils.play_sound("bells")
    utils.play_sound("quick_meditation")

    utils.text_to_speech.say("When you're ready, slowly open your eyes.")
    print("[PEPPER] When you're ready, slowly open your eyes.\n")
    time.sleep(5.0)

    utils.play_sound("bells")  
    utils.text_to_speech.say("Thank you for taking this moment for yourself.")
    print("[PEPPER] Thank you for taking this moment for yourself.\n")
    
    return
    
    
def full_meditation():

    quick_meditation()

    utils.text_to_speech.say("Let's continue!")
    print("[PEPPER] Let's continue!\n")
    time.sleep(1.0)

    full_immersion()
    time.sleep(1.0)

    utils.text_to_speech.say("Great job! I hope it was a positive experience.")
    print("[PEPPER] Great job! I hope it was a positive experience.\n")
    time.sleep(1.0)

    return


def intro():
    utils.text_to_speech.say("Hello! Welcome to this guided meditation session.")
    print("[PEPPER] Hello! Welcome to this guided meditation session.\n")
    time.sleep(1.0)
    
    utils.text_to_speech.say("If you feel agitated or angry, this might help you.")
    print("[PEPPER] If you feel agitated or angry, this might help you.\n")
    time.sleep(1.0)
    
    utils.text_to_speech.say("Tell me, do you prefer a short or long session?")
    print("[PEPPER] Tell me, do you prefer a short or long session?\n")
    
    while True:
        time.sleep(2.0)
    
        user_selection = utils.recognize_speech()

        if user_selection == "short":
            quick_meditation()
            break
        
        elif user_selection == "long":
            full_meditation()
            break
        
        else:
            utils.text_to_speech.say("Answer not allowed, retry!")
            print("Answer not allowed, retry!\n")
            time.sleep(2.0)
        
    return


def main():
    try:
        while True:
            intro()
            if not user_feedback():
                break
        
    except Exception as e:
        print("[ERROR] Some problems happened:", e)


