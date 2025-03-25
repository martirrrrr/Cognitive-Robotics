import utils
import time

def bye():
    try:
        joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

        wave_up = [0.5, -0.2, 1.0, 1.5, 0.0]
        
        wave_down = [0.5, -0.2, 1.0, 0.8, 0.0]

        times = [1.0, 1.0, 1.0, 1.0, 1.0]

        utils.motion.angleInterpolation(joint_names, wave_up, times, True)

        for _ in range(3):
            utils.motion.angleInterpolation(joint_names, wave_down, times, True)
            utils.motion.angleInterpolation(joint_names, wave_up, times, True)

        
        rest_position = [1.4, -0.2, 1.3, 0.3, 0.0]
        utils.motion.angleInterpolation(joint_names, rest_position, times, True)

    except Exception as e:
        print("[Error] Error during movement execution: " + str(e))


def perform_meditation_pose():
    print("[INFO] Starting meditation and relaxation pose...\n")

    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "HeadYaw", "HeadPitch", "HipRoll", "HipPitch"
    ]

    
    initial_pose = [1.4, 0.0, -0.3, -0.5, 1.4, 0.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0]

    meditation_pose = [0.8, 0.4, -1.0, -0.4, 0.8, -0.4, 1.0, 0.4, 0.0, 0.2, 0.0, -0.1]

    times = [3.0] * len(joint_names)

    
    utils.motion.angleInterpolation(joint_names, initial_pose, times, True)
    utils.motion.angleInterpolation(joint_names, meditation_pose, times, True)
    utils.motion.angleInterpolation(joint_names, meditation_pose, [5.0] * len(joint_names), True)

    print("[INFO] Meditation pose completed!\n")


def move_arms_in_wave():
    print("[INFO] Wave movement with arms...\n")
    
    names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
    ]

    angles_list = [
        [0.0, -0.5, 0.0],
        [0.2, 0.5, 0.2],
        [-1.0, -0.8, -1.0],
        [-0.5, -0.3, -0.5],
        [0.0, 0.5, 0.0],
        [-0.2, -0.5, -0.2],
        [1.0, 0.8, 1.0],
        [0.5, 0.3, 0.5]
    ]

    times = [
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0]
    ]

    utils.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)


def spin_torso():
    print("[INFO] Rotating torso...\n")
    
    names = ["HipRoll", "HipPitch"]
    
    angles_list = [
        [0.0, -0.5, 0.0],
        [0.2, 0.5, 0.2]
    ]

    times = [
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0]
    ]

    utils.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)


def step_side_to_side():
    print("[INFO] Side step...\n")
    
    names = ["HipPitch"]
    
    angles_list = [
        [0.0, -0.5, 0.0]
    ]

    times = [
        [1.0, 2.0, 3.0]
    ]

    utils.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)


def nod_head():
    print("[INFO] Head movement...\n")
    
    names = ["HeadPitch", "HeadYaw"]
    
    angles_list = [
        [0.0, -0.5, 0.0],
        [0.2, 0.5, 0.2]
    ]

    times = [
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0]
    ]

    utils.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)


def perform_techno_dance():
    print("[INFO] Starting dance routine...\n")

    for _ in range(2):
        move_arms_in_wave()
        spin_torso()
        step_side_to_side()
        nod_head()
    move_arms_in_wave()
    spin_torso()

    print("[INFO] Dance routine completed!\n")


def perform_rock_dance():

    print("[INFO] Starting guitar simulation...\n")

    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", 
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", 
        "HipRoll", "HipPitch",
        "HeadYaw", "HeadPitch"
    ]

    guitar_moves = [
        [1.0, 0.5, -1.0, -0.5, 1.5, -0.3, 0.8, 1.0, 0.0, -0.2, 0.0, 0.3],
        [1.0, 0.5, -1.2, -0.7, 1.3, -0.5, 1.0, 1.2, 0.2, -0.2, 0.0, 0.5],
        [1.2, 0.6, -1.3, -0.8, 1.4, -0.4, 1.1, 1.3, 0.0, -0.2, 0.1, 0.4],
        [0.8, 0.4, -0.9, -0.6, 1.0, -0.5, 1.2, 0.8, 0.2, -0.3, 0.1, 0.3]
    ]

    times = [0.5] * len(joint_names)
    
    for _ in range(16):
        for move in guitar_moves:
            utils.motion.angleInterpolation(joint_names, move, times, True)

    print("[INFO] Guitar simulation complete!\n")


