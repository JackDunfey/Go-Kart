from wpilib import XboxController

import Wiring

class operator_interface:
    def __init__(self):
        self.pilot = XboxController(Wiring.PILOT_PORT)
    
    def getBrake(self):
        return self.pilot.getLeftTriggerAxis()
    
    def isBraking(self):
        return self.getBrake() > 0.25
    
    def y(self):
        return self.pilot.getLeftY()
    
    def setCruiseControlButton(self):
        return self.pilot.getRightBumper()

    def releaseCruiseControlButton(self):
        return self.pilot.getLeftBumper()