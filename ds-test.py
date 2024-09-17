from pydualsense import pydualsense,TriggerModes
import time
import hid


def test_connection():
    print("Listing available HID devices...")
    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

    print("Testing connection to the PS5 controller...")
    ds = pydualsense()
    ds.init()

    print("Vibrating 3 seconds...")
    ds.setLeftMotor(100)
    ds.setRightMotor(100)
    time.sleep(3)
    ds.setLeftMotor(0)
    ds.setRightMotor(0)

    print("LED test 3 seconds...")
    # Updated LED control
    ds.light.setColorI(255, 0, 0)  # Red
    time.sleep(3)
    ds.light.setColorI(0, 255, 0)  # Green
    time.sleep(3)
    ds.light.setColorI(0, 0, 255)  # Blue
    time.sleep(3)
    ds.light.setColorI(0, 0, 0)    # Off
    print("LED test complete.")


    print("Viberating 3 seconds.. in different force lever for left and right motor")
    ds.setLeftMotor(0)
    ds.setRightMotor(255)
    time.sleep(3)
    ds.setLeftMotor(0)
    ds.setRightMotor(0)


    # Close the connection
    ds.close()

test_connection()

