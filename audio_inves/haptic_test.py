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



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test haptic feedback modes')
    parser.add_argument('--mode', type=int, default=0, 
                      help='Haptic mode (0=default, 1=enabled, 2=disabled)')
    args = parser.parse_args()
    
    customer_test(args.mode)
