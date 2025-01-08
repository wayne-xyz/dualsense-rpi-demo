# this python function using for collect data from the sensor to the csv data from the ps5 controller.



import argparse
import time
import os
import logging
import csv
import pydualsense as ds
import numpy as np
import datetime

# print env info:
import sys
print(f"sys.platform: {sys.platform}")


# data format: 
data_fields=[
    "time",
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_pitch",
    "gyro_yaw",
    "gyro_roll",
    "vibration_status", # 0: no vibration, 1: vibration type 1, 2: vibration type 2, 3: vibration type 3
    "label", # 0:on table, 1:in hand
    "person_id" # 0: person 1, 1: person 2, 2: person 3, 3: person 4
]

# data collection rule1: 
rule1={
    "rule_name":"rule1",
    "category_rows": 1000, # 1000 rows per vibration status and label
    "session_rows":50, # for the svm model, divide the data into session with 50 rows in each category
    "polling_interval":1 # polling the data every 1ms
}

# vibration pattern
vib_pattern={
    0:"no_vibration",
    1:"4khz",
    2:"1khz",
    3:"250hz",
    4:"50hz",
    5:"rhythmic_pulses", # 100 pulse and 100 pause , frequency modulation
    6:"frequency_modulation", # from 100hz to 200hz adjustable wave 
    7:"amplitude_modulation", # from the 0 to 100% adjustable wave  of the vibration
}


CSV_FILE_NAME="inertial_data"

def collect_data(csv_file_name=CSV_FILE_NAME, data_fields=data_fields, vib_pattern=vib_pattern, rule1=rule1, label=0, person_id=0, pattern_id=0):
    print(f"Starting data collection with parameters:")
    print(f"Label: {label}, Person ID: {person_id}, Pattern ID: {pattern_id}")
    
    # Initialize controller
    dualsense = ds.pydualsense()
    dualsense.init()
    
    # Get parameters from rule1
    category_rows = rule1["category_rows"]
    polling_interval = rule1["polling_interval"] / 1000.0  # Convert ms to seconds
    rule_name = rule1["rule_name"]

    try:
        # Use list instead of numpy array to handle mixed data types
        data_rows = []
        row_index = 0
        
        print(f"\nCollecting {category_rows} samples...")
        print(f"Polling interval: {polling_interval*1000:.1f}ms")
        print("Data will be saved after collection is complete...")
        
        # Main data collection loop
        while row_index < category_rows:
            start_time = time.time()
            
            # Get sensor data
            acc = dualsense.state.accelerometer
            gyro = dualsense.state.gyro
                        # skip the zero data x,y,z, pitch, yaw, roll all 0 
            if acc.X == 0 and acc.Y == 0 and acc.Z == 0 and gyro.Pitch == 0 and gyro.Yaw == 0 and gyro.Roll == 0:
                continue
            
            # Create data row
            data_row = [
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),  # timestamp
                acc.X,        # accelerometer X
                acc.Y,        # accelerometer Y
                acc.Z,        # accelerometer Z
                gyro.Pitch,   # gyroscope pitch
                gyro.Yaw,     # gyroscope yaw
                gyro.Roll,    # gyroscope roll
                pattern_id,   # vibration status
                label,        # label (0:on table, 1:in hand)
                person_id     # person ID
            ]
            
            # Append to list instead of numpy array
            data_rows.append(data_row)
            
            # Print progress every 100 samples
            if row_index % 100 == 0:
                print(f"Progress: {row_index}/{category_rows} samples", end='\r')
            
            row_index += 1
            
            # Calculate sleep time to maintain polling interval
            elapsed = time.time() - start_time
            sleep_time = max(0, polling_interval - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        print("\nData collection completed. Saving to CSV...")
        
        # Save all data at once
        csv_file_name = f"{csv_file_name}_{rule_name}.csv"
        file_exists = os.path.isfile(csv_file_name)
        
        with open(csv_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(data_fields)
            
            # Write all data at once
            writer.writerows(data_rows)
        
        print(f"Successfully saved {category_rows} samples to {csv_file_name}")
        
    except KeyboardInterrupt:
        print("\nData collection interrupted by user")
        # Save partial data if interrupted
        if row_index > 0:
            print(f"Saving {row_index} collected samples...")
            csv_file_name = f"{csv_file_name}_{rule_name}.csv"
            file_exists = os.path.isfile(csv_file_name)
            with open(csv_file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(data_fields)
                writer.writerows(data_rows[:row_index])
            print(f"Partial data saved to {csv_file_name}")
            
    except Exception as e:
        print(f"\nError during data collection: {e}")
    finally:
        # Clean up
        dualsense.close()
        print("Controller disconnected")


def test_controller_rt():
    print("========start test controller rt========")
    
    try:
        # Initialize controller
        dualsense = ds.pydualsense()
        dualsense.init()
        print("Controller initialized successfully")

        # Real-time data loop
        print("\nStarting real-time sensor data... Press Ctrl+C to stop")
        while True:
            # Clear console for better visibility
            print("\033[2J\033[H")
            print("=== DualSense Sensor Data ===")
            
            # Get accelerometer data
            acc = dualsense.state.accelerometer
            print("\nAccelerometer:")
            print(f"X: {acc.X:8.3f}")
            print(f"Y: {acc.Y:8.3f}")
            print(f"Z: {acc.Z:8.3f}")
            
            # Get gyroscope data
            gyro = dualsense.state.gyro
            print("\nGyroscope:")
            print(f"Pitch: {gyro.Pitch:8.3f}")
            print(f"Yaw:   {gyro.Yaw:8.3f}")
            print(f"Roll:  {gyro.Roll:8.3f}")
            
            # Add timestamp
            print(f"\nTimestamp: {time.strftime('%H:%M:%S')}")
            print("\nPress Ctrl+C to stop...")
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping data collection...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Clean up
        if 'dualsense' in locals():
            dualsense.close()
            print("Controller disconnected")


def main():
    # Add your main logic here
    pass



if __name__ == "__main__":
    print("========start collect data========")
    #  using the command line argument to get the label, person_id, pattern_id
    # example: python collecte.py --label 0 --person_id 0 --pattern_id 0 --test_controller_rt False
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", type=int, default=0)
    parser.add_argument("--person_id", type=int, default=0)
    parser.add_argument("--pattern_id", type=int, default=0)
    parser.add_argument("--test_controller_rt", type=bool, default=False)
    args = parser.parse_args()
    if args.test_controller_rt:
        test_controller_rt()
    else:
        collect_data(label=args.label, person_id=args.person_id, pattern_id=args.pattern_id)
    print("========end collect data========")
