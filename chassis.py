from ctre import *
from wpilib import Ultrasonic

import Wiring


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

    def get_speed(self):
        return ((self.falcon1.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon2.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon3.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon4.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon5.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
            ((self.falcon6.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) / 6

    def __init__(self, operator_interface):
        self.oi = operator_interface

        self.falcon1 = TalonFX(Wiring.TALON1)
        self.falcon2 = TalonFX(Wiring.TALON2)
        self.falcon3 = TalonFX(Wiring.TALON3)
        self.falcon4 = TalonFX(Wiring.TALON4)
        self.falcon5 = TalonFX(Wiring.TALON5)
        self.falcon6 = TalonFX(Wiring.TALON6)
        
        self.left = Chassis.MotorSet(self.falcon1, self.falcon2, self.falcon3)
        self.right = Chassis.MotorSet(self.falcon4, self.falcon5, self.falcon6)

        self.cruising = False
        self.safe_mode = True
        self.parking = True

        self.brake = TalonSRX(Wiring.BRAKE)
        self.brake.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)
        
        self.ultrasonic = Ultrasonic(Wiring.ULTRASONIC_1, Wiring.ULTRASONIC_2)
        self.ultrasonic.setAutomaticMode(True)

        self.configDrivetrain()

    def drive(self, ySpeed, rSpeed):
        self.left.set_speed(ySpeed - rSpeed)
        self.right.set_speed(ySpeed + rSpeed)

    def cruiseMain(self):
        if self.oi.setCruiseControlButton():
            self.cruising = True
            self.cruise_speed = self.get_speed()
        elif self.oi.releaseCruiseControlButton():
            self.cruising = False
    
    def main(self):
        # Parking
        if self.oi.parkingTogglePressed():
            self.parking = not self.parking
        if self.parking:
            self.braking = True
            self.brake.set(TalonFXControlMode.PercentOutput, 1)
            self.set_speed(0)
            return

        # Braking
        if self.oi.isBraking():
            self.braking = True
        else:
            self.braking = False
        if self.braking:
            self.brake.set(TalonSRXControlMode.PercentOutput, self.oi.getBrake())
        else:
            self.brake.set(TalonSRXControlMode.PercentOutput, 0)
        
        # Safety toggle
        if self.oi.safetyTogglePressed():
            self.safe_mode = not self.safe_mode

        # Driving
        self.cruiseMain()
        ySpeed = self.oi.y()
        rSpeed = self.oi.x()
        if self.cruising:
            ySpeed = self.cruise_speed
        if self.safe_mode and ySpeed > Chassis.MAX_SAFE_OUTPUT:
            ySpeed = Chassis.MAX_SAFE_OUTPUT
        if not self.braking:
            if self.ultrasonic.getRange() < 36 and self.get_speed() > Chassis.MAX_SAFE_OUTPUT: # Idk what default is or what the ultrasonic units are (I think inches)
                self.parking = True
            else:
                self.drive(ySpeed, rSpeed)
        else:
            self.drive(0,0)
