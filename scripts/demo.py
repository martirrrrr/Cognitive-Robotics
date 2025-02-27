import pepper 
import subprocess
import time
from pathlib import Path

def test():
    pepper_test = pepper.Pepper()
    pepper_test.behaviours_module.perform_neutral(pepper_test.play_sound, pepper_test.recognize_speech)

def main():
    script_dir = Path(__file__).parent
    parent_dir = script_dir.parent
    video_dir = parent_dir / "video/pepper_video.avi"
    audio_dir = parent_dir / "audio/pepper_audio.wav"
    input_dir = parent_dir / "input.mp4"
    predictions_dir = parent_dir / "predictions.txt"

    print(video_dir)

    audio_command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_audio.wav", 
        audio_dir
    ]

    video_command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_video.avi", 
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

    pepper_test = pepper.Pepper()
    pepper_test.text_to_speech.say("Hi how are you feeling today?")
    print("[PEPPER] Hi how are you feeling today?\n")   
    time.sleep(1.0)
      
    pepper_test.poses_module.lock_head() 
            
    pepper_test.record_audio_video("pepper_video", "pepper_audio")   
            
    pepper_test.poses_module.unlock_head()
            
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
     
    pepper_test.poses_module.lock_head()
 
    pepper_test.record_audio_video("pepper_video", "pepper_audio")   
            
    pepper_test.poses_module.unlock_head()           
            
    subprocess.run(audio_command)
            
    print("[INFO] Audio received!\n")
    
    subprocess.run(video_command)
        
    print("[INFO] Video received!\n")

    subprocess.run(ffmpeg_command)
           
    subprocess.run(prediction_command)
       
if __name__ == "__main__":
    main()
    # test()
