from ctre import *
import cv2
import numpy as np
from wpilib import PowerDistribution

from operator_interface import Operator_Interface
from chassis import Chassis
import Wiring

TEXT_PADDING = 5

def updateDisplay(speed=0):
    text = str(speed) + " MPH"
    frame = np.zeros(shape=(1920, 1080, 3))
    text_w, text_h = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
    cv2.putText(frame, text, (0,2*(text_h+TEXT_PADDING)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Speedometer", frame)
    cv2.waitKey(1)

class Robot:
    def __init__(self):
        self.oi = Operator_Interface()
        self.chassis = Chassis(self.oi)
        self.PDM = PowerDistribution(Wiring.PDP, PowerDistribution.ModuleType.kRev)

    def main(self):
        while True:
            updateDisplay(speed=int(self.chassis.get_speed() + 0.5))
            self.chassis.main()
            if self.oi.hornButton():
                self.PDM.setSwitchableChannel(True)
            else:
                self.PDM.setSwitchableChannel(False)

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except KeyboardInterrupt:
        exit(0)