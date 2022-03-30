class Brake:
    def __init__(self, operator_interface, actuator_id, engaged=True):
        self.oi = operator_interface
        self.id = actuator_id
        self.brake = TalonSRX(actuator_id)
        self.brake.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)
        self.engaged = engaged
    def engage(selfs):
        self.engaged = True
    def disengage(self):
        self.engaged = False
    def main(self):
        if self.oi.isBraking():
            self.engage()
        else:
            self.disengage()
        if self.brake.engaged:
            self.brake.set(TalonSRXControlMode.PercentOutput, self.oi.getBrake())
        else:
            self.brake.set(TalonSRXControlMode.PercentOutput, 0)