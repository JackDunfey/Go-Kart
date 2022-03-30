from turtle import speed
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
    WIDTH, HEIGHT = 1920//2, 1080//2
    
    def __init__(self):
        self.oi = Operator_Interface()
        self.chassis = Chassis(self.oi)
        self.PDM = PowerDistribution(Wiring.PDM, PowerDistribution.ModuleType.kRev)
        self.headlights = Headlights(self.oi, Wiring.HEADLIGHT_RELAY)

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
        frame = np.zeros(shape=(Robot.HEIGHT, Robot.WIDTH, 3))

        # Display text
        texts = [f"Parking Brake: {self.chassis.parking}", f"Cruising @ {self.chassis.get_speed_mph()} MPH" if self.chassis.cruising else "Not cruising"]
        y = 0
        for text in texts:
            (w, h), _ = cv2.getTextSize(text, Robot.font, 1, 1)
            y += 2*(h+Robot.TEXT_PADDING) # May need to be adjusted after font correction
            cv2.putText(frame, text, (0, y), Robot.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Speedometer
        HEADING_SIZE = 5
        speed_str = str(int(self.chassis.get_speed_mph())) + " MPH"
        (w, h), _ = cv2.getTextSize(speed_str, Robot.font, HEADING_SIZE, HEADING_SIZE)
        cv2.putText(frame, speed_str, ((Robot.WIDTH-w)//2, (Robot.HEIGHT+h)//2), Robot.font, HEADING_SIZE, (255, 255, 255), HEADING_SIZE, cv2.LINE_AA)

        # Safe mode indicator
        r = 100
        cv2.rectangle(frame, (Robot.WIDTH - r, 0), (Robot.WIDTH, r), (0, 255, 0) if not self.chassis.safe_mode else (0, 255, 255), -1)

        # Display output
        cv2.imshow("Speedometer", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    try:
        robot = Robot()
        robot.main()
    except KeyboardInterrupt:
        exit(0)