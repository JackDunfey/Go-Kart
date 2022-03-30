from wpilib import Relay

# Untested code!!
# Assumes active-high
class Headlights:
    def __init__(self, operator_interface, relay_id, startOn=False):
        self.oi = operator_interface
        self.relay = Relay(relay_id)
        if startOn:
            self.on()
    def isOn(self):
        return self.relay.get() == Relay.Value.kOn
    def on(self):
        self.relay.set(Relay.Value.kOn)
    def off(self):
        self.relay.set(Relay.Value.kOff)
    def toggle(self):
        if self.isOn():
            self.off()
        else:
            self.on()

    def main(self):
        if self.oi.headlightsButtonPresed():
            self.toggle()