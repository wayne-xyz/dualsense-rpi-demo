# dualsense-rpi-demo
For dualsense controller and raspberry pi 
And for windows 


## Description
Demos for Dualsense controller and Raspberry Pi 3B+
And for windows 

## TODO
- Lantency of the touchpad
- ACC y when stable is more than 8000



## Sep-11 2024
- Using pydualsense to test communication with the controller and perform basic actions
- Added pi-prep.sh to check if all prerequisites are met

## Source

Development 
- [pydualsense](https://github.com/flok/pydualsense)(preferred)
- [hidapi](https://github.com/libusb/hidapi)
- [dualsense-controller-python](https://github.com/yesbotics/dualsense-controller-python)

Data of HID
- [Sony DualSense](https://controllers.fandom.com/wiki/Sony_DualSense)
- [dualsense](https://github.com/nondebug/dualsense)



## Prerequisites 
### Windows
- Windows 11
- Python 3.11
- Preparing the hidapi 
- Install pydualsense



###Raspberry Pi
- Raspberry Pi 3B+
- Dualsense controller
- Raspberry Pi OS Lite (64-bit)




# Environment
## pydualsense_env


# use the ds-test.py
activate the environment
```
source pydualsense_env/bin/activate
```

## use full path to the python interpreter in virtual environment with sudo
```
sudo /home/pi/pydualsense_env/bin/python ds-test.py
``` 