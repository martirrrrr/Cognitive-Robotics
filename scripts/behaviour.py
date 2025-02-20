import happy
import neutral
import angry
import sad
import poses
import record
import utils


def main():
    utils.motion.setAngles(["HeadYaw", "HeadPitch"], [1.0, 1.0], 0.1)
    # utils.motion.setStiffnesses("Head", 0.0)    
    # neutral.main()
    # happy.main()
    # angry.main()
    # sad.main()
  
main()


