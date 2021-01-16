#A video of the example: https://www.youtube.com/watch?v=cxDJ34ofeHk
from spike import ForceSensor
from spike import PrimeHub
myHub = PrimeHub()
mySensor = colorDistanceSensor("F", 7)
#You can use the following commands to send PF commands:
#PFComboDirectCommand, PFSingleOutputCommand and PFComboPWMCommand
force = ForceSensor('E')

#This example "spams" the sensor with commands. It would be better to send each command only once or twice (see second PF example)!
while True:
    if force.is_pressed():
        mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.BACKWARD, PFMotor.FORWARD)
    elif myHub.left_button.is_pressed():
        mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.BACKWARD, PFMotor.BACKWARD)
    elif myHub.right_button.is_pressed():
        mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.FORWARD, PFMotor.FORWARD)
    else:
        mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.FLOAT, PFMotor.FLOAT)
    utime.sleep_ms(75)
