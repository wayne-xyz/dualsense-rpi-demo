# dualsense-rpi-demo
For dualsense controller and raspberry pi 
And for windows for MacOS


## Description
Demos for Dualsense controller and Raspberry Pi 3B+
And for windows 

## TODO
- [X] Limitation of the vibration frequncy 
- [X] Sound play and LRA vibration mimic 
- [X] Limitation frequency of the speaker's output
- [X] Limitation frequency of the mic's input
- [X] Vibrate when identify the status of the controller

## Features data
sampling/polling rate from controller: 250hz , hid is 1000hz


## Source

Development 
- [pydualsense](https://github.com/flok/pydualsense)(preferred)(not working on macos)
- [hidapi](https://github.com/libusb/hidapi)
- [dualsense-controller-python](https://github.com/yesbotics/dualsense-controller-python)

Data of HID
- [Sony DualSense](https://controllers.fandom.com/wiki/Sony_DualSense)
- [dualsense](https://github.com/nondebug/dualsense)

## For supportting the macos
edit the hidapi.py from https://github.com/flok/pydualsense  to include the darwin platform

```
# edit the platform to include darwin by Wayne J 2025-01-06 custom edit
if platform.startswith('linux') or platform.startswith('darwin'):
    ffi.cdef("""
```

## For supportting haptic enabliing switch for the pydualsense library
- add the enable_haptic = True in the pydualsense.py 
- add hatpic class in the pydualsense.py  
- add the 0x00 and 0x03 to the outReport[1] which are the flags determing what changes this packet will perform


## Prerequisites 
### Windows
- Windows 11
- Python 3.11
- Preparing the hidapi 
- Install pydualsense



### Raspberry Pi
- Raspberry Pi 3B+
- Dualsense controller
- Raspberry Pi OS Lite (64-bit)

### MacOS
- MacOS 14.0
- Python 3.11
- Preparing the hidapi 
- Install pydualsense
- Install: brew install portaudio 


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