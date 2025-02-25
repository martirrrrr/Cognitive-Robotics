import time
import utils


def start_video_recording(video_recorder, filename):
    try:
        video_recorder.setCameraID(0)
        video_recorder.setResolution(2)
        video_recorder.setFrameRate(10)
        video_recorder.setVideoFormat("MJPG") 

        # utils.text_to_speech.say("Video recording started...")
        print("[PEPPER] Video recording started...\n")
        
        video_recorder.startRecording("/home/nao/transfer", filename)
    except Exception as e:
        print("[ERROR] An issue occurred during video setup:", e)


def start_audio_recording(audio_recorder, filename):
    audio_channels = [0, 0, 1, 0]
    # utils.text_to_speech.say("Audio recording started...")
    print("[PEPPER] Audio recording started...\n")
    audio_recorder.startMicrophonesRecording("/home/nao/transfer/" + filename + ".wav", "wav", 16000, audio_channels)


def stop_video_recording(video_recorder):
    try:
        video_info = video_recorder.stopRecording()
        # utils.text_to_speech.say("Video recording completed!\n")
        # print("[PEPPER] Video recording completed!\n")
        # print("[INFO] Video saved in: " + str(video_info[1]) + ".\n")
        # print("[INFO] Number of frames recorded: " + str(video_info[0]) + ".\n")
        
    except Exception as e:
        print("[ERROR] An issue occurred while stopping video recording:", e)


def stop_audio_recording(audio_recorder):
    audio_recorder.stopMicrophonesRecording()
    # utils.text_to_speech.say("Audio recording completed!\n")
    # print("[PEPPER] Audio recording completed!\n")
    # print("[INFO] Audio saved in: " + str(audio_info[1]) + ".\n")
    # print("[INFO] Number of frames recorded: " + str(audio_info[0]) + ".\n")


def record_audio_video(video_filename, audio_filename):
    try:
        stop_video_recording(utils.video_recorder)
        stop_audio_recording(utils.audio_recorder)
        
        start_video_recording(utils.video_recorder, video_filename)
        start_audio_recording(utils.audio_recorder, audio_filename)
        
        time.sleep(4)
        
        stop_video_recording(utils.video_recorder)
        stop_audio_recording(utils.audio_recorder)
        
        print("[INFO] Audio and video recording successfully completed!\n")
    
    except Exception as e:
        print("[ERROR] An issue occurred:", e)

