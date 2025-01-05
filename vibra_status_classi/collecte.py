# this python function using for collect data from the sensor to the csv data from the ps5 controller.



import argparse
import time
import numpy as np
import os
import logging
import pydualsense as ds

# print env info:
import sys
print(f"sys.platform: {sys.platform}")
# import hidapi
# print(hidapi.__version__)


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
    "category_rows": 1000, # 1000 rows per vibration status and label
    "session_rows":50 # for the svm model, divide the data into session with 50 rows in each category
}

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


def collect_data(data_fields=data_fields, vib_pattern=vib_pattern, rule1=rule1, label=0, person_id=0, pattern_id=0):
    print(f"Parameters: person_id={person_id}, pattern_id={pattern_id}, label={label}")
    # Add your data collection logic here
    pass


def main():
    # Add your main logic here
    pass



if __name__ == "__main__":
    print("========start collect data========")
    #  using the command line argument to get the label, person_id, pattern_id
    # example: python collecte.py --label 0 --person_id 0 --pattern_id 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", type=int, default=0)
    parser.add_argument("--person_id", type=int, default=0)
    parser.add_argument("--pattern_id", type=int, default=0)
    args = parser.parse_args()
    collect_data(label=args.label, person_id=args.person_id, pattern_id=args.pattern_id)
    print("========end collect data========")
