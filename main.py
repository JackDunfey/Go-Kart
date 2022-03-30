from ctre import *
import cv2
import numpy as np
from wpilib import PowerDistribution

from operator_interface import Operator_Interface
from chassis import Chassis
import Wiring

class Robot:
    TEXT_PADDING = 5
    
    def __init__(self):
        self.oi = Operator_Interface()
        self.chassis = Chassis(self.oi)
        self.PDM = PowerDistribution(Wiring.PDM, PowerDistribution.ModuleType.kRev)

    def main(self):
        while True:
            # Dashboard
            self.updateDisplay()
            # Driving
            self.chassis.main()
            # Horn
            if self.oi.hornButton():
                self.PDM.setSwitchableChannel(True)
            else:
                self.PDM.setSwitchableChannel(False)

    def updateDisplay(self):
        speed = str(int(self.chassis.get_speed() + 0.5)) + " MPH"
        frame = np.zeros(shape=(1920, 1080, 3))
        texts = [speed, f"Parking Brake: {self.chassis.parking}"]
        prev_y = 0
        for text in texts:
            w, h = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            prev_y += 2*(h+Robot.TEXT_PADDING)
            cv2.putText(frame, text, (0,prev_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Speedometer", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except KeyboardInterrupt:
        exit(0)