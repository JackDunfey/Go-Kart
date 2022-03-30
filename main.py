from ctre import *
import cv2
import numpy as np
from wpilib import Solenoid

import operator_interface
import Chassis

def updateDisplay(speed=0):
    text = str(speed) + " MPH"
    frame = np.zeros(shape=(1920, 1080, 3))
    cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 2)
    cv2.imshow("Speedometer", frame)

class Robot:
    def __init__(self):
        self.configDrivetrain()
        self.oi = operator_interface()
        self.chassis = Chassis()

    def main(self):
        while True:
            updateDisplay(speed=int(self.get_speed() + 0.5))
            self.chassis.main()

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
