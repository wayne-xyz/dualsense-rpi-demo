# dualsense-rpi-demo
For dualsense controller and raspberry pi 
And for windows for MacOS


## Description
Demos for Dualsense controller and Raspberry Pi 3B+
And for windows 

## TODO
- [ ] Limitation of the vibration frequncy 
- [ ] Limitation of the vibration amplitude 
- [ ] Limitation frequency of the speaker's output
- [ ] Limitation frequency of the mic's input
- [ ] Vibrate when identify the status of the controller

## Features data
sampling/polling rate from controller: 250hz , hid is 1000hz


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



### Raspberry Pi
- Raspberry Pi 3B+
- Dualsense controller
- Raspberry Pi OS Lite (64-bit)

### MacOS
- MacOS 14.0
- Python 3.11
- Preparing the hidapi 
- Install pydualsense


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