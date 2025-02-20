from naoqi import ALProxy
import time

def main():
    # Configurazione del robot
    ROBOT_IP = "192.168.1.104"  # Inserisci l'IP del tuo robot
    ROBOT_PORT = 9559

    # Creazione delle proxy
    motion_proxy = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)
    posture_proxy = ALProxy("ALRobotPosture", ROBOT_IP, ROBOT_PORT)

    # Rilassamento delle giunture e inizializzazione della postura
    motion_proxy.wakeUp()
    posture_proxy.goToPosture("SitRelax", 1.0)

    # Configurazione delle posizioni delle mani per il gesto "ohm" con mani chiuse
    names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
             "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
             "LHand", "RHand"]
    angles = [1.0, 0.2, -1.0, -0.5, 0.3,  # Braccio sinistro
              1.0, -0.2, 1.0, 0.5, -0.3,  # Braccio destro
              0.2, 0.2]                   # Mani chiuse (0.2 = semi-chiuse)
    times = [1.0] * len(names)            # Tempo di esecuzione per ogni giuntura

    # Esecuzione del gesto
    motion_proxy.angleInterpolation(names, angles, times, True)

    # Pausa per mantenere la posizione
    time.sleep(5)

    # Tornare alla posizione iniziale
    posture_proxy.goToPosture("SitRelax", 1.0)
