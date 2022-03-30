from ctre import *

import Wiring
from brake import Brake

class Chassis:
    MAX_SAFE_OUTPUT = 0.25 # ~ 10 mph

    class MotorSet:
        def __init__(self, *motor_list):
            self.motors = []
            for motor in motor_list:
                self.motors += [motor]
        def set_speed(self, speed, control_mode=TalonFXControlMode.PercentOutput):
            for motor in self.motors:
                motor.set(control_mode, speed)

    def configMotor(self,motor):
        # TODO: May want to add a ramprate
        motor.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)

    def configDrivetrain(self):
        self.configMotor(self.falcon1)
        self.configMotor(self.falcon2)
        self.configMotor(self.falcon3)
        self.configMotor(self.falcon4)
        self.configMotor(self.falcon5)
        self.configMotor(self.falcon6)

    def set_speed(self, speed, control_mode=TalonFXControlMode.PercentOutput):
        self.falcon1.set(control_mode, speed)
        self.falcon2.set(control_mode, speed)
        self.falcon3.set(control_mode, speed)
        self.falcon4.set(control_mode, speed)
        self.falcon5.set(control_mode, speed)
        self.falcon6.set(control_mode, speed)

    def get_speed_mph(self):
        return ((self.falcon1.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon2.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon3.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon4.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon5.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon6.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) / 6

    def __init__(self, operator_interface, cruising=False, safe_mode=True, parking=True):
        self.oi = operator_interface

        self.falcon1 = TalonFX(Wiring.TALON1)
        self.falcon2 = TalonFX(Wiring.TALON2)
        self.falcon3 = TalonFX(Wiring.TALON3)
        self.falcon4 = TalonFX(Wiring.TALON4)
        self.falcon5 = TalonFX(Wiring.TALON5)
        self.falcon6 = TalonFX(Wiring.TALON6)
        
        self.left = Chassis.MotorSet(self.falcon1, self.falcon2, self.falcon3)
        self.right = Chassis.MotorSet(self.falcon4, self.falcon5, self.falcon6)

        self.cruising = cruising
        self.safe_mode = safe_mode
        self.parking = parking

        self.brake = Brake(self.oi, Wiring.BRAKE, engaged=self.parking)

        self.configDrivetrain()

    def drive(self, ySpeed, rSpeed):
        self.left.set_speed(ySpeed - rSpeed)
        self.right.set_speed(ySpeed + rSpeed)

    def enterCruise(self):
        self.cruising = True

    def exitCruise(self):
        self.cruising = False

    def cruiseMain(self):
        # Cruise control will need to be updated if MotorSafety still exists in python
        if self.oi.setCruiseControlButtonPressed():
            self.enterCruise()
        elif self.oi.exitCruiseControlButton():
            self.exitCruise()
    
    def main(self):
        # Parking
        if self.oi.parkingTogglePressed():
            self.parking = not self.parking
        if self.parking:
            self.cruising = False
            self.set_speed(0)
            self.brake.engage()
            return

        # Braking
        self.brake.main(self.oi)
        
        # Safety toggle
        if self.oi.safetyTogglePressed():
            self.safe_mode = not self.safe_mode
            if self.safety_mode and self.cruising and self.get_speed_mph > Chassis.MAX_SAFE_OUTPUT * Chassis.MAX_SPEED:
                self.exitCruise()

        # Driving
        self.cruiseMain()
        ySpeed = self.oi.y()
        rSpeed = self.oi.x()
        if self.cruising:
            # If MotorSafety complains, I will need to command Motors to the velocity they were at when cruise speed was set
            return
        if self.safe_mode and ySpeed > Chassis.MAX_SAFE_OUTPUT:
            ySpeed = Chassis.MAX_SAFE_OUTPUT
        if not self.braking:
            self.drive(ySpeed, rSpeed)
        else:
            self.drive(0,0)
