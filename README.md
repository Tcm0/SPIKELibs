# SPIKELibs
This is the repository for my LEGO SPIKE Prime (45678) and Robot Inventor (51515) libraries.

The first library, PUPSensorLib.py, can be used to use the other Powered Up sensors with the large hubs that LEGO doesn't support properly. Currently 3 sensors are supported:
-Color & Distance Sensor (known from LEGO Boost)
-Motion Sensor (known from LEGO WeDo 2.0 and the LEGO Ideas grand piano)
-Tilt Sensor (known from LEGO WeDo 2.0)
-Send Power Functions IR commands with the Color & Distance Sensor to up to 8 PF receivers (a total of 16 motors with just one port on the hub)

The easiest way to use it is to copy the content of PUPSensorLib.py into a new python project in the SPIKE Prime or Mindstorms Robot Inventor software. Then you can paste the code of the example you'd like to use below that into the project.
Another option is to upload the code to the hub and use it as a library. Check https://github.com/XenseEducation/spiketools-release/releases for a tool to do that.
