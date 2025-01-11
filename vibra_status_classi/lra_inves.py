# this script is for using the invesitgation of the LRA linear resonat actuator 

import argparse
import numpy as np
import pydualsense as ds
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# method 1: response time and ftt of the LRA to full intensity value by the accelerometer's change


def frequency_range():
    # Initialize the controller
    dualsense = ds.pydualsense()
    dualsense.init()
    print("Controller initialized.")

    sleep_duration = 0.120  # Default vibration duration in seconds
    num_samples = 100  # Number of samples to display in the plot

    # Initialize the accelerometer data
    accelerometer_data = []

    # Real-time plotting setup
    fig, ax = plt.subplots()
    ax.set_title("Real-time Accelerometer Data")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Acceleration (m/s²)")
    ax.grid(True)

    # Line objects for X, Y, Z axes
    x_line, = ax.plot([], [], label="X-axis", color="r")
    y_line, = ax.plot([], [], label="Y-axis", color="g")
    z_line, = ax.plot([], [], label="Z-axis", color="b")

    ax.legend()
    time_data = []

    def update(frame):
        # Trigger vibration
        dualsense.setLeftMotor(255)
        dualsense.setRightMotor(255)
        time.sleep(sleep_duration)
        
        # Get accelerometer data
        timestamp = time.time()
        x = dualsense.state.accelerometer.X
        y = dualsense.state.accelerometer.Y
        z = dualsense.state.accelerometer.Z
        accelerometer_data.append((timestamp, x, y, z))

        # Limit to the last `num_samples` entries
        if len(accelerometer_data) > num_samples:
            accelerometer_data.pop(0)

        # Extract data for plotting
        timestamps = [data[0] - accelerometer_data[0][0] for data in accelerometer_data]
        x_values = [data[1] for data in accelerometer_data]
        y_values = [data[2] for data in accelerometer_data]
        z_values = [data[3] for data in accelerometer_data]

        # Update plot lines
        x_line.set_data(timestamps, x_values)
        y_line.set_data(timestamps, y_values)
        z_line.set_data(timestamps, z_values)

        # Adjust axis limits dynamically
        ax.set_xlim(max(0, timestamps[0]), timestamps[-1])
        ax.set_ylim(-2, 2)  # Adjust based on expected accelerometer range

        # Turn off vibration
        dualsense.setLeftMotor(0)
        dualsense.setRightMotor(0)
        time.sleep(sleep_duration)

        return x_line, y_line, z_line

    ani = FuncAnimation(fig, update, interval=50, blit=True)

    try:
        plt.show()
    finally:
        # Clean up and close the controller
        dualsense.close()
        print("Controller closed.")





def play_sound():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Investigate LRA frequency and sound')
    
    parser.add_argument("--mode",
                       type=str, 
                       required=True,
                       choices=['frequency', 'sound'],
                       help="Mode to run: frequency or sound investigation")
    
    args = parser.parse_args()
    
    if args.mode == 'frequency':
        frequency_range()
    elif args.mode == 'sound':
        play_sound()