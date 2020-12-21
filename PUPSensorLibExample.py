from spike import PrimeHub
#from mindstorms import MSHub


#DON'T FORGET TO IMPORT THE LIBRARY
#(or paste it here)


technicHub = PrimeHub()
#technicHub = MSHub()
mySensor = colorDistanceSensor("E")
mode = 0;
while True:
    value = mySensor.read()
    technicHub.light_matrix.write(value)
    print(value)
    if technicHub.left_button.is_pressed():
        mode = mode - 1
        mySensor.changeMode(mode)
    if technicHub.right_button.is_pressed():
        mode = mode + 1
        mySensor.changeMode(mode)