from ctre import *
import cv2
import numpy as np
from wpilib import PowerDistribution

from operator_interface import Operator_Interface
from chassis import Chassis
from headlights import Headlights
import Wiring

class Robot:
    TEXT_PADDING = 5
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    def __init__(self):
        self.oi = Operator_Interface()
        self.chassis = Chassis(self.oi)
        self.PDM = PowerDistribution(Wiring.PDM, PowerDistribution.ModuleType.kRev)
        self.headlights = Headlights(Wiring.HEADLIGHT_RELAY)

    def main(self):
        # Dashboard
        self.updateDisplay()
        # Driving
        self.chassis.main()
        self.headlights.main()
        # Horn
        if self.oi.hornButton():
            self.PDM.setSwitchableChannel(True)
        else:
            self.PDM.setSwitchableChannel(False)

    def updateDisplay(self):
        frame = np.zeros(shape=(1920, 1080, 3))
        texts = [spstr(int(self.chassis.get_speed() + 0.5)) + " MPH"eed, f"Parking Brake: {self.chassis.parking}", f"Cruising @ {self.cruise_speed} MPH" if self.cruising else "Not cruising"]
        y = 0
        for text in texts:
            w, h = cv2.getTextSize(text, Robot.font, 1, 1)
            y += 2*(h+Robot.TEXT_PADDING)
            cv2.putText(frame, text, (0, y), Robot.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Speedometer", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except KeyboardInterrupt:
        exit(0)