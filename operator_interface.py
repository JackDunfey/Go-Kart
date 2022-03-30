from wpilib import XboxController

import Wiring

class Operator_Interface:
    """
    * brake = lt
    * parking = start button
    * safety_mode = right joystick button

    * cruise control set = RB
    * cruise control exit = LB

    * driving = left joystick y
    * steering = right joystick x

    * headlights = y button
    * horn = a button
    """
    def __init__(self):
        self.pilot = XboxController(Wiring.PILOT_PORT)
    
    def getBrake(self):
        return self.pilot.getLeftTriggerAxis()
    
    def isBraking(self):
        return self.getBrake() > 0.1
    
    def y(self):
        return self.pilot.getLeftY()

    def x(self):
        return self.pilot.getRightX()
    
    def setCruiseControlButton(self):
        return self.pilot.getRightBumper()

    def setCruiseControlButtonPressed(self):
        return self.pilot.getRightBumperPressed()

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
        return self.pilot.getStartButton()
    
    def parkingTogglePressed(self):
        return self.pilot.getStartButtonPressed()

    def headlightsButton(self):
        return self.pilot.getYButton()

    def headlightsButtonPresed(self):
        return self.pilot.getYButtonPressed()