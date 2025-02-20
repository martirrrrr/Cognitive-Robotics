# Import necessary libraries
from naoqi import ALProxy
import time

# Connect to Pepper
pepper_ip = "192.168.1.104"  # Pepper's IP address
pepper_port = 9559  # Connection port

# Create proxies for the required services
motion = ALProxy("ALMotion", pepper_ip, pepper_port)
posture = ALProxy("ALRobotPosture", pepper_ip, pepper_port)
tts = ALProxy("ALTextToSpeech", pepper_ip, pepper_port)

# Function for meditation
def meditation():
    tts.say("Let's start the meditation session. Close your eyes and breathe deeply.")
    motion.setBreathEnabled("Body", True)
    time.sleep(60)  # Meditate for 60 seconds
    motion.setBreathEnabled("Body", False)
    tts.say("The meditation session is over. Slowly open your eyes.")

# Function for yoga
def yoga():
    tts.say("Let's start the yoga session. Follow my movements.")
    posture.goToPosture("StandInit", 1.0)
    time.sleep(2)
    motion.angleInterpolationWithSpeed("HeadYaw", 0.5, 0.1)  # Example movement
    time.sleep(2)
    motion.angleInterpolationWithSpeed("HeadYaw", -0.5, 0.1)
    time.sleep(2)
    posture.goToPosture("Stand", 1.0)
    tts.say("The yoga session is over. Relax.")

# Function for relaxation
def relaxation():
    tts.say("Let's start the relaxation session. Lie down and close your eyes.")
    posture.goToPosture("LyingBack", 1.0)
    motion.setBreathEnabled("Body", True)
    time.sleep(60)  # Relax for 60 seconds
    motion.setBreathEnabled("Body", False)
    posture.goToPosture("Stand", 1.0)
    tts.say("The relaxation session is over. I hope you enjoyed it.")

def main():     
    # Execute the sessions
    meditation()
    yoga()
    relaxation()


'''
# Configurazione del robot
ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 45710

# Creazione delle proxy
motion_proxy = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)
posture_proxy = ALProxy("ALRobotPosture", ROBOT_IP, ROBOT_PORT)

def crane_pose():
    # Porta Pepper in posizione iniziale stabile
    posture_proxy.goToPosture("StandInit", 1.0)

    # Definizione delle articolazioni e degli angoli
    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",  # Braccio sinistro
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",  # Braccio destro
        "LHipRoll", "LHipPitch", "LKneePitch",                                    # Gamba sinistra
        "RHipRoll", "RHipPitch", "RKneePitch",                                    # Gamba destra
        "HeadYaw", "HeadPitch"                                                    # Testa
    ]

    # Angoli in radianti per la posa della gru
    joint_angles = [
        1.0,  0.3, -1.0, -0.5, 0.3,  # Braccio sinistro sollevato
        1.0, -0.3,  1.0,  0.5, -0.3,  # Braccio destro sollevato
        0.2, -0.3,  0.0,              # Gamba sinistra leggermente piegata
       -0.2,  0.5,  1.0,              # Gamba destra piegata per equilibrio
        0.0,  0.2                     # Testa dritta e leggermente inclinata verso il basso
    ]

    # Tempi di transizione per i movimenti
    times = [2.0] * len(joint_names)

    # Esegui i movimenti
    motion_proxy.angleInterpolation(joint_names, joint_angles, times, True)

    # Mantieni la posa per 5 secondi
    time.sleep(5)

    # Torna alla posizione iniziale
    posture_proxy.goToPosture("StandInit", 1.0)

# Esegui la posa della gru
crane_pose()
'''
