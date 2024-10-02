from pydualsense import pydualsense
import time
import sys

def monitor_controller_inputs(mode='btn'):
    dualsense = pydualsense()
    dualsense.init()

    button_mapping = {
        'SQUARE': 'square',
        'TRIANGLE': 'triangle',
        'CIRCLE': 'circle', 
        'CROSS': 'cross',
        'UP': 'DpadUp',
        'DOWN': 'DpadDown',
        'LEFT': 'DpadLeft',
        'RIGHT': 'DpadRight',
        'L1': 'L1',
        'L2': 'L2',
        'L3': 'L3',
        'R1': 'R1',
        'R2': 'R2',
        'R3': 'R3',
        'SHARE': 'share',
        'OPTIONS': 'options',
        'PS': 'ps',
        'TOUCHPAD': 'touchBtn',
        'MIC': 'micBtn'
    }

    analog_mapping = {
        'LEFT_STICK_X': 'LX',
        'LEFT_STICK_Y': 'LY',
        'RIGHT_STICK_X': 'RX',
        'RIGHT_STICK_Y': 'RY'
    }

    trigger_mapping = {
        'L2': 'L2',
        'R2': 'R2'
    }

    previous_button_states = {button: False for button in button_mapping}
    previous_trigger_states = {'L2': False, 'R2': False}

    print(f"Monitoring DualSense controller inputs in {mode.upper()} mode. Press Ctrl+C to exit.")

    try:
        while True:
            if mode == 'btn':
                # Check button states
                for button, attribute in button_mapping.items():
                    current_state = getattr(dualsense.state, attribute)
                    if current_state != previous_button_states[button]:
                        if current_state:
                            print(f"{button} button pressed")
                        else:
                            print(f"{button} button released")
                        previous_button_states[button] = current_state

                # Check trigger states (simple press/release)
                for trigger in ['L2', 'R2']:
                    current_state = getattr(dualsense.state, trigger) > 0
                    if current_state != previous_trigger_states[trigger]:
                        if current_state:
                            print(f"{trigger} trigger pressed")
                        else:
                            print(f"{trigger} trigger released")
                        previous_trigger_states[trigger] = current_state

            elif mode == 'stk':
                # Check analog stick positions
                for stick, attribute in analog_mapping.items():
                    value = getattr(dualsense.state, attribute)
                    if value != 128:  # 128 is the center position
                        print(f"{stick}: {value}")

            elif mode == 'trg':
                # Check trigger states (detailed)
                for trigger, attribute in trigger_mapping.items():
                    current_value = getattr(dualsense.state, attribute)
                    if current_value > 0:  # Only print if the trigger is being pressed
                        percentage = (current_value / 255) * 100
                        print(f"{trigger} trigger: {current_value} ({percentage:.1f}%)")

            time.sleep(0.1)  # Add a small delay to prevent excessive CPU usage

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dualsense.close()

if __name__ == "__main__":
    mode = 'btn'  # Default mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode not in ['btn', 'stk', 'trg']:
        print("Invalid mode. Please use 'btn' for button detection, 'stk' for analog stick detection, or 'trg' for trigger detection.")
        sys.exit(1)
    
    monitor_controller_inputs(mode)