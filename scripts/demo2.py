import pepper 
import subprocess
import time
from pathlib import Path
import threading
import os

# Initial indices for audio, video, and input files
VIDEO_INDEX = 0
AUDIO_INDEX = 0
INPUT_INDEX = 0

# Define directories
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
video_dir = parent_dir / "video"
audio_dir = parent_dir / "audio"
input_dir = parent_dir / "inputs"
predictions_dir = parent_dir / "predictions.txt"
transfer_dir = parent_dir / "transfer"

# Create necessary directories if they do not exist
os.makedirs(video_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(input_dir, exist_ok=True)

def get_latest_index():
    """ 
    Determines the latest available index for audio, video, and input files 
    to avoid overwriting existing files.
    """
    global VIDEO_INDEX, AUDIO_INDEX, INPUT_INDEX
    
    # Get the list of existing files and sort them
    audio_files = sorted(f for f in os.listdir(audio_dir) if f.startswith("pepper_audio_") and f.endswith(".wav"))
    video_files = sorted(f for f in os.listdir(video_dir) if f.startswith("pepper_video_") and f.endswith(".avi"))
    input_files = sorted(f for f in os.listdir(input_dir) if f.startswith("input_") and f.endswith(".mp4"))

    # Update the indices based on the last file found
    if audio_files:
        AUDIO_INDEX = int(audio_files[-1].split("_")[-1].split(".")[0]) + 1
    if video_files:
        VIDEO_INDEX = int(video_files[-1].split("_")[-1].split(".")[0]) + 1
    if input_files:
        INPUT_INDEX = int(input_files[-1].split("_")[-1].split(".")[0]) + 1

# Function to generate SSH transfer commands for audio and video files
def get_ssh_command(file_type, index):
    return [
        "sshpass", 
        "-p", 
        "pepperina2023", 
        "scp",
        f"nao@192.168.1.104:/home/nao/transfer/pepper_{file_type}_{index}.{'wav' if file_type == 'audio' else 'avi'}", 
        f"{parent_dir}/{file_type}/pepper_{file_type}_{index}.{'wav' if file_type == 'audio' else 'avi'}"
    ]

# Command to transfer the entire "transfer" directory from the robot
transfer_command = [
    "sshpass", 
    "-p", 
    "pepperina2023", 
    "scp",
    "-r", 
    f"nao@192.168.1.104:/home/nao/transfer/", 
    str(parent_dir)
]

# Command to run the emotion prediction model
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

def merge_audio_video():
    """ 
    Merges corresponding audio and video files using ffmpeg 
    and saves the output as an MP4 file.
    """
    global INPUT_INDEX

    for i in range(AUDIO_INDEX):
        audio_path = audio_dir / f"pepper_audio_{i}.wav"
        video_path = video_dir / f"pepper_video_{i}.avi"
        output_path = input_dir / f"input_{i}.mp4"

        # Check if both audio and video files exist
        if audio_path.exists() and video_path.exists():
            ffmpeg_command = [
                "ffmpeg", 
                "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-strict", "experimental",
                str(output_path)
            ]

            subprocess.run(ffmpeg_command, check=True)
            print(f"[INFO] Merged file created: {output_path}")

    INPUT_INDEX += 1

def record_session(pepper_test, interval):  
    """ 
    Continuously records audio and video from Pepper with a given time interval.
    """
    global VIDEO_INDEX, AUDIO_INDEX

    while True:
        # Start recording
        pepper_test.record_audio_video(f"pepper_video_{VIDEO_INDEX}", f"pepper_audio_{AUDIO_INDEX}")
        time.sleep(4)  # Recording duration
        pepper_test.stop_recording()

        # Increment the file indices for the next recording
        VIDEO_INDEX += 1
        AUDIO_INDEX += 1
        time.sleep(interval)

def main():
    global VIDEO_INDEX, AUDIO_INDEX, INPUT_INDEX

    # Get the latest available indices for file naming
    get_latest_index()

    pepper_test = pepper.Pepper()
    pepper_test.text_to_speech.say("Hi, how are you feeling today?")
    print("[PEPPER] Hi, how are you feeling today?\n")   
    time.sleep(1.0)

    pepper_test.poses_module.lock_head()

    # Start recording in a separate thread
    recording_thread = threading.Thread(target=record_session, args=(pepper_test, 10,), daemon=True)
    recording_thread.start()

    # Transfer audio and video files from the robot
    subprocess.run(get_ssh_command("audio", AUDIO_INDEX))
    print("[INFO] Audio received!\n")

    subprocess.run(get_ssh_command("video", VIDEO_INDEX))
    print("[INFO] Video received!\n")

    # Merge the received audio and video files
    merge_audio_video()

    # Process the data using the AI model
    pepper_test.text_to_speech.say("I'm processing your data...")
    print("[PEPPER] I'm processing your data...\n")
    pepper_test.text_to_speech.say("Please wait!")
    print("[PEPPER] Please wait!\n")

    subprocess.run(prediction_command)    

    # Read the prediction result
    try:
        with open(predictions_dir, "r") as file:
            lines = file.readlines()
            prediction = int(lines[-1].strip()) if lines else None
    except Exception as e:
        print(f"[Error] {e}\n")
        return

    # Map the prediction to an emotion and respond accordingly
    if prediction is not None:
        emotions = ["neutral", "happy", "angry", "sad"]
        emotion_detected = emotions[prediction]

        pepper_test.text_to_speech.say(f"Today you look {emotion_detected}!")
        print(f"[PEPPER] Today you look {emotion_detected}!\n")

        pepper_test.perform_behaviours(prediction)

    # End interaction
    pepper_test.text_to_speech.say("How was it?")
    print("[PEPPER] How was it?\n")
    pepper_test.poses_module.unlock_head()

    # Transfer processed data back to the robot
    subprocess.run(transfer_command)       

if __name__ == "__main__":
    main()
