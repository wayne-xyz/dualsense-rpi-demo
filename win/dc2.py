from time import sleep, time
import time
from dualsense_controller import DualSenseController

def run_controller_demo(duration=30):
    # List available devices and throw exception when there is no device detected
    device_infos = DualSenseController.enumerate_devices()
    if len(device_infos) < 1:
        raise Exception('No DualSense Controller available.')

    # Create an instance, use first available device
    controller = DualSenseController()

    # Callback function for button presses
    def on_button_event(button, is_pressed):
        state = "pressed" if is_pressed else "released"
        print(f"{button} button {state}")

    # Register callbacks for specific buttons
    controller.btn_cross.on_down(lambda: on_button_event("Cross", True))
    controller.btn_cross.on_up(lambda: on_button_event("Cross", False))
    controller.btn_circle.on_down(lambda: on_button_event("Circle", True))
    controller.btn_circle.on_up(lambda: on_button_event("Circle", False))
    controller.btn_square.on_down(lambda: on_button_event("Square", True))
    controller.btn_square.on_up(lambda: on_button_event("Square", False))
    controller.btn_triangle.on_down(lambda: on_button_event("Triangle", True))
    controller.btn_triangle.on_up(lambda: on_button_event("Triangle", False))
    controller.btn_ps.on_down(lambda: on_button_event("PS", True))
    controller.btn_ps.on_up(lambda: on_button_event("PS", False))
    controller.btn_options.on_down(lambda: on_button_event("Options", True))
    controller.btn_options.on_up(lambda: on_button_event("Options", False))
    controller.btn_l1.on_down(lambda: on_button_event("L1", True))
    controller.btn_l1.on_up(lambda: on_button_event("L1", False))
    controller.btn_r1.on_down(lambda: on_button_event("R1", True))
    controller.btn_r1.on_up(lambda: on_button_event("R1", False))
    controller.btn_l2.on_down(lambda: on_button_event("L2", True))
    controller.btn_l2.on_up(lambda: on_button_event("L2", False))
    controller.btn_r2.on_down(lambda: on_button_event("R2", True))
    controller.btn_r2.on_up(lambda: on_button_event("R2", False))

    # Enable/connect the device
    controller.activate()

    # Start time
    start_time = time.time()

    print(f"Controller demo started. Running for {duration} seconds...")
    print("Press any button on the DualSense controller.")

    # Run for specified duration
    while time.time() - start_time < duration:
        sleep(0.001)

    # Disable/disconnect controller device
    controller.deactivate()
    print("Controller demo ended.")

# Run the demo for 30 seconds
if __name__ == "__main__":
    run_controller_demo(30)

