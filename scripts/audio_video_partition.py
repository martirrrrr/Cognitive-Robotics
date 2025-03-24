import os
import subprocess
from moviepy.editor import VideoFileClip

def extract_segments(video_path, output_folder, interval=10, slice_duration=3):
    # Crea la cartella se non esiste
    os.makedirs(output_folder, exist_ok=True)

    # Ottieni la durata totale del video come float
    clip = VideoFileClip(video_path)
    total_duration = clip.duration  # Più preciso con i float

    # Contatore per i nomi dei file
    slice_index = 1
    start_time = 0  # Iniziamo da 0s

    while start_time + slice_duration <= total_duration:  # Controlliamo PRIMA di creare il segmento
        print(f"DEBUG - start_time: {start_time}, total_duration: {total_duration}")

        output_file = os.path.join(output_folder, f"Video_Slice_{slice_index}.mp4")

        # Comando ffmpeg per estrarre il segmento
        cmd = ["ffmpeg", "-y", "-ss", str(start_time), "-i", video_path, "-t", str(slice_duration), "-c", "copy", output_file]

        # Esegui il comando senza output
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Creato: {output_file}")

        # Incrementa il contatore per il nome del file
        slice_index += 1

        # Aggiorna il tempo di inizio con il salto di 10s
        start_time += interval + slice_duration

    print(f"Tutti i segmenti sono stati salvati in: {output_folder}")


video_input = "./Test/User_Folder/sampleN.mp4"
output_dir = "./Test/User_Folder/Video_Slices/"
extract_segments(video_input, output_dir)
