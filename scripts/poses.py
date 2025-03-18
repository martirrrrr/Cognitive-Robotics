class Poses:
    def __init__(self, motion, robot_posture, text_to_speech):
        # Initialize the Poses class with motion, posture, and speech control modules
        self.motion = motion
        self.robot_posture = robot_posture
        self.text_to_speech = text_to_speech

    def bye(self):
        """Perform a waving gesture with the right arm to say goodbye."""
        try:
            # Define joint names for the right arm
            joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            
            # Define joint angles for the wave-up and wave-down positions
            wave_up = [0.5, -0.2, 1.0, 1.5, 0.0]
            wave_down = [0.5, -0.2, 1.0, 0.8, 0.0]
            
            # Define the timing for movement execution
            times = [1.0] * len(joint_names)
            
            # Move arm to wave-up position
            self.motion.angleInterpolation(joint_names, wave_up, times, True)
            
            # Perform three wave movements (up and down)
            for _ in range(3):
                self.motion.angleInterpolation(joint_names, wave_down, times, True)
                self.motion.angleInterpolation(joint_names, wave_up, times, True)
            
            # Return arm to resting position
            rest_position = [1.4, -0.2, 1.3, 0.3, 0.0]
            self.motion.angleInterpolation(joint_names, rest_position, times, True)
        
        except Exception as e:
            print("[Error] Error during movement execution: " + str(e))
    
    def perform_meditation_pose(self):
        """Moves the robot into a meditation and relaxation pose."""
        print("[INFO] Starting meditation and relaxation pose...\n")
        
        # Define joint names for upper body and hips
        joint_names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
            "HeadYaw", "HeadPitch", "HipRoll", "HipPitch"
        ]
        
        # Define joint angles for initial and meditation poses
        initial_pose = [1.4, 0.0, -0.3, -0.5, 1.4, 0.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0]
        meditation_pose = [0.8, 0.4, -1.0, -0.4, 0.8, -0.4, 1.0, 0.4, 0.0, 0.2, 0.0, -0.1]
        
        # Define time durations for movements
        times = [3.0] * len(joint_names)
        
        # Transition into meditation pose
        self.motion.angleInterpolation(joint_names, initial_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, times, True)
        self.motion.angleInterpolation(joint_names, meditation_pose, [5.0] * len(joint_names), True)
        
        print("[INFO] Meditation pose completed!\n")
    
    def move_arms_in_wave(self):
        """Moves both arms in a wave-like motion."""
        print("[INFO] Wave movement with arms...\n")
        
        # Define joint names for arms
        names = [
            "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
            "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"
        ]
        
        # Define a sequence of angle movements to simulate a wave
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
        
        # Define the time duration for each motion step
        times = [[1.0, 2.0, 3.0]] * len(names)
        
        # Perform the wave motion
        self.motion.angleInterpolation(names, angles_list, times, True)
    
    def spin_torso(self):
        """Rotates the robot's torso."""
        print("[INFO] Rotating torso...\n")
        
        # Define joint names for torso movement
        names = ["HipRoll", "HipPitch"]
        
        # Define the angle sequence for torso spinning
        angles_list = [
            [0.0, -0.5, 0.0],
            [0.2, 0.5, 0.2]
        ]
        
        # Define the time duration for each movement
        times = [[1.0, 2.0, 3.0]] * len(names)
        
        # Execute torso rotation
        self.motion.angleInterpolation(names, angles_list, times, True)
    
    def nod_head(self):
        """Performs a nodding head motion."""
        print("[INFO] Head movement...\n")
        
        names = ["HeadPitch", "HeadYaw"]
        
        angles_list = [
            [0.0, -0.5, 0.0],
            [0.2, 0.5, 0.2]
        ]
        
        times = [[1.0, 2.0, 3.0]] * len(names)
        
        self.motion.angleInterpolation(names, angles_list, times, True)
    
    def perform_techno_dance(self):
        """Executes a techno dance routine combining different movements."""
        print("[INFO] Starting dance routine...\n")
        
        for _ in range(2):
            self.move_arms_in_wave()
            self.spin_torso()
            self.nod_head()
        self.move_arms_in_wave()
        self.spin_torso()
        
        print("[INFO] Dance routine completed!\n")

    def lock_head(self):
        """Locks the head in a fixed position."""
        self.robot_posture.goToPosture("StandInit", 0.5)
        self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.2)
        self.motion.setStiffnesses("Head", 1.0)
        
    def unlock_head(self):
        """Unlocks the head allowing it to move freely."""
        self.motion.setStiffnesses("Head", 0.0)
