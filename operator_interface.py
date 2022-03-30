from wpilib import XboxController

import Wiring

class Operator_Interface:
    def __init__(self):
        self.pilot = XboxController(Wiring.PILOT_PORT)
    
    def getBrake(self):
        return self.pilot.getLeftTriggerAxis()
    
    def isBraking(self):
        return self.getBrake() > 0.25
    
    def y(self):
        return self.pilot.getLeftY()

    def x(self):
        return self.pilot.getLeftX()
    
    def setCruiseControlButton(self):
        return self.pilot.getRightBumper()

    def exitCruiseControlButton(self):
        return self.pilot.getLeftBumper()

    def hornButton(self):
        return self.pilot.getAButton()
    
    def hornButtonPressed(self):
        return self.pilot.getAButton()

    def safetyToggle(self):
        return self.pilot.getRightStickButton()
    
    def safetyTogglePressed(self):
        return self.pilot.getRightStickButtonPressed()

    def parkingToggle(self):
        return self.pilot.getLeftStickButton()
    
    def parkingTogglePressed(self):
        return self.pilot.getLeftStickButtonPressed()

    def headlightsButton(self):
        return self.pilot.getYButton()

    def headlightsButtonPresed(self):
        return self.pilot.getYButtonPressed()