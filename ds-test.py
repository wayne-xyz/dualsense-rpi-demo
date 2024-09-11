from pydualsense import pydualsense,TriggerModes
import time


def test_connection():
    print("Testing connection to the PS5 controller...")
    ds=pydualsense()
    ds.init()

    print("Vibrting 3 seconds...")
    ds.setLeftMotor(100)
    ds.setRightMotor(100)
    time.sleep(3)
    ds.setLeftMotor(0)
    ds.setRightMotor(0)


    print("led test 3 seconds...    ")
    ds.set_led(255,0,0)
    time.sleep(3)
    ds.set_led(0,255,0)
    time.sleep(3)
    ds.set_led(0,0,255)
    time.sleep(3)
    ds.set_led(0,0,0)
    print("led test complete.")


    print("Battery test...")
    print("Battery level: ",ds.get_battery())
    print("Battery test complete.")

    print("Connection test complete.")

test_connection()

