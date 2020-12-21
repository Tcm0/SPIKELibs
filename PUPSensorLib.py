import hub, utime
from hub import port
#In memories of Gianluca Cannalire
#Special thanks:
#Roman H
#Philo
#Nard Strijbosch

class motionSensorModes:
    DETECT_MODE = 0     #Measures the distance (up to 10)
    COUNT_MODE = 1      #Counts how often things were nearby
    #CAL_RAW_MODE = 2   #probably calibration. This library skips it

class tiltSensorModes:  
    ANGLE_DEG_MODE = 0  #Measures the angle in both directions (up to 45 deg)
    TILT_DIR_MODE = 1
    CRASH_CNT_MODE = 2  #probably amount of crashes
    #CAL_MODE = 3


class colorDistanceSensorModes:
    COLOR_MODE = 0      #Measures a color ID
    DISTANCE_MODE = 1   #Measures the distance (up to 10)
    COUNT_MODE = 2      #Counts how often things were nearby
    REFL_LIGHT_MODE = 3 #Measures the reflected light of the LED in percent
    AMB_LIGHT_MODE = 4  #Measures the ambient light from other sources
    RGB_MODE = 6
    #PF_MODE = 7        #Does not work yet

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

    #Writing does not work so far!
    #def write(self, data):
    #    bytestosend = bytearray(b'\x00\x0F')
    #    getattr(hub.port, self.__port).device.write_direct()

    def changeMode(self, newSensorMode):
        if newSensorMode >= 0 and newSensorMode <= self.maxModes:
            getattr(hub.port, self.__port).device.mode(newSensorMode)


class colorDistanceSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):     #Port, mode
        UARTSensor.__init__(self, sensorPort, 7, sensorMode)

class motionSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):
        UARTSensor.__init__(self, sensorPort, 2, sensorMode)

class tiltSensor(UARTSensor):
    def __init__(self, sensorPort, sensorMode = 0):
        UARTSensor.__init__(self, sensorPort, 3, sensorMode)
