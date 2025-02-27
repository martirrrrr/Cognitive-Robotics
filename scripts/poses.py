import time

class Poses:
    def __init__(self, motion, robot_posture, text_to_speech):
        self.motion = motion
        self.robot_posture = robot_posture
        self.text_to_speech = text_to_speech

    def bye(self):
        try:
            joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

            wave_up = [0.5, -0.2, 1.0, 1.5, 0.0]
            
            wave_down = [0.5, -0.2, 1.0, 0.8, 0.0]

            times = [1.0, 1.0, 1.0, 1.0, 1.0]

            self.motion.angleInterpolation(joint_names, wave_up, times, True)

            for _ in range(3):
                self.motion.angleInterpolation(joint_names, wave_down, times, True)
                self.motion.angleInterpolation(joint_names, wave_up, times, True)

            
            rest_position = [1.4, -0.2, 1.3, 0.3, 0.0]
            self.motion.angleInterpolation(joint_names, rest_position, times, True)

        except Exception as e:
            print("[Error] Error during movement execution: " + str(e))

    def perform_meditation_pose(self):
        print("[INFO] Starting meditation and relaxation pose...\n")

        joint_names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
            "HeadYaw", "HeadPitch", "HipRoll", "HipPitch"
        ]

        
        initial_pose = [1.4, 0.0, -0.3, -0.5, 1.4, 0.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0]

        meditation_pose = [0.8, 0.4, -1.0, -0.4, 0.8, -0.4, 1.0, 0.4, 0.0, 0.2, 0.0, -0.1]

        times = [3.0] * len(joint_names)

        
        self.motion.angleInterpolation(joint_names, initial_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, [5.0] * len(joint_names), True)

        print("[INFO] Meditation pose completed!\n")

    def move_arms_in_wave(self):
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

        self.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)

    def spin_torso(self):
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

        self.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)


    def step_side_to_side(self):
        print("[INFO] Side step...\n")
        
        names = ["HipPitch"]
        
        angles_list = [
            [0.0, -0.5, 0.0]
        ]

        times = [
            [1.0, 2.0, 3.0]
        ]

        self.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)

    def nod_head(self):
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

        self.motion.angleInterpolation(names, [a for a in angles_list], [t for t in times], True)

    def perform_techno_dance(self):
        print("[INFO] Starting dance routine...\n")

        for _ in range(2):
            self.move_arms_in_wave()
            self.spin_torso()
            self.step_side_to_side()
            self.nod_head()
        self.move_arms_in_wave()
        self.spin_torso()

        print("[INFO] Dance routine completed!\n")

    def perform_rock_dance(self):

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
                self.motion.angleInterpolation(joint_names, move, times, True)

        print("[INFO] Guitar simulation complete!\n")

    def perform_classic_dance(self):
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
                self.motion.angleInterpolation(joint_names, move, times, True)

        print("[INFO] Dance completed!\n")

    def stretch_right_arm(self):
        self.text_to_speech.say("Let's raise the right arm to the sky!")
        self.motion.angleInterpolation("RShoulderPitch", -0.5, 6, True)
        self.motion.angleInterpolation("RShoulderPitch", 1.5, 6, True)

    def stretch_left_arm(self):
        self.text_to_speech.say("Now let's raise the left arm to the sky!")
        self.motion.angleInterpolation("LShoulderPitch", -0.5, 5, True)
        self.motion.angleInterpolation("LShoulderPitch", 1.5, 5, True)

    def stretch_both_arms(self):
        self.text_to_speech.say("Now let's raise both arms to the sky!")
        self.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [-0.5, -0.5], [5, 6], True)
        self.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [1.5, 1.5], [5, 6], True)

    def stretch_back(self):
        self.text_to_speech.say("Now let's stretch the back slowly!")
        self.motion.angleInterpolation("HipPitch", 0.2, 5, True)
        self.motion.angleInterpolation("HipPitch", 0.0, 5, True)

    def perform_stretching(self):
        self.text_to_speech.say("Let's start the stretching session! Follow my movements.")
        self.robot_posture.goToPosture("StandInit", 0.5)
        time.sleep(1)

        self.stretch_right_arm()
        time.sleep(5)
        
        self.stretch_left_arm()
        time.sleep(5)
        
        self.stretch_both_arms()
        time.sleep(5)
        
        self.stretch_back()
        time.sleep(5)

        self.text_to_speech.say("Great job! The stretching session is over. Well done!")

    def lock_head(self):
        self.robot_posture.goToPosture("StandInit", 0.5)
        
        names = ["HeadYaw", "HeadPitch"]
        angles = [0.0, 0.0]
        fraction_max_speed = 0.2
        self.motion.setAngles(names, angles, fraction_max_speed)
        
        self.motion.setStiffnesses("Head", 1.0)
        
    def unlock_head(self):
        self.motion.setStiffnesses("Head", 0.0)
