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


    print("trigger test ")
        # set left l2 trigger to Rigid and set index 1 to force 255
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)

    # set left r2 trigger to Rigid
    ds.triggerR.setMode(TriggerModes.Pulse_A)
    ds.triggerR.setForce(0, 200)
    ds.triggerR.setForce(1, 255)
    ds.triggerR.setForce(2, 175)

    while not ds.state.R1:
        print("start triger ")
        time.sleep(1)


    # Close the connection
    ds.close()




def print_dualsense_state():
    # Get DualSense instance and initialize
    dualsense = pydualsense()
    dualsense.init()

    print('DualSense State Monitoring started. Press R1 to exit.')

    # Loop until the R1 button is pressed
    try:
        while not dualsense.state.R1:
            # Accessing various states
            print(f"Left Stick: X={dualsense.state.LX}, Y={dualsense.state.LY}")
            print(f"Right Stick: X={dualsense.state.RX}, Y={dualsense.state.RY}")
            print(f"Triggers: L2={dualsense.state.L2}, R2={dualsense.state.R2}")

            # Print whether specific buttons are pressed
            if dualsense.state.DpadUp:
                print("D-Pad Up Pressed")
            if dualsense.state.DpadDown:
                print("D-Pad Down Pressed")
            if dualsense.state.DpadLeft:
                print("D-Pad Left Pressed")
            if dualsense.state.DpadRight:
                print("D-Pad Right Pressed")
                
            print("-" * 40)

    except KeyboardInterrupt:
        pass  # Allow exit with Ctrl+C

    finally:
        # Close the controller connection
        dualsense.close()





test_connection()

#print_dualsense_state()