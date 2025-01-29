import pydualsense
import time
import sys


def customer_test(haptic_mode: int=88):
    dualsense=pydualsense.pydualsense()
    dualsense.init()
    dualsense.haptic_mode.set_mode(haptic_mode)

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

def parse_int_or_hex(value):
    """Parse string as integer or hex"""
    try:
        if isinstance(value, str) and value.startswith('0x'):
            return int(value, 16)
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f'Invalid integer or hex value: {value}')

def test_customer_output(k:int,v:int):
    dualsense=pydualsense.pydualsense()
    dualsense.init()

    dualsense.hid_customer.set_customer_setting(k,v)
    print(f"set the {k} to {v}")

    time.sleep(5)
    for i in range(5, 0, -1):
        print(f"Time remaining: {i} seconds", end='\r')
        time.sleep(1)
    print("Time's up!")
    dualsense.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test haptic feedback modes and intensity')
    parser.add_argument('--mode', type=int, 
                        help='Haptic mode (0=default, 1=enabled, 2=disabled)')
    parser.add_argument('--intensity', type=int, 
                        help='Haptic intensity (0-255)')
    parser.add_argument('--customer_output', nargs=2, metavar=('k', 'v'), 
                        help='Customer output setting (key value pair in decimal or hex)')
    args = parser.parse_args()
    
    if args.mode is not None:
        customer_test(args.mode)
    elif args.intensity is not None:
        set_controller_haptic(args.intensity)
    elif args.customer_output is not None:
        try:
            k = parse_int_or_hex(args.customer_output[0])
            v = parse_int_or_hex(args.customer_output[1])
            test_customer_output(k, v)
        except ValueError as e:
            print(f"Error: Invalid input values - {str(e)}")
            sys.exit(1)


