import time
import qi
import sys


ip = "192.168.1.104"
port = 9559


vocabulary = [
    "yes",
    "no",
    "forest", 
    "sea",
    "short",
    "long",
    "rock", 
    "techno", 
    "classical",
    "relax", 
    "music", 
    "joke"
]


sound_files = {
    "bells": "/home/nao/CR/bells.mp3",
    "birds": "/home/nao/CR/birds.mp3",
    "seashore": "/home/nao/CR/seashore.mp3",
    "quick_meditation": "/home/nao/CR/quick_meditation.mp3",
    "full_meditation": "/home/nao/CR/full_meditation.mp3",
    "techno": "/home/nao/CR/techno.mp3",
    "classical": "/home/nao/CR/classic.mp3",
    "rock": "/home/nao/CR/rock2.mp3",
    "comedy": "/home/nao/CR/comedy.mp3"
}


jokes = [
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


def connect_to_pepper(ip, port):
    session = qi.Session()
    try:
        session.connect("tcp://" + ip + ":" + str(port))
        print("[INFO] Robot connection established.\n")
        return session
    except RuntimeError as e:
        print("[ERROR] It's impossible to connect to Pepper. Check IP address or connetction to network\n.")
        raise e


session = connect_to_pepper(ip, port)
text_to_speech = session.service("ALTextToSpeech")
motion = session.service("ALMotion")
audio_player = session.service("ALAudioPlayer")
speech_recognition = session.service("ALSpeechRecognition")
memory = session.service("ALMemory")
robot_posture = session.service("ALRobotPosture")
video_recorder = session.service("ALVideoRecorder")
audio_recorder = session.service("ALAudioRecorder")
robot_posture = session.service("ALRobotPosture")


def recognize_speech():

    recognized_word = None

    try:
        text_to_speech.say("Waiting for user's input")
        print("[PEPPER] Waiting for user's input.\n")

        while recognized_word is None:
            event_data = memory.getData("WordRecognized")
            if event_data and isinstance(event_data, list) and len(event_data) > 1:
                word, confidence = event_data[0], event_data[1]
                if confidence >= 0.4:
                    recognized_word = word
                    print("[INFO] Detected word: " + str(recognized_word) + ".\n")
                    text_to_speech.say("You have said: " + str(recognized_word))
                    print("[PEPPER] You have said: " + str(recognized_word) + ".\n")
            time.sleep(0.1)
            
    except Exception as e:
        print("[ERROR] Some problems happened during speech recognition: ", e)
    
    return recognized_word


def set_speech_service():
    speech_recognition.pause(True)
    speech_recognition.setLanguage("English")
    text_to_speech.setLanguage("English")
    speech_recognition.setVocabulary(vocabulary, False)
    speech_recognition.subscribe("Recognizer")
    speech_recognition.pause(False)


def play_sound(sound_file):
    audio_player.playFile(sound_files.get(sound_file, None))
    
   
set_speech_service()
 
 
