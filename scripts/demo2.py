import pepper 
import subprocess
import time
from pathlib import Path
import threading

VIDEO_INDEX = 0
AUDIO_INDEX = 0

script_dir = Path(__file__).parent
parent_dir = script_dir.parent
video_dir = parent_dir / f"video/pepper_video_{VIDEO_INDEX}.avi"
audio_dir = parent_dir / f"audio/pepper_audio_{AUDIO_INDEX}.wav"
input_dir = parent_dir / "input.mp4"
predictions_dir = parent_dir / "predictions.txt"

audio_command = [
    "sshpass", 
    "-p", 
    "pepperina2023", 
    "scp",
    f"nao@192.168.1.104:/home/nao/transfer/pepper_audio_{AUDIO_INDEX}.wav", 
    audio_dir
]

video_command = [
    "sshpass", 
    "-p", 
    "pepperina2023", 
    "scp", 
    f"nao@192.168.1.104:/home/nao/transfer/pepper_video_{VIDEO_INDEX}.avi", 
    video_dir
]

ffmpeg_command = [
    "ffmpeg", 
    "-y",
    "-i", 
    video_dir, 
    "-i",
    audio_dir,
    "-c:v", 
    "copy", 
    "-c:a", 
    "aac", 
    "-strict", 
    "experimental", 
    input_dir
]

prediction_command = [
    "python", 
    "Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/main.py",
    "--no_train", 
    "--no_val", 
    "--predict",
    "--test", 
    "--device", 
    "cpu",
    "--path_cached",
    "/home/mungowz/.torcheeg/datasets_1740495597019_i0VpE"
]

def test():
    pepper_test = pepper.Pepper()
    # pepper_test.behaviours_module.perform_neutral(pepper_test.play_sound, pepper_test.recognize_speech)
    # pepper_test.behaviours_module.perform_happy(pepper_test.play_sound, pepper_test.recognize_speech)
    pepper_test.behaviours_module.perform_angry(pepper_test.play_sound, pepper_test.recognize_speech)
    
def execute_timer(interval, pepper_test, record_session):    
    while True:
        record_session(pepper_test)
        time.sleep(interval)
    
def record_session(pepper_test):    
    global VIDEO_INDEX
    global AUDIO_INDEX
    pepper_test.record_audio_video(f"pepper_video_{VIDEO_INDEX}", f"pepper_audio_{AUDIO_INDEX}")
    time.sleep(4)
    pepper_test.stop_recording()
    
    VIDEO_INDEX += 1;
    AUDIO_INDEX += 1;

def main():
    pepper_test = pepper.Pepper()
    pepper_test.text_to_speech.say("Hi how are you feeling today?")
    print("[PEPPER] Hi how are you feeling today?\n")   
    time.sleep(1.0)
         
    pepper_test.poses_module.lock_head() 
    
    record_session(pepper_test)
    
    subprocess.run(audio_command)
          
    print("[INFO] Audio received!\n")
    
    subprocess.run(video_command)
        
    print("[INFO] Video received!\n")
                
    subprocess.run(ffmpeg_command)
    
    pepper_test.text_to_speech.say("I'm processing your data...")
    print("[PEPPER] I'm processing your data...\n")
    pepper_test.text_to_speech.say("Please wait!")
    print("[PEPPER] Please wait!\n")
            
    subprocess.run(prediction_command)    
    
    recording_thread = threading.Thread(target= execute_timer, args=(10, pepper_test, record_session), daemon=True)
    recording_thread.start()
     
    with open(predictions_dir, "r") as file:
        lines = file.readlines()
        if lines:
            prediction = lines[-1].strip()
        else:
            print("[Error] File is empty.\n")
            return
     
    prediction = int(prediction)
     
    emotions = ["neutral", "happy", "angry", "sad"]
    pepper_test.text_to_speech.say("Today you look " + emotions[prediction] + "!\n")
    print("[PEPPER] Today you look " + emotions[prediction] + "!\n")

    pepper_test.perform_behaviours(prediction)
      
    pepper_test.text_to_speech.say("How it was?")
    print("[Pepper] How it was?\n")         
    pepper_test.poses_module.unlock_head()           
       
if __name__ == "__main__":
    main()
    # test()
