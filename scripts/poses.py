import time

class Poses:
    """
    A class that encapsulates various movement poses and animations for Pepper robot.
    Handles all physical movements including dances, gestures, and posture control.
    """
    
    def __init__(self, motion, robot_posture, text_to_speech):
        """
        Initialize the Poses class with required NAOqi modules.
        
        Args:
            motion: ALMotion service for controlling robot movements
            robot_posture: ALRobotPosture service for posture control
            text_to_speech: ALTextToSpeech service for voice output
        """
        self.motion = motion
        self.robot_posture = robot_posture
        self.text_to_speech = text_to_speech

    def bye(self):
        """
        Executes a waving goodbye animation sequence.
        Movement sequence:
            1. Raises arm to wave position
            2. Performs 3 waving motions
            3. Returns arm to rest position
        """
        try:
            # Define joints involved in the wave motion
            joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            
            # Arm positions for different wave phases
            wave_up = [0.5, -0.2, 1.0, 1.5, 0.0]  # Arm raised for waving
            wave_down = [0.5, -0.2, 1.0, 0.8, 0.0]  # Arm lowered slightly
            rest_position = [1.4, -0.2, 1.3, 0.3, 0.0]  # Neutral rest position
            
            # Time intervals for each movement (in seconds)
            times = [1.0, 1.0, 1.0, 1.0, 1.0]

            # Execute the wave sequence
            self.motion.angleInterpolation(joint_names, wave_up, times, True)
            
            # Perform 3 wave cycles
            for _ in range(3):
                self.motion.angleInterpolation(joint_names, wave_down, times, True)
                self.motion.angleInterpolation(joint_names, wave_up, times, True)
            
            # Return to rest position
            self.motion.angleInterpolation(joint_names, rest_position, times, True)

        except Exception as e:
            print("[Error] Error during movement execution: " + str(e))

    def perform_meditation_pose(self):
        """
        Guides Pepper through a meditation pose sequence:
            1. Starts from initial position
            2. Moves to meditation pose
            3. Holds pose for 5 seconds
        """
        print("[INFO] Starting meditation and relaxation pose...\n")

        # All joints that will be moved
        joint_names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
            "HeadYaw", "HeadPitch", "HipRoll", "HipPitch"
        ]

        # Position definitions
        initial_pose = [1.4, 0.0, -0.3, -0.5, 1.4, 0.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0]
        meditation_pose = [0.8, 0.4, -1.0, -0.4, 0.8, -0.4, 1.0, 0.4, 0.0, 0.2, 0.0, -0.1]

        # Movement timing (3 seconds for transition, 5 seconds hold)
        times = [3.0] * len(joint_names)
        
        # Execute pose sequence
        self.motion.angleInterpolation(joint_names, initial_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, [5.0] * len(joint_names), True)

        print("[INFO] Meditation pose completed!\n")

    def move_arms_in_wave(self):
        """
        Creates a wave-like motion with both arms moving in opposition.
        Each arm moves through 3 positions over 3 seconds.
        """
        print("[INFO] Wave movement with arms...\n")
        
        # Joints to control
        names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
        ]

        # Angle sequences for each joint (3 positions each)
        angles_list = [
            [0.0, -0.5, 0.0],  # LShoulderPitch
            [0.2, 0.5, 0.2],     # LShoulderRoll
            [-1.0, -0.8, -1.0],  # LElbowYaw
            [-0.5, -0.3, -0.5],  # LElbowRoll
            [0.0, 0.5, 0.0],     # RShoulderPitch
            [-0.2, -0.5, -0.2],   # RShoulderRoll
            [1.0, 0.8, 1.0],      # RElbowYaw
            [0.5, 0.3, 0.5]       # RElbowRoll
        ]

        # Timing for each movement phase
        times = [
            [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0],
            [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]
        ]

        # Execute the movement
        self.motion.angleInterpolation(names, angles_list, times, True)

    def spin_torso(self):
        """Rotates the torso side to side in a smooth motion."""
        print("[INFO] Rotating torso...\n")
        
        names = ["HipRoll", "HipPitch"]
        
        angles_list = [
            [0.0, -0.5, 0.0],  # HipRoll positions
            [0.2, 0.5, 0.2]     # HipPitch positions
        ]

        times = [
            [1.0, 2.0, 3.0],  # HipRoll timing
            [1.0, 2.0, 3.0]    # HipPitch timing
        ]

        self.motion.angleInterpolation(names, angles_list, times, True)

    def step_side_to_side(self):
        """Makes Pepper shift weight from side to side."""
        print("[INFO] Side step...\n")
        
        names = ["HipPitch"]
        angles_list = [[0.0, -0.5, 0.0]]  # Forward/backward motion
        times = [[1.0, 2.0, 3.0]]

        self.motion.angleInterpolation(names, angles_list, times, True)

    def nod_head(self):
        """Makes Pepper nod its head up and down."""
        print("[INFO] Head movement...\n")
        
        names = ["HeadPitch", "HeadYaw"]
        angles_list = [
            [0.0, -0.5, 0.0],  # Head nod (pitch)
            [0.2, 0.5, 0.2]     # Head turn (yaw)
        ]
        times = [
            [1.0, 2.0, 3.0],  # Pitch timing
            [1.0, 2.0, 3.0]    # Yaw timing
        ]

        self.motion.angleInterpolation(names, angles_list, times, True)

    def perform_techno_dance(self):
        """
        Executes a techno dance routine consisting of:
            - Arm waves
            - Torso spins
            - Side steps
            - Head nods
        Repeated twice with a final flourish.
        """
        print("[INFO] Starting dance routine...\n")

        # Dance sequence repeated twice
        for _ in range(2):
            self.move_arms_in_wave()
            self.spin_torso()
            self.step_side_to_side()
            self.nod_head()
        
        # Final movements
        self.move_arms_in_wave()
        self.spin_torso()

        print("[INFO] Dance routine completed!\n")

    def perform_rock_dance(self):
        """
        Simulates playing air guitar with dynamic arm movements.
        Cycles through 4 different guitar playing positions 16 times.
        """
        print("[INFO] Starting guitar simulation...\n")

        # All joints involved in guitar playing motion
        joint_names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", 
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", 
            "HipRoll", "HipPitch", "HeadYaw", "HeadPitch"
        ]

        # Four different guitar playing positions
        guitar_moves = [
            [1.0, 0.5, -1.0, -0.5, 1.5, -0.3, 0.8, 1.0, 0.0, -0.2, 0.0, 0.3],  # Position 1
            [1.0, 0.5, -1.2, -0.7, 1.3, -0.5, 1.0, 1.2, 0.2, -0.2, 0.0, 0.5],  # Position 2
            [1.2, 0.6, -1.3, -0.8, 1.4, -0.4, 1.1, 1.3, 0.0, -0.2, 0.1, 0.4],  # Position 3
            [0.8, 0.4, -0.9, -0.6, 1.0, -0.5, 1.2, 0.8, 0.2, -0.3, 0.1, 0.3]   # Position 4
        ]

        # Fast transitions between positions (0.5 seconds each)
        times = [0.5] * len(joint_names)
        
        # Repeat the sequence 16 times for a complete performance
        for _ in range(16):
            for move in guitar_moves:
                self.motion.angleInterpolation(joint_names, move, times, True)

        print("[INFO] Guitar simulation complete!\n")

    def perform_classic_dance(self):
        """
        Executes a classic dance routine with elegant arm movements.
        Cycles through 8 different dance positions 8 times.
        """
        print("[INFO] Pepper's dance starting...\n")

        # Joints used in the dance
        joint_names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
        ]

        # Eight different dance positions
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

        # Smooth transitions between positions
        times = [0.5] * len(joint_names)

        # Repeat the sequence 8 times
        for _ in range(8):
            for move in dance_moves:
                self.motion.angleInterpolation(joint_names, move, times, True)

        print("[INFO] Dance completed!\n")

    def stretch_right_arm(self):
        """Raises and lowers the right arm in a stretching motion."""
        self.text_to_speech.say("Let's raise the right arm to the sky!")
        self.motion.angleInterpolation("RShoulderPitch", -0.5, 6, True)  # Raise arm
        self.motion.angleInterpolation("RShoulderPitch", 1.5, 6, True)   # Lower arm

    def stretch_left_arm(self):
        """Raises and lowers the left arm in a stretching motion."""
        self.text_to_speech.say("Now let's raise the left arm to the sky!")
        self.motion.angleInterpolation("LShoulderPitch", -0.5, 5, True)  # Raise arm
        self.motion.angleInterpolation("LShoulderPitch", 1.5, 5, True)   # Lower arm

    def stretch_both_arms(self):
        """Raises and lowers both arms simultaneously for stretching."""
        self.text_to_speech.say("Now let's raise both arms to the sky!")
        self.motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"], 
            [-0.5, -0.5],  # Both arms up
            [5, 6],  # Movement durations
            True
        )
        self.motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"], 
            [1.5, 1.5],  # Both arms down
            [5, 6], 
            True
        )

    def stretch_back(self):
        """Performs a gentle back stretch by adjusting hip pitch."""
        self.text_to_speech.say("Now let's stretch the back slowly!")
        self.motion.angleInterpolation("HipPitch", 0.2, 5, True)  # Lean back slightly
        self.motion.angleInterpolation("HipPitch", 0.0, 5, True)  # Return to neutral

    def perform_stretching(self):
        """
        Guides through a complete stretching routine:
            1. Right arm stretch
            2. Left arm stretch
            3. Both arms stretch
            4. Back stretch
        Includes verbal instructions and pauses between stretches.
        """
        self.text_to_speech.say("Let's start the stretching session! Follow my movements.")
        self.robot_posture.goToPosture("StandInit", 0.5)  # Start from standing position
        time.sleep(1)

        # Execute each stretch with pauses
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
        """
        Locks Pepper's head in a stable position for recording or focused interaction.
        Sets head joints to neutral position and increases stiffness.
        """
        self.robot_posture.goToPosture("StandInit", 0.5)  # Ensure standing posture
        
        names = ["HeadYaw", "HeadPitch"]
        angles = [0.0, 0.0]  # Neutral head position
        fraction_max_speed = 0.2  # Moderate speed for smooth movement
        self.motion.setAngles(names, angles, fraction_max_speed)
        
        self.motion.setStiffnesses("Head", 1.0)  # Maximum stiffness to prevent movement
        
    def unlock_head(self):
        """Releases head stiffness allowing natural movement."""
        self.motion.setStiffnesses("Head", 0.0)  # Zero stiffness allows free movement