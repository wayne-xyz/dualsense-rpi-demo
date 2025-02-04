# dualsense-rpi-demo
Resaerch by using the features from the Dualsense controlelr 


## Description
Investigation for the Dualsense controller based on the PC/Mac

## TODO
- [ ] Dynamic triger features
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

## For support the customer hidapi 
```outreport[1]```
the haptic UAC features 


## HID commend table 
### Output table(USB)
Source: https://controllers.fandom.com/wiki/Sony_DualSense 

| Byte.Offset | Bit(s)       | Field                          | Description                                                   |
|-------------|--------------|--------------------------------|---------------------------------------------------------------|
| 0.0         | 0            | EnableRumbleEmulation          | Emulation(Haptic), Suggest halving rumble strength                               |
| 0.1         | 1            | UseRumbleNotHaptics            | Use rumble instead of haptics                                 |
| 0.2         | 2            | AllowRightTriggerFFB           | Enable setting RightTriggerFFB                                |
| 0.3         | 3            | AllowLeftTriggerFFB            | Enable setting LeftTriggerFFB                                 |
| 0.4         | 4            | AllowHeadphoneVolume           | Enable setting VolumeHeadphones                               |
| 0.5         | 5            | AllowSpeakerVolume             | Enable setting VolumeSpeaker                                  |
| 0.6         | 6            | AllowMicVolume                 | Enable setting VolumeMic                                      |
| 0.7         | 7            | AllowAudioControl              | Enable setting AudioControl section                           |
| 1.0         | 0            | AllowMuteLight                 | Enable setting MuteLightMode                                  |
| 1.1         | 1            | AllowAudioMute                 | Enable setting MuteControl section                            |
| 1.2         | 2            | AllowLedColor                  | Enable RGB LED section                                        |
| 1.3         | 3            | ResetLights                    | Release LEDs from wireless firmware control                   |
| 1.4         | 4            | AllowPlayerIndicators          | Enable setting PlayerIndicators section                       |
| 1.5         | 5            | AllowHapticLowPassFilter      | Enable HapticLowPassFilter                                    |
| 1.6         | 6            | AllowMotorPowerLevel          | Enable MotorPowerLevel reductions for trigger/haptic          |
| 1.7         | 7            | AllowAudioControl2             | Enable setting AudioControl2 section                          |
| 2           | -            | RumbleEmulationRight           | Emulates the light weight rumble                              |
| 3           | -            | RumbleEmulationLeft            | Emulates the heavy weight rumble                              |
| 4           | -            | VolumeHeadphones               | Max 0x7F                                                       |
| 5           | -            | VolumeSpeaker                  | PS5 uses range 0x3D-0x64                                       |
| 6           | -            | VolumeMic                      | Non-linear, max at 64, 0 is not fully muted                    |
| 7.0         | 0-1          | MicSelect                      | 0=Auto, 1=Internal, 2=External, 3=Unclear (Test needed)       |
| 7.2         | 2            | EchoCancelEnable               | Enable echo cancellation                                       |
| 7.3         | 3            | NoiseCancelEnable              | Enable noise cancellation                                      |
| 7.4         | 4-5          | OutputPathSelect               | 0=L_R_X, 1=L_L_X, 2=L_L_R, 3=X_X_R                           |
| 7.6         | 6-7          | InputPathSelect                | 0=CHAT_ASR, 1=CHAT_CHAT, 2=ASR_ASR, 3=Invalid                 |
| 8           | -            | MuteLightMode                  | Controls mute light behavior                                   |
| 9.0         | 0            | TouchPowerSave                 | Enable touchpad power saving                                   |
| 9.1         | 1            | MotionPowerSave                | Enable motion power saving                                     |
| 9.2         | 2            | HapticPowerSave                | AKA BulletPowerSave                                           |
| 9.3         | 3            | AudioPowerSave                 | Enable audio power saving                                      |
| 9.4         | 4            | MicMute                        | Mute the microphone                                            |
| 9.5         | 5            | SpeakerMute                    | Mute the speaker                                              |
| 9.6         | 6            | HeadphoneMute                  | Mute the headphones                                            |
| 9.7         | 7            | HapticMute                     | AKA BulletMute                                                |
| 10-20       | -            | RightTriggerFFB                | 11 bytes for right trigger force feedback                      |
| 21-31       | -            | LeftTriggerFFB                 | 11 bytes for left trigger force feedback                       |
| 32          | -            | HostTimestamp                  | Mirrored into report read                                      |
| 36.0        | 0-3          | TriggerMotorPowerReduction     | 0x0-0x7, applied in 12.5% reductions                           |
| 36.4        | 4-7          | RumbleMotorPowerReduction     | 0x0-0x7, applied in 12.5% reductions                           |
| 37.0        | 0-2          | SpeakerCompPreGain             | Additional speaker volume boost                                |
| 37.3        | 3            | BeamformingEnable              | Likely affects microphone performance                          |
| 37.4        | 4-7          | UnkAudioControl2               | Unknown additional audio settings                              |
| 38.0        | 0            | AllowLightBrightnessChange     | Enable LED brightness control                                  |
| 38.1        | 1            | AllowColorLightFadeAnimation   | Enable light fade animation                                     |
| 38.2        | 2            | EnableImprovedRumbleEmulation  | Requires FW >= 0x0224, no need to halve rumble strength        |
| 38.3        | 3-7          | UNKBITC                        | Unused                                                         |
| 39.0        | 0            | HapticLowPassFilter            | Enable haptic low-pass filtering                               |
| 39.1        | 1-7          | UNKBIT                         | Unknown usage                                                  |
| 40          | -            | UNKBYTE                        | Possibly misaligned haptic low-pass filter                     |
| 41          | -            | LightFadeAnimation             | Light fade animation settings                                  |
| 42          | -            | LightBrightness                | Controls brightness level                                      |
| 43.0        | 0            | PlayerLight1                   | Controls Player 1 indicator                                    |
| 43.1        | 1            | PlayerLight2                   | Controls Player 2 indicator                                    |
| 43.2        | 2            | PlayerLight3                   | Controls Player 3 indicator                                    |
| 43.3        | 3            | PlayerLight4                   | Controls Player 4 indicator                                    |
| 43.4        | 4            | PlayerLight5                   | Controls Player 5 indicator (unconfirmed)                      |
| 43.5        | 5            | PlayerLightFade                | If low, lights fade in; if high, lights instantly change       |
| 43.6        | 6-7          | PlayerLightUNK                 | Unknown usage                                                  |
| 44          | -            | LedRed                         | Red component of RGB LED                                       |
| 45          | -            | LedGreen                       | Green component of RGB LED                                     |
| 46          | -            | LedBlue                        | Blue component of RGB LED                                      |



## Potential feature in the HIDapi 
not include in the pydualsense.
- outReport[5] - outReport[8]  audio related

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