import time
import numpy as np
import pandas as pd
import pydualsense as ds
import sys


#  this function will collect data from the dualsense controller only about the inertial data( gyroscope and accelerometer, save them in a csv file, with the timestamp of the data collection 
def simple_data_collection(label: str, session_time: int = 500, collection_duration: int = 100000):
    # parameters:
    # label: the label of the data collection
    # session_time: the time segment of the data collection in milliseconds
    # collection_duration: the duration of the data collection in milliseconds

    dualsense = ds.pydualsense()
    dualsense.init()    

    #  get the timestamp of the data collection
    timestamp = time.time()

    #  get the inertial data from the dualsense controller
    inertial_data = []
    start_time = time.time()
    session_id = 0
    
    while (time.time() - start_time) * 1000 < collection_duration:
        current_time_num = time.time()
        current_time = time.strftime("%Y%m%d-%H%M%S-") + "{:04d}".format(int((current_time_num % 1) * 10000))
        # Get sensor data from dualsense
        gyro = dualsense.state.gyro
        accel = dualsense.state.accelerometer
        
        # Create a data point
        data_point = [
            current_time,
            gyro.Pitch, gyro.Yaw, gyro.Roll,
            accel.X, accel.Y, accel.Z,
            session_id,
            label
        ]

        # update the data point in the console in one line 
        print(data_point, end='\r')

        #  append the data point to the inertial data
        inertial_data.append(data_point)
        
        # Update session_id every session_time milliseconds
        if (current_time_num - start_time) * 1000 // session_time > session_id:
            session_id += 1
            
        time.sleep(0.001)  # Small delay to prevent overwhelming the controller
    
    #  save the inertial data to a csv file
    df = pd.DataFrame(inertial_data, columns=['timestamp', 'gyroscope_pitch', 'gyroscope_yaw', 'gyroscope_roll', 'accelerometer_x', 'accelerometer_y', 'accelerometer_z','session_id','label'])
    
    
    #  save the dataframe to a csv file
    df.to_csv(f'inertial_data_{label}_{timestamp}.csv', index=False)
    print(f'inertial_data_{label}_{timestamp}.csv saved')

    dualsense.close()



def main():
    # Get label from command line argument
    if len(sys.argv) != 2:
        print("Usage: python data_collection.py <label>")
        print("Label must be either 'table' or 'hand'")
        sys.exit(1)
        
    label = sys.argv[1].lower()
    
    if label not in ['table', 'hand']:
        print("Error: Label must be either 'table' or 'hand'")
        print("Usage: python data_collection.py <label>")
        sys.exit(1)
        
    simple_data_collection(label=label)


if __name__ == "__main__":
    main()
