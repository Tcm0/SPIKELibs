import hub, utime
from hub import port
#In memories of Gianluca Cannalire
#Special thanks:
#Roman H
#Philo
#ahmedjouirou: https://github.com/ahmedjouirou/legopup_arduino
#Ralph Hempel
#Extra huge thanks to:
#Nard Strijbosch

class motionSensorModes:
    DETECT_MODE = 0     #Measures the distance (up to 10)
    COUNT_MODE = 1      #Counts how often things were nearby
    #CAL_RAW_MODE = 2   #probably calibration. This library skips it

class tiltSensorModes:
    ANGLE_DEG_MODE = 0  #Measures the angle in both directions (up to 45 deg)
    TILT_DIR_MODE = 1
    CRASH_CNT_MODE = 2  #probably amount of "crashes" (how often sensor hit something else)
    #CAL_MODE = 3


class colorDistanceSensorModes:
    COLOR_MODE = 0      #Measures a color ID (see colorDistanceSensorColorID)
    DISTANCE_MODE = 1   #Measures the distance (up to 10)
    COUNT_MODE = 2      #Counts how often things were nearby
    REFL_LIGHT_MODE = 3 #Measures the reflected light of the LED in percent
    AMB_LIGHT_MODE = 4  #Measures the ambient light from other sources
    LED_COLOR_MODE = 5 #Sets the color of the sensor's LED (see colorDistanceSensorLight)
    RGB_MODE = 6        #Measures light data in RAW RGB
    #https://github.com/pybricks/pybricks-micropython/blob/0b9b18a084ae72f419ce06b4168bc0dbb12d8a94/pybricks/pupdevices/pb_type_pupdevices_colordistancesensor.c#L28
    PF_MODE = 7        #Send Power Functions commands
    #COMBINED_MODE = 8  #Officially called SPEC1. Seems to bundle serveral of the values from above.

#use with changeColor(color) of colorDistanceSensor
class colorDistanceSensorLight:
    COLOR_OFF = 0
    COLOR_BLUE = 3
    COLOR_GREEN = 5
    COLOR_RED = 9
    COLOR_WHITE = 10

#Color IDs for COLOR_MODE of colorDistanceSensor
class colorDistanceSensorColorID:
    COLOR_BLACK = 0
    COLOR_BLUE = 3
    COLOR_GREEN = 5
    COLOR_YELLOW = 7
    COLOR_RED = 9
    COLOR_WHITE = 10
    #TODO COLOR_PINK, COLOR_TURQUOISE and COLOR_ORANGE are missing

class PFMotor:
    #Constants for Power Functions combo direct mode
    FLOAT = b'\x00'
    FORWARD = b'\x01'
    BACKWARD = b'\x02'
    BRAKE = b'\x03'

    #Constants for Power Functions single output and combo PWM modes
    PWM_FLOAT = b'\x00'
    PWM_FORWARD_1 = b'\x01'
    PWM_FORWARD_2 = b'\x02'
    PWM_FORWARD_3 = b'\x03'
    PWM_FORWARD_4 = b'\x04'
    PWM_FORWARD_5 = b'\x05'
    PWM_FORWARD_6 = b'\x06'
    PWM_FORWARD_7 = b'\x07'
    PWM_BRAKE = b'\x08'
    PWM_BACKWARD_1 = b'\x09'
    PWM_BACKWARD_2 = b'\x0A'
    PWM_BACKWARD_3 = b'\x0B'
    PWM_BACKWARD_4 = b'\x0C'
    PWM_BACKWARD_5 = b'\x0D'
    PWM_BACKWARD_6 = b'\x0E'
    PWM_BACKWARD_7 = b'\x0F'

class PFChannel:
    CHANNEL_1 = b'\x00'
    CHANNEL_2 = b'\x01'
    CHANNEL_3 = b'\x02'
    CHANNEL_4 = b'\x03'

class UARTSensor:
    __mode = 0
    __port = "A"
    maxModes = 0

    def __init__(self, sensorPort, sensorMaxModes, sensorMode = 0):    #Port, mode
        self.__mode = sensorMode
        self.__port = sensorPort
        self.maxModes = sensorMaxModes
        self.changeMode(sensorMode)

    def read(self):
        return (getattr(hub.port, self.__port).device.get())

    #Writing is implemented for the sensors themselves! The following function does not work properly!
    #def write(self, data):
    #        getattr(hub.port, self.__port).device.mode(self.__mode, data)

    def changeMode(self, newSensorMode):
        if newSensorMode >= 0 and newSensorMode <= self.maxModes:
            self.__mode = newSensorMode
            getattr(hub.port, self.__port).device.mode(newSensorMode)


class colorDistanceSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):    #Port, mode
        UARTSensor.__init__(self, sensorPort, 7, sensorMode)
    
    def changeColor(self, color):
        self.__mode = 5
        getattr(hub.port, self.__port).device.mode(5, color)
    
    #The bits are not in the order that you find in the PUP documentation. The following order is what I found:
    #a? M M M D D D D L? L? L? L? T? E? C C (I didn't check bits with question marks. They have been determined by guessing)
    #The Checksum (LLLL) is calculated automatically. It should be 0
    #This mode has a timeout but the sensor will repeat the command until you send another cmd or stop the program
    #motor1 and motor2 are NOT PWM commands
    #This mode is used by the normal PF remote (and the EV3 remote)
    def PFComboDirectCommand(self, channel, motor1, motor2):  #Channel of receiver, blue port, red port
        self.__mode = 7
        PFmode = b'\x10'
        motor1 = motor1[0] << 2
        sendbuf = PFmode[0] | motor1 | motor2[0]
        getattr(hub.port, self.__port).device.mode(7, bytes([sendbuf]) + channel)
    
    #This mode has no timeout (except special cases). It's used by the PF train remote
    #output is the port of the receiver. It can be 0 for the red port, 1 for the blue one
    #data expects a PWM command if mode = 0 (default). See PF protocol for mode = 1
    def PFSingleOutputCommand(self, channel, output, data, PFmode = 0):    #basically channel, output and speed
        self.__mode = 7
        nibble2 = 4 | (PFmode << 1) | output
        getattr(hub.port, self.__port).device.mode(7, bytes([(nibble2 << 4) | data[0]]) + channel)
    
    #This mode has timeout. motor1 and motor2 are PWM commands. First motor is red port, second is blue port
    def PFComboPWMCommand(self, channel, motor2, motor1): #channel, speed of red port, speed of blue port
        self.__mode = 7
        getattr(hub.port, self.__port).device.mode(7, bytes([(motor1[0] << 4) | motor2[0]]) + bytes([channel[0] | 4]))
    
    def PFNibbles(self, nibble1, nibble2, nibble3):
        self.__mode = 7
        getattr(hub.port, self.__port).device.mode(7, bytes([(nibble2[0] << 4) | nibble3[0]]) + bytes([nibble1]))

class motionSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):
        UARTSensor.__init__(self, sensorPort, 2, sensorMode)

class tiltSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):
        UARTSensor.__init__(self, sensorPort, 3, sensorMode)
