#A video of the example: https://www.youtube.com/watch?v=cxDJ34ofeHk
from spike import ForceSensor
from spike import PrimeHub
myHub = PrimeHub()
mySensor = colorDistanceSensor("F", 7)
#You can use the following commands to send PF commands:
#PFComboDirectCommand, PFSingleOutputCommand and PFComboPWMCommand
force = ForceSensor('E')

lastCommand = 0

while True:
    if force.is_pressed():
        if lastCommand != 1:
            mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.BACKWARD, PFMotor.FORWARD)
        lastCommand = 1
    elif myHub.left_button.is_pressed():
        if lastCommand !=2:
            mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.BACKWARD, PFMotor.BACKWARD)
        lastCommand = 2
    elif myHub.right_button.is_pressed():
        if lastCommand != 3:
            mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.FORWARD, PFMotor.FORWARD)
        lastCommand = 3
    else:
        if lastCommand != 0:
            mySensor.PFComboDirectCommand(PFChannel.CHANNEL_4, PFMotor.FLOAT, PFMotor.FLOAT)
        lastCommand = 0
    utime.sleep_ms(75)