def perform_classic_dance():
    print("[INFO] Pepper's dance starting...\n")

    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
    ]

    dance_moves = [
        [1.0, 0.7, -1.0, -1.0, 1.0, -0.5, 1.0, 1.0, 0.5, -0.2],
        [0.5, 0.3, -0.5, -0.5, 0.5, -0.3, 0.5, 0.5, -0.5, 0.2],
        [1.2, 0.8, -1.2, -1.2, 1.2, 0.0, 1.2, 1.2, 0.0, 0.0],
        [0.8, 0.2, -0.8, -0.6, 0.8, -0.2, 0.8, 0.6, 0.3, -0.3],
        [1.0, 0.5, -1.0, -1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.2],
        [0.7, 0.4, -0.6, -0.5, 0.7, -0.4, 0.6, 0.5, 0.0, 0.0],
        [1.2, 0.3, -1.2, -0.9, 1.2, 0.3, 1.2, 0.9, -0.2, 0.1],
        [1.0, 0.2, -1.0, -0.7, 1.0, -0.2, 1.0, 0.7, 0.2, -0.1]
    ]

    times = [0.5] * len(joint_names)

    for _ in range(8):
        for move in dance_moves:
            utils.motion.angleInterpolation(joint_names, move, times, True)

    print("[INFO] Dance completed!\n")


def stretch_right_arm():
    utils.text_to_speech.say("Let's raise the right arm to the sky!")
    utils.motion.angleInterpolation("RShoulderPitch", -0.5, 6, True)
    utils.motion.angleInterpolation("RShoulderPitch", 1.5, 6, True)

def stretch_left_arm():
    utils.text_to_speech.say("Now let's raise the left arm to the sky!")
    utils.motion.angleInterpolation("LShoulderPitch", -0.5, 5, True)
    utils.motion.angleInterpolation("LShoulderPitch", 1.5, 5, True)


def stretch_both_arms():
    utils.text_to_speech.say("Now let's raise both arms to the sky!")
    utils.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [-0.5, -0.5], [5, 6], True)
    utils.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [1.5, 1.5], [5, 6], True)


def stretch_back():
    utils.text_to_speech.say("Now let's stretch the back slowly!")
    utils.motion.angleInterpolation("HipPitch", 0.2, 5, True)
    utils.motion.angleInterpolation("HipPitch", 0.0, 5, True)


def perform_stretching():
    utils.text_to_speech.say("Let's start the stretching session! Follow my movements.")
    utils.robot_posture.goToPosture("StandInit", 0.5)
    time.sleep(1)

    stretch_right_arm()
    time.sleep(5)
    
    stretch_left_arm()
    time.sleep(5)
    
    stretch_both_arms()
    time.sleep(5)
    
    stretch_back()
    time.sleep(5)

    utils.text_to_speech.say("Great job! The stretching session is over. Well done!")


def lock_head():
    utils.robot_posture.goToPosture("StandInit", 0.5)
    
    names = ["HeadYaw", "HeadPitch"]
    angles = [0.0, 0.0]
    fraction_max_speed = 0.2
    utils.motion.setAngles(names, angles, fraction_max_speed)
    
    utils.motion.setStiffnesses("Head", 1.0)
    
    
def unlock_head():
    utils.motion.setStiffnesses("Head", 0.0)


