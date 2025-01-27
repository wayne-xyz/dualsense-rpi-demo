import pydualsense
import time
def customer_test(haptic_mode: int=0):
    dualsense=pydualsense.pydualsense()
    dualsense.init()
    dualsense.haptic_mode.set_mode(haptic_mode)
    if haptic_mode == 1:
        print("haptic enabled")
    elif haptic_mode == 2:
        print("haptic disabled")
    else:
        print("haptic mode default")

    dualsense.close()


    time.sleep(1)

def set_controller_haptic(intesity:int=0,duration:int=10):
    if intesity < 0 or intesity > 255:
        print("Invalid intensity value")
        return
    
    dualsense=pydualsense.pydualsense()
    dualsense.init()
    dualsense.leftMotor= intesity
    dualsense.rightMotor= intesity
    print(f"play the {intesity} for {duration} seconds")

    time.sleep(10)
    # dualsense.leftMotor= 0
    # dualsense.rightMotor= 0
    # print("stop the vibration")

    # time.sleep(2)
    dualsense.close()


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test haptic feedback modes and intensity')
    parser.add_argument('--mode', type=int, default=0, 
                        help='Haptic mode (0=default, 1=enabled, 2=disabled)')
    parser.add_argument('--intensity', type=int, default=0, 
                        help='Haptic intensity (0-255)')
    args = parser.parse_args()
    
    if args.mode is not None:
         customer_test(args.mode)
    if args.intensity is not None:
        set_controller_haptic(args.intensity)


