import time
import numpy as np
import pandas as pd
import pydualsense as ds


#  this function will collect data from the dualsense controller only about the inertial data( gyroscope and accelerometer, save them in a csv file, with the timestamp of the data collection 
def simple_data_collection(label: str, session_time: int = 500):
    # parameters:
    # label: the label of the data collection
    # session_time: the time segment of the data collection in milliseconds

    dualsense = ds.pydualsense()
    dualsense.init()    

    #  get the timestamp of the data collection
    timestamp = time.time()

    #  get the inertial data from the dualsense controller
    inertial_data = []

    #  save the inertial data to a csv file
    df = pd.DataFrame(inertial_data, columns=['timestamp', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z', 'accelerometer_x', 'accelerometer_y', 'accelerometer_z','session_id','label'])
    
    #  save the dataframe to a csv file
    df.to_csv(f'inertial_data_{label}.csv', index=False)


    pass



def main():
    simple_data_collection()


if __name__ == "__main__":
    main()
