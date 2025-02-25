import time
import utils


def stretch_right_arm():
    utils.text_to_speech.say("Alziamo il braccio destro verso il cielo!")
    utils.motion.angleInterpolation("RShoulderPitch", -0.5, 5, True)
    utils.motion.angleInterpolation("RShoulderPitch", 1.5, 5, True)

def stretch_left_arm():
    utils.text_to_speech.say("Adesso alziamo il braccio sinistro verso il cielo!")
    utils.motion.angleInterpolation("LShoulderPitch", -0.5, 5, True)
    utils.motion.angleInterpolation("LShoulderPitch", 1.5, 5, True)


def stretch_both_arms():
    utils.text_to_speech.say("Adesso alziamo entrambe le braccia verso il cielo!")
    utils.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [-0.5, -0.5], [5, 5], True)
    utils.motion.angleInterpolation(["LShoulderPitch", "RShoulderPitch"], [1.5, 1.5], [5, 5], True)


def stretch_back():
    utils.text_to_speech.say("Adesso distendiamo la schiena lentamente!")
    utils.motion.angleInterpolation("HipPitch", 0.2, 5, True)
    utils.motion.angleInterpolation("HipPitch", 0.0, 5, True)


def main():
    utils.text_to_speech.say("Iniziamo la sessione di stretching! Segui i miei movimenti.")
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

    utils.text_to_speech_service.say("Ottimo lavoro! La sessione di stretching e' finita. Complimenti!")

