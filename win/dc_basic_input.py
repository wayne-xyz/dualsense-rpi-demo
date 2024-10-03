from pydualsense import pydualsense
import time
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import signal

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


def graphic_input():
    # using the matplotlib to show:
    # 1.  touchpad for two points x1,y1,x2,y2
    # 2.  trigger for two lines l1: x:time, y:value; l2: x:time, y:value
    # 3.  analog stick for two lines l1: x1,y1; l2: x2, y2
    # 4.  acc x,y,z
    # 5.  gyro x,y,z 
    # totally 5 graphics/plots for the above:
    # 1.  touchpad for two points x1,y1,x2,y2
    
    dualsense = pydualsense()
    dualsense.init()

    # Set up the plots
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(12, 18))
    plt.subplots_adjust(hspace=0.4)

    # 1. Touchpad
    touchpad_scatter = ax1.scatter([0, 0], [0, 0], c=['r', 'b'], alpha=0)
    ax1.set_xlim(0, 1920)
    ax1.set_ylim(1080, 0)
    ax1.set_title('Touchpad')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')

    # 2. Triggers
    trigger_lines = [ax2.plot([], [], label=f'{trigger}')[0] for trigger in ['L2', 'R2']]
    ax2.set_ylim(0, 255)
    ax2.set_title('Triggers')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.legend()

    # 3. Analog Sticks
    stick_scatter = ax3.scatter([128, 128], [128, 128], c=['r', 'b'], alpha=0)
    ax3.set_xlim(0, 255)
    ax3.set_ylim(255, 0)
    ax3.set_title('Analog Sticks')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')

    # 4. Accelerometer
    acc_lines = [ax4.plot([], [], label=f'Acc {axis}')[0] for axis in ['X', 'Y', 'Z']]
    ax4.set_ylim(-32768, 32767)
    ax4.set_title('Accelerometer')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Value')
    ax4.legend()

    # 5. Gyroscope
    gyro_lines = [ax5.plot([], [], label=f'Gyro {axis}')[0] for axis in ['Pitch', 'Yaw', 'Roll']]
    ax5.set_ylim(-32768, 32767)
    ax5.set_title('Gyroscope')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('Value')
    ax5.legend()

    # Initialize data arrays
    max_points = 1000
    trigger_data = {trigger: np.zeros(max_points) for trigger in ['L2', 'R2']}
    acc_data = {axis: np.zeros(max_points) for axis in ['X', 'Y', 'Z']}
    gyro_data = {axis: np.zeros(max_points) for axis in ['Pitch', 'Yaw', 'Roll']}
    time_data = np.zeros(max_points)

    # Flag to control the animation
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("Ctrl+C pressed. Stopping the animation...")
        running = False

    # Set up the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    start_time = time.time()

    def update(frame):
        nonlocal time_data
        if not running:
            ani.event_source.stop()
            plt.close(fig)
            return

        current_time = time.time() - start_time
        state = dualsense.state

        # 1. Touchpad
        touchpad_x = [state.trackPadTouch0.X, state.trackPadTouch1.X]
        touchpad_y = [state.trackPadTouch0.Y, state.trackPadTouch1.Y]
        touchpad_scatter.set_offsets(np.c_[touchpad_x, touchpad_y])
        touchpad_scatter.set_alpha([1 if x > 0 or y > 0 else 0 for x, y in zip(touchpad_x, touchpad_y)])

        # 2. Triggers
        for trigger in ['L2', 'R2']:
            trigger_data[trigger] = np.roll(trigger_data[trigger], -1)
            trigger_data[trigger][-1] = getattr(state, trigger)

        # 3. Analog Sticks
        stick_x = [state.LX, state.RX]
        stick_y = [state.LY, state.RY]
        stick_scatter.set_offsets(np.array([stick_x, stick_y]).T)
        stick_scatter.set_alpha([1, 1])

        # 4. Accelerometer
        for axis in ['X', 'Y', 'Z']:
            acc_data[axis] = np.roll(acc_data[axis], -1)
            acc_data[axis][-1] = getattr(state.accelerometer, axis)

        # 5. Gyroscope
        for axis in ['Pitch', 'Yaw', 'Roll']:
            gyro_data[axis] = np.roll(gyro_data[axis], -1)
            gyro_data[axis][-1] = getattr(state.gyro, axis)

        # Update time data
        time_data = np.roll(time_data, -1)
        time_data[-1] = current_time

        # Update plots
        for line, trigger in zip(trigger_lines, ['L2', 'R2']):
            line.set_data(time_data, trigger_data[trigger])
        ax2.set_xlim(time_data[0], time_data[-1])

        for line, axis in zip(acc_lines, ['X', 'Y', 'Z']):
            line.set_data(time_data, acc_data[axis])
        ax4.set_xlim(time_data[0], time_data[-1])

        for line, axis in zip(gyro_lines, ['Pitch', 'Yaw', 'Roll']):
            line.set_data(time_data, gyro_data[axis])
        ax5.set_xlim(time_data[0], time_data[-1])

        return touchpad_scatter, *trigger_lines, stick_scatter, *acc_lines, *gyro_lines

    ani = FuncAnimation(fig, update, frames=None, interval=50, blit=True)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        dualsense.close()
        print("DualSense controller connection closed.")


if __name__ == "__main__":
    mode = 'btn'  # Default mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode == 'graph':
        graphic_input()
    elif mode in ['btn', 'stk', 'trg']:
        monitor_controller_inputs(mode)
    else:
        print("Invalid mode. Please use 'btn' for button detection, 'stk' for analog stick detection, 'trg' for trigger detection, or 'graph' for graphical input display.")
        sys.exit(1)