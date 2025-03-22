import os
import subprocess
from moviepy.editor import VideoFileClip

def extract_segments(video_path, output_folder, interval=10, slice=3):
    # Create folder
    os.makedirs(output_folder, exist_ok=True)

    # Ottieni la durata del video
    clip = VideoFileClip(video_path)
    total = int(clip.duration)

    # Nome base per i segmenti
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    for start_time in range(0, total, interval):
        output_file = os.path.join(output_folder, f"{base_name}segment{start_time}.mp4")
        
        cmd = ["ffmpeg", "-y", "-ss", str(start_time), "-i", video_path,"-t", str(slice), "-c", "copy", output_file]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Segment saved in: {output_folder}")

# Esempio di utilizzo su Windows
video_input = "video.mp4" 
output_dir = "../video"
estrai_segmenti(video_input, output_dir)
