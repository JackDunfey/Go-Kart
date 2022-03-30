from ctre import *
import Wiring

class Chassis:
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

        self.cruising = False

        self.brake = TalonSRX(Wiring.BRAKE)
        self.brake.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)

        self.configDrivetrain()

    def engageBrake(self):
        self.braking = True

    def disengageBrake(self):
        self.braking = False

    def cruiseMain(self):
        if self.oi.setCruiseControlButton():
            self.cruising = True
            self.cruise_speed = self.get_speed()
        elif self.oi.releaseCruiseControlButton():
            self.cruising = False
    def main(self):
        if self.braking:
            self.brake.set(TalonSRXControlMode.PercentOutput, self.oi.getBrake())
        else:
            self.brake.set(TalonSRXControlMode.PercentOutput, 0)

        if self.oi.isBraking():
            self.engageBrake()
        else:
            self.disengageBrake()

        self.cruiseMain()
        ySpeed = self.oi.y()
        if self.cruising:
            ySpeed = self.cruise_speed
        self.set_speed(ySpeed)