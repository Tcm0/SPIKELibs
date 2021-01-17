#Example for 16 individually controlled Power Functions motors
#A video of the example: https://www.youtube.com/watch?v=PnSCIm-i0b4
#ATTENTION! There are several things you have to keep in mind if you want to get it to work properly

#This program uses the extended address space of the PF protocol. Use the following procedure:
#1. Turn the 4 receivers that should use the extended address space on
#2. Send PFChangeAddressSpace CMD for right channel (start this program and click the right button when asked)
# (make sure that the LEDs of the receivers blink when you change the address space)
#3. Turn the other 4 receivers for the normal address space on
#Now you SHOULD be able to control all the motors individually. You have to set addressSpace value to 1
#for commands that control the first 4 Receivers in the extended address space.

#NOTES/ DEBUG/ WHY IT MIGHT NOT WORK
#The EV3 IR Sensor ignores Address bit. It will react to commands with or without addressSpace = 1
#Make sure that the Color & Distance sensor reaches all of the receivers. You might have to change the
# order/position if their LEDs don't blink or change the light conditions.
#Some older PF IR receivers don't work with the extended address space (Version 1). Make sure to
# use V1.2 or newer for the extended commands if the receiver doesn't work with the change command.
#The address toggle command might not work on the first few tries. Check if all receivers are in the extended
# mode by sending cmds for the extended mode before you turn the last 4 receivers on.
#(Check if they are actually in extended mode and don't thrust that they are)
#Receivers in ext. mode stay there until they are turned off or until they receive a addr. change CMD

#make sure to import the lib itself or paste it here
import utime
from spike import PrimeHub

#This function maps the counter to the actual motor
# 0- 3: 1st motor in normal address space
# 4- 7: 2nd motor in normal address space
# 8-11: 1st motor in extended address space
#12-15: 2nd motor in extended address space
def turnMotorOn(PFSensor, PFM):
    print(PFM)
    if PFM < 4:
        PFSensor.PFComboDirectCommand(bytes([PFM]), PFMotor.FORWARD, PFMotor.FLOAT)
    elif PFM < 8:
        PFSensor.PFComboDirectCommand(bytes([PFM-4]), PFMotor.FLOAT, PFMotor.FORWARD)
    elif PFM < 12:
        PFSensor.PFComboDirectCommand(bytes([PFM-8]), PFMotor.FORWARD, PFMotor.FLOAT, 1)
    elif PFM < 16:
        PFSensor.PFComboDirectCommand(bytes([PFM-12]), PFMotor.FLOAT, PFMotor.FORWARD, 1)
    utime.sleep_ms(100)

#This is the actual start of the program
myHub = PrimeHub()
mySensor = colorDistanceSensor("F", 7)
selectedMotor = 0

myHub.light_matrix.write('turn 4 receivers on and press RIGHT')
myHub.right_button.wait_until_pressed()
#Send 4 ChangeAddressSpace commands to each of the sensors to make sure that they switch the address space.
#(You might have to restart the program if they still don't change on first try)
for x in range(1):
    mySensor.PFChangeAddressSpace(PFChannel.CHANNEL_1)
    #utime.sleep_ms(100)
    mySensor.PFChangeAddressSpace(PFChannel.CHANNEL_2)
    #utime.sleep_ms(100)
    mySensor.PFChangeAddressSpace(PFChannel.CHANNEL_3)
    #utime.sleep_ms(100)
    mySensor.PFChangeAddressSpace(PFChannel.CHANNEL_4)
    #utime.sleep_ms(100)

#You can turn the other receivers on when the first 4 are in extended address space
myHub.light_matrix.write('turn the other receivers on')
utime.sleep_ms(400)
myHub.light_matrix.write(selectedMotor)
turnMotorOn(mySensor, selectedMotor)

#This is mainly the menu control
while True:
    if myHub.right_button.is_pressed():
        if selectedMotor < 15:
            selectedMotor = selectedMotor+1
            myHub.light_matrix.write(selectedMotor)
            turnMotorOn(mySensor, selectedMotor)
    if myHub.left_button.is_pressed():
        if selectedMotor > 0:
            selectedMotor = selectedMotor-1
            myHub.light_matrix.write(selectedMotor)
            turnMotorOn(mySensor, selectedMotor)