'''
# Function for Namaste pose
def pose_namaste(posture, motion):
    posture.goToPosture("Stand", 0.5)  # Initial standing position
    names = ["LShoulderPitch", "RShoulderPitch", "LElbowYaw", "RElbowYaw"]
    angles = [1.0, 1.0, 0.0, 0.0]  # Arms towards the chest
    motion.setAngles(names, angles, 0.2)
    # Keep hands joined (optional)
    motion.setAngles(["LWristYaw", "RWristYaw"], [-1.5, 1.5], 0.2)
    print("Namaste pose completed.")
    time.sleep(5)  # Hold the position for 5 seconds


# Function for Stand pose (arms down)
def pose_stand(posture, motion):
    posture.goToPosture("Stand", 0.5)
    motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [1.4, 1.4], 0.2)  # Arms down
    print("Stand pose completed.")
    time.sleep(5)


# Function for Meditation pose (arms raised and open)
def pose_meditation(posture, motion):
    posture.goToPosture("Stand", 0.5)
    names = ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"]
    angles = [0.5, 0.5, -0.2, 0.2]  # Arms raised and slightly open
    motion.setAngles(names, angles, 0.2)
    print("Meditation pose completed.")
    time.sleep(5)


# Function for Bowed pose (prayer with inclination)
def pose_bowed(posture, motion):
    posture.goToPosture("Stand", 0.5)
    motion.setAngles("HeadPitch", 0.3, 0.2)  # Slight head tilt
    names = ["LShoulderPitch", "RShoulderPitch", "LElbowYaw", "RElbowYaw"]
    angles = [1.0, 1.0, -0.5, 0.5]  # Hands joined and inclined
    motion.setAngles(names, angles, 0.2)
    motion.setAngles("TorsoPitch", 0.2, 0.1)  # Torso inclination
    print("Bowed pose completed.")
    time.sleep(5)

    
def pepper_meditation_sequence(ip, port):
    """
    Pepper performs a sequence of movements resembling meditation or yoga.
    """
    try:
        # Proxy per il controllo dei movimenti
        motion = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)

        # Porta Pepper nella posizione iniziale
        posture.goToPosture("StandInit", 0.5)

        # Abilita la rigidita' dei motori
        motion.setStiffnesses("Body", 1.0)

        # Movimenti della sequenza
        print("[INFO] Inizio sequenza di meditazione.")

        # Movimento 1: Alza le braccia sopra la testa
        motion.angleInterpolationWithSpeed(["LShoulderPitch", "RShoulderPitch"], [-0.5, -0.5], 0.2)
        time.sleep(1.5)

        # Movimento 2: Porta le mani unite davanti al petto (Namaste)
        motion.angleInterpolationWithSpeed(["LElbowYaw", "RElbowYaw"], [1.5, -1.5], 0.3)
        motion.angleInterpolationWithSpeed(["LElbowRoll", "RElbowRoll"], [-0.5, 0.5], 0.3)
        time.sleep(1.5)

        # Movimento 3: Apri le braccia lateralmente
        motion.angleInterpolationWithSpeed(["LShoulderRoll", "RShoulderRoll"], [0.3, -0.3], 0.3)
        time.sleep(1.5)

        # Movimento 4: Abbassa le braccia lentamente in avanti
        motion.angleInterpolationWithSpeed(["LShoulderPitch", "RShoulderPitch"], [1.0, 1.0], 0.2)
        time.sleep(1.5)

        # Movimento 5: Leggera inclinazione in avanti, come in un "bow"
        motion.angleInterpolationWithSpeed(["HipPitch"], [0.2], 0.2)
        time.sleep(1.5)

        # Ritorno alla posizione iniziale
        posture.goToPosture("StandInit", 0.5)

        # Disabilita la rigidita' dei motori
        motion.setStiffnesses("Body", 0.0)

        print("[INFO] Sequenza di meditazione completata.")

    except Exception as e:
        print("[ERRORE] Si e' verificato un problema:", e)
        

def pepper_ohm_pose(posture, motion):
    """
    Pepper performs a meditative 'Ohm' pose:
    - Step 1: Arms crossed on the chest
    - Step 2: Opens arms wide with fists closed
    """
    try:
        # Porta Pepper nella posizione iniziale
        posture.goToPosture("StandInit", 0.5)

        # Abilita la rigidita' dei motori
        motion.setStiffnesses("Body", 1.0)

        print("[INFO] Inizio posa 'Ohm'.")

        # Step 1: Incrocia le braccia sul petto
        motion.setAngles(
            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",  # Braccio destro
             "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"], # Braccio sinistro
            [1.0, 0.3, 0.0, 1.0,  # Posizione braccio destro
             1.0, -0.3, 0.0, -1.0],  # Posizione braccio sinistro
            0.2  # Velocita'
        )
        time.sleep(1.5)

        # Step 2: Apre le braccia lentamente e chiude le mani (gesto meditativo)
        motion.setAngles(
            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",  # Braccio destro
             "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"], # Braccio sinistro
            [0.5, -0.3, 0.0, 0.5, 0.0,  # Braccio destro (braccio aperto, polso neutro)
             0.5, 0.3, 0.0, -0.5, 0.0],  # Braccio sinistro (braccio aperto, polso neutro)
            0.2  # Velocita'
        )
        time.sleep(1.5)

        # Step 3: Chiudi i pugni per simulare una posizione meditativa
        motion.setAngles(["RHand", "LHand"], [0.0, 0.0], 0.2)  # 0.0 = pugno chiuso
        time.sleep(1.5)

        # Disabilita la rigidita' dei motori
        motion.setStiffnesses("Body", 0.0)

        print("[INFO] Posa 'Ohm' completata.")

    except Exception as e:
        print("[ERRORE] Si e' verificato un problema:", e)


def pepper_wave_hand(ip, port):
    """
    Pepper performs an exaggerated waving gesture.
    """
    try:
        # Proxy per il controllo dei movimenti
        motion = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)

        # Assicura che Pepper sia in posizione base
        posture.goToPosture("StandInit", 0.5)

        # Abilita il controllo motori
        motion.setStiffnesses("RArm", 1.0)

        # Definizione dei movimenti del saluto
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        times = [1.0, 2.0, 3.0]
        keys = [
            [0.0, -0.2, 0.2],  # Movimento su/giu' della spalla
            [-0.2, 0.2, -0.2], # Rotazione laterale per un gesto ampio
            [1.5, 1.2, 1.5],   # Yaw del gomito
            [0.5, 0.8, 0.5],   # Movimento del gomito per flessione ampia
            [1.0, 1.5, 1.0]    # Rotazione del polso per il saluto
        ]

        # Esegui il movimento
        motion.angleInterpolation(names, keys, times, True)

        # Ritorna alla posizione iniziale
        motion.rest()

    except Exception as e:
        print("[ERRORE] Si e' verificato un problema:", e)


def perform_meditation_pose_static(motion_service):
    print(" Eseguo la posa da meditazione (statica)...")

    # Nome dei giunti per la posa
    joint_names = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
        "HeadPitch"
    ]

    # Angoli per simulare rilassamento
    meditation_angles = [
        1.2, 0.3, -1.0, -0.6, 0.0,  # Braccio sinistro rilassato
        1.2, -0.3, 1.0, 0.6, 0.0,  # Braccio destro rilassato
        0.2  # Testa leggermente inclinata in avanti
    ]

    # Tempi per raggiungere la posizione
    times = [1.5] * len(joint_names)

    # Esegui i movimenti
    motion_service.angleInterpolation(joint_names, meditation_angles, times, True)
    print("Posa da meditazione completata!")


def pose_chinata(posture, motion):
    posture.goToPosture("Stand", 0.5)
    motion.setAngles("HeadPitch", 0.3, 0.2)  # Leggera inclinazione del capo
    names = ["LShoulderPitch", "RShoulderPitch", "LElbowYaw", "RElbowYaw"]
    angles = [1.0, 1.0, -0.5, 0.5]  # Mani giunte e inclinazione
    motion.setAngles(names, angles, 0.2)
    motion.setAngles("TorsoPitch", 0.2, 0.1)  # Inclinazione del busto
    print("Pose Chinata completata.")
    time.sleep(5)
'''
