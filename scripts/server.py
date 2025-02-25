import socket
import time
import utils
import record
import happy
import sad
import angry
import neutral


def pepper_server():
    HOST = "0.0.0.0"
    PORT = 5000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("[INFO] Pepper server is listening...\n")

    conn, addr = server_socket.accept()
    print("[INFO] Connection established with " + str(addr) + ".\n")

    try:
        for _ in range(2):
            # utils.text_to_speech.say("Hi how are you feeling today?")
            print("[PEPPER] Hi how are you feeling today?\n")
            
            
            record.record_audio_video("pepper_video", "pepper_audio")
            conn.sendall("4".encode())   
            
            response = conn.recv(1024).decode()
            if response == "6":
                print("[INFO] Client has received audio and video.\n")
            else:
                print("[ERROR] Client hasn't received audio and video!\n")
        
            # Potrebbe dire qualcosa intanto
        
            command = ['python', 'Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/main.py', '--no_train', '--no_val', '--predict', '--test', '--device cpu', '--path_cached', '/home/mungowz/Cognitive-Robotics-Project-Multi-Modal-Emotion-Classification/Meta_model/.torcheeg/datasets_1738840093246_i0VpE/']
        
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
        
            conn.sendall("7".encode())
        
            data = conn.recv(1024)
            if not data:
                break

            command = int(data.decode())
            
            emotions = ["happy", "sad", "angry", "neutral"]
            # utils.text_to_speech.say("Today you look " + emotions[command] + "!\n")
            print("[PEPPER] Today you look " + emotions[command] + "!\n")
            
            '''
            if command == 0:
                happy.main()
            elif command == 1:
                sad.main()
            elif command == 2:
                angry.main()
            elif command == 3:
                neutral.main()
            '''

            conn.sendall("5".encode())
    
    except KeyboardInterrupt:
        print("[INFO] Server stopped.\n")
    
    finally:
        conn.close()
        server_socket.close()
        return


if __name__ == "__main__":
    pepper_server()
