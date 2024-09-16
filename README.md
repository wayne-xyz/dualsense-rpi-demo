# dualsense-rpi-demo
For dualsense controller and raspberry pi 

## Description
Demos for Dualsense controller and Raspberry Pi 3B+

## Sep-11 2024
- Using pydualsense to test communication with the controller and perform basic actions
- Added pi-prep.sh to check if all prerequisites are met


## Prerequisites
- Raspberry Pi 3B+
- Dualsense controller
- Raspberry Pi OS Lite (64-bit)

- [pydualsense](https://github.com/flok/pydualsense)

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