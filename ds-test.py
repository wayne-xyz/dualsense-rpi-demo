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
    ds.setLED(255,0,0)
    time.sleep(3)
    ds.setLED(0,255,0)
    time.sleep(3)
    ds.setLED(0,0,255)
    time.sleep(3)
    ds.setLED(0,0,0)
    print("led test complete.")


    print("Battery test...")
    print("Battery level: ",ds.battery_level)
    print("Battery test complete.")

    print("Connection test complete.")

test_connection()

