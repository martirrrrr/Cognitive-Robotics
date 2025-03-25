import socket
import random
import time
import subprocess


def pc_client():
    HOST = "0.0.0.0"
    PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        while True:
            response = client_socket.recv(1024).decode()
            if response == "4":
                print("[INFO] Server has recorded new audio and video.\n")
            else:
                print("[ERROR] Some problem has happened during audio and video recordings!\n")
                return
                
            command = ['sshpass', '-p', 'pepperina2023', 'scp', 'nao@192.168.1.104:/home/nao/transfer/pepper_video.avi', '/home/mungowz/cognitive_robotics/video/pepper_video.avi']
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            
            command = ['sshpass', '-p', 'pepperina2023', 'scp', 'nao@192.168.1.104:/home/nao/transfer/pepper_audio.wav', '/home/mungowz/cognitive_robotics/audio/pepper_video.wav']
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            
            client_socket.sendall("6".encode())
            
            client_socket.recv(1024).decode()
                
            command = random.randint(0, 3)
            print("[INFO] Sending command: " + str(command) + ".\n")
            client_socket.sendall(str(command).encode())
            
            response = client_socket.recv(1024).decode()
            if response == "5":
                print("[INFO] Server is ready to accept new data.\n")
            else:
                print("[ERROR] Server isn't ready to accept new data!\n")
                returnS
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("[INFO] Client stopped!.\n")
    finally:
        client_socket.close()
        return

if __name__ == "__main__":
    pc_client()
