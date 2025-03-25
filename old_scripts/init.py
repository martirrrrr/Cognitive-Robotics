import utils 
import record
import sad
import happy
import neutral 
import angry
import poses_old
import subprocess

def test():
    sad.main()

def main():
    utils.text_to_speech.say("Hi how are you feeling today?")
    print("[PEPPER] Hi how are you feeling today?\n")   
    time.sleep(2)
      
    poses_old.lock_head() 
            
    record.record_audio_video("pepper_video", "pepper_audio")   
            
    poses_old.unlock_head()
            
    command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_video.avi", 
        "/home/mungowz/cognitive_robotics/video/pepper_video.avi"
    ]
    subprocess.run(command)
          
    print("[INFO] Audio received!\n")
    
    command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_audio.wav", 
        "/home/mungowz/cognitive_robotics/audio/pepper_audio.wav"
    ]
    subprocess.run(command)
        
    print("[INFO] Video received!\n")
             
    command = [
        "ffmpeg", 
        "-i", 
        "/home/mungowz/cognitive_robotics/video/pepper_video.avi", 
        "-i",
        "/home/mungowz/cognitive_robotics/audio/pepper_audio.wav",
        "-c:v", 
        "copy", 
        "-c:a", 
        "aac", 
        "-strict", 
        "experimental", 
        "/home/mungowz/cognitive_robotics/input.mp4"
    ]   
    subprocess.run(command)
    
    utils.text_to_speech.say("I'm processing your data...")
    print("[PEPPER] I'm processing your data...\n")
    utils.text_to_speech.say("Please wait!")
    print("[PEPPER] Please wait!\n")
        
    command = [
        "python", 
        "Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/main.py",
        "--no_train", 
        "--no_val", 
        "--predict",
        "--test", 
        "--device", 
        "cpu",
        "--path_cached",
        "/home/mungowz/.torcheeg/datasets_1740404252543_i0VpE"
    ]      
    subprocess.run(command)    
     
    with open("/home/mungowz/cognitive_robotics/predictions.txt", "r") as file:
        lines = file.readlines()
        if lines:
            prediction = lines[-1].strip()
        else:
            print("[Error] File is empty.\n")
            return
     
    prediction = int(prediction)
     
    emotions = ["neutral", "happy", "angry", "sad"]
    utils.text_to_speech.say("Today you look " + emotions[prediction] + "!\n")
    print("[PEPPER] Today you look " + emotions[prediction] + "!\n")

    if prediction == 0:
        neutral.main()
    elif prediction == 1:
        happy.main()
    elif prediction == 2:
        angry.main()
    elif prediction == 3:
        sad.main()
     
    utils.text_to_speech.say("How it was?")
    print("[Pepper] How it was?\n") 
     
    poses_old.lock_head()
 
    record.record_audio_video("pepper_video", "pepper_audio")   
            
    poses_old.unlock_head()           
            
    command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_video.avi", 
        "/home/mungowz/cognitive_robotics/video/pepper_video.avi"
    ]
    subprocess.run(command)
            
    print("[INFO] Audio received!\n")
    
    command = [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp", 
        "nao@192.168.1.104:/home/nao/transfer/pepper_audio.wav", 
        "/home/mungowz/cognitive_robotics/audio/pepper_video.wav"
    ]
    subprocess.run(command)
        
    print("[INFO] Video received!\n")
        
    command = [
        "python", 
        "Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/main.py",
        "--no_train", 
        "--no_val", 
        "--predict",
        "--test", 
        "--device", 
        "cpu",
        "--path_cached",
        "/home/mungowz/.torcheeg/datasets_1740404252543_i0VpE"
    ]      
    subprocess.run(command)
     
            
if __name__ == "__main__":
    test()  
