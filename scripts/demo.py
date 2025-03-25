# Import necessary libraries
import pepper  # Main Pepper robot interface
import subprocess  # For running system commands
import time  # For timing operations
from pathlib import Path  # For cross-platform path handling
import threading  # For parallel execution
import os  # For filesystem operations

# File indexing system to prevent overwrites
VIDEO_INDEX = 0  # Counter for video files (pepper_video_0.avi, pepper_video_1.avi, etc.)
AUDIO_INDEX = 0  # Counter for audio files (pepper_audio_0.wav, pepper_audio_1.wav, etc.)
INPUT_INDEX = 0  # Counter for merged files (input_0.mp4, input_1.mp4, etc.)

# Directory setup
script_dir = Path(__file__).parent  # Directory containing this script
parent_dir = script_dir.parent  # Parent directory
video_dir = parent_dir / "videos"  # Stores recorded videos
audio_dir = parent_dir / "audios"  # Stores recorded audio
input_dir = parent_dir / "inputs"  # Stores merged audio-video files
predictions_dir = parent_dir / "predictions.txt"  # Emotion prediction results
transfer_dir = parent_dir / "transfer"  # For file transfers with Pepper

# Ensure required directories exist
os.makedirs(video_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(input_dir, exist_ok=True)

def get_latest_index():
    """
    Scans existing files to determine the next available index number.
    Prevents file overwrites by maintaining sequential numbering.
    Updates global VIDEO_INDEX, AUDIO_INDEX, and INPUT_INDEX.
    """
    global VIDEO_INDEX, AUDIO_INDEX, INPUT_INDEX
    
    # Get sorted lists of existing files
    audio_files = sorted(f for f in os.listdir(audio_dir) 
                       if f.startswith("pepper_audio_") and f.endswith(".wav"))
    video_files = sorted(f for f in os.listdir(video_dir) 
                       if f.startswith("pepper_video_") and f.endswith(".avi"))
    input_files = sorted(f for f in os.listdir(input_dir) 
                       if f.startswith("input_") and f.endswith(".mp4"))

    # Update indices based on highest found file number
    if audio_files:
        AUDIO_INDEX = int(audio_files[-1].split("_")[-1].split(".")[0]) + 1
    if video_files:
        VIDEO_INDEX = int(video_files[-1].split("_")[-1].split(".")[0]) + 1
    if input_files:
        INPUT_INDEX = int(input_files[-1].split("_")[-1].split(".")[0]) + 1

def get_ssh_command(file_type, index):
    """
    Generates SSH command to transfer files from Pepper to local machine.
    
    Args:
        file_type (str): "audio" or "video" 
        index (int): File index number
        
    Returns:
        list: Command list for subprocess execution
    """
    file_extension = "wav" if file_type == "audio" else "avi"
    return [
        "sshpass", "-p", "pepperina2023", "scp",  # Using sshpass for password automation
        f"nao@192.168.0.67:/home/nao/transfer/pepper_{file_type}_{index}.{file_extension}",  # Source
        f"{parent_dir}/{file_type}/pepper_{file_type}_{index}.{file_extension}"  # Destination
    ]

# Command to recursively transfer all files from Pepper's transfer directory
transfer_command = [
    "sshpass", "-p", "pepperina2023", "scp",
    "-r", "nao@192.168.0.67:/home/nao/transfer/", str(parent_dir)
]

# Command to run emotion prediction model
prediction_command = [
    "python", "/home/mungowz/Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/main.py",
    "--no_train", "--no_val", "--predict", "--test", "--device", "cpu",
    "--path_eeg", "/home/mungowz/Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification_old/Empatica_EPOCX/SEED_IV/eeg_raw_data",
    "--video_audio_dataset_path", input_dir / f"inputs_{INPUT_INDEX}.mp4"
]

def merge_audio_video():
    """
    Merges corresponding audio and video files into MP4 format using ffmpeg.
    Processes all available matching pairs in the audio and video directories.
    Updates INPUT_INDEX after merging.
    """
    global INPUT_INDEX

    for i in range(AUDIO_INDEX):
        audio_path = audio_dir / f"pepper_audio_{i}.wav"
        video_path = video_dir / f"pepper_video_{i}.avi"
        output_path = input_dir / f"input_{i}.mp4"

        if audio_path.exists() and video_path.exists():
            ffmpeg_command = [
                "ffmpeg", "-y",  # Overwrite without prompting
                "-i", str(video_path),  # Input video
                "-i", str(audio_path),  # Input audio
                "-c:v", "copy",  # Stream copy video (no re-encode)
                "-c:a", "aac",  # Encode audio to AAC
                "-strict", "experimental",  # Allow experimental codecs
                str(output_path)
            ]

            subprocess.run(ffmpeg_command, check=True)
            print(f"[INFO] Created merged file: {output_path}")

    INPUT_INDEX += 1

def start_recording_session(pepper_test):  
    """
    Starts synchronized audio and video recording on Pepper.
    
    Args:
        pepper_test: Initialized Pepper instance
    """
    pepper_test.record_audio_video(f"pepper_video", f"pepper_audio")
        
def stop_recording_session(pepper_test):
    """
    Stops ongoing recordings and increments file counters.
    
    Args:
        pepper_test: Initialized Pepper instance
    """
    global VIDEO_INDEX, AUDIO_INDEX
    pepper_test.stop_recording()
    VIDEO_INDEX += 1
    AUDIO_INDEX += 1

def main():
    """
    Main workflow:
    1. Initializes Pepper and greets user
    2. Records initial interaction
    3. Transfers and processes media
    4. Runs emotion prediction
    5. Responds based on detected emotion
    6. Records follow-up interaction
    7. Cleans up and transfers data
    """
    global VIDEO_INDEX, AUDIO_INDEX, INPUT_INDEX

    get_latest_index()  # Initialize file counters

    # Initialize Pepper and start interaction
    pepper_test = pepper.Pepper()
    pepper_test.text_to_speech.say("Hi, how are you feeling today?")
    print("[PEPPER] Hi, how are you feeling today?\n")   
    time.sleep(1.0)  # Pause for user response

    # First recording session (3 seconds)
    pepper_test.poses_module.lock_head()  # Stabilize for recording
    recording_thread = threading.Thread(target=start_recording_session, args=(pepper_test,), daemon=True)
    recording_thread.start()
    time.sleep(3)
    recording_thread.join()
    stop_recording_session(pepper_test)

    # Transfer and process media
    subprocess.run(get_ssh_command("audio", AUDIO_INDEX))
    subprocess.run(get_ssh_command("video", VIDEO_INDEX))
    merge_audio_video()

    # Emotion prediction
    pepper_test.text_to_speech.say("I'm processing your data...")
    print("[PEPPER] Processing data...\n")
    subprocess.run(prediction_command)

    # Handle prediction results
    try:
        with open(predictions_dir, "r") as file:
            lines = file.readlines()
            prediction = int(lines[-1].strip()) if lines else None
    except Exception as e:
        print(f"[Error] {e}\n")
        return

    # Response based on emotion
    if prediction is not None:
        emotions = ["neutral", "happy", "angry", "sad"]
        emotion_detected = emotions[prediction]
        pepper_test.text_to_speech.say(f"Today you look {emotion_detected}!")
        print(f"[PEPPER] Detected emotion: {emotion_detected}\n")

        # Second recording during interaction
        recording_thread = threading.Thread(target=start_recording_session, args=(pepper_test,), daemon=True)
        recording_thread.start()
        pepper_test.perform_behaviours(prediction)

    # Clean up
    pepper_test.text_to_speech.say("How was it?")
    print("[PEPPER] How was it?\n")
    pepper_test.poses_module.unlock_head()
    recording_thread.join()
    stop_recording_session(pepper_test)
    subprocess.run(transfer_command)
    merge_audio_video()

def start():    
    """
    Initial interaction phase:
    - Greets user
    - Records initial 3-second clip
    - Transfers media files
    """
    global VIDEO_INDEX, AUDIO_INDEX, INPUT_INDEX

    get_latest_index()
    pepper_test = pepper.Pepper()
    pepper_test.text_to_speech.say("Hi, how are you feeling today?")
    print("[PEPPER] Hi, how are you feeling today?\n")   
    time.sleep(1.0)

    pepper_test.poses_module.lock_head()
    recording_thread = threading.Thread(target=start_recording_session, args=(pepper_test,), daemon=True)
    recording_thread.start()
    time.sleep(3)
    recording_thread.join()
    stop_recording_session(pepper_test)
    pepper_test.poses_module.unlock_head()
    
def finish(prediction):
    """
    Final interaction phase:
    - Provides emotion feedback
    - Performs appropriate behavior
    - Records follow-up interaction
    
    Args:
        prediction (int): Detected emotion index
    """
    pepper_test = pepper.Pepper()
    pepper_test.poses_module.lock_head()

    if prediction is not None:
        emotions = ["neutral", "happy", "angry", "sad"]
        emotion_detected = emotions[prediction]
        pepper_test.text_to_speech.say(f"Today you look {emotion_detected}!")
        print(f"[PEPPER] Detected emotion: {emotion_detected}\n")

        recording_thread = threading.Thread(target=start_recording_session, args=(pepper_test,), daemon=True)
        recording_thread.start()
        pepper_test.perform_behaviours(prediction)

    pepper_test.text_to_speech.say("How was it?")
    print("[PEPPER] How was it?\n")
    pepper_test.poses_module.unlock_head()
    recording_thread.join()
    stop_recording_session(pepper_test)
    pepper_test.poses_module.unlock_head()
    
if __name__ == "__main__":
    # Example usage:
    # start()  # For initial recording
    finish(2)  # For testing with "angry" emotion (index 2)