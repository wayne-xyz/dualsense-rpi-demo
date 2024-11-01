# using the model to predict the gesture

import tensorflow as tf
import pydualsense as ds
import time
import os
import joblib
import pandas as pd
import numpy as np

model = tf.keras.models.load_model('gesture_model.keras')
scaler = joblib.load('scaler.save')
label_encoder = joblib.load('label_encoder.save')



def predict_controller_realtime(model):
    dualsense = ds.pydualsense()
    dualsense.init()

    # Define feature names to match training data
    feature_names = ['gyroscope_pitch', 'gyroscope_yaw', 'gyroscope_roll',
                    'accelerometer_x', 'accelerometer_y', 'accelerometer_z']

    sequence_length = model.input_shape[1]
    print(f"Sequence length: {sequence_length}")
    sequence_data = []

    print("Press Ctrl+C to exit...")
    try:
        while True:
            # Get the data from the controller
            data = [dualsense.state.gyro.Pitch, dualsense.state.gyro.Yaw, dualsense.state.gyro.Roll,
                   dualsense.state.accelerometer.X, dualsense.state.accelerometer.Y, dualsense.state.accelerometer.Z]
            sequence_data.append(data)
            
            if len(sequence_data) == sequence_length:
                # Convert to DataFrame with correct feature names
                df = pd.DataFrame(sequence_data, columns=feature_names)
                
                # Scale the sequence data
                scaled_data = scaler.transform(df)
                
                # Reshape for model input (add batch dimension)
                model_input = scaled_data.reshape(1, sequence_length, 6)
                
                # Get prediction
                prediction = model.predict(model_input, verbose=0)
                
                # Convert prediction to label
                predicted_label = label_encoder.inverse_transform([prediction.argmax()])[0]
                print(f"Predicted gesture: {predicted_label}")
                
                # Clear sequence for next prediction
                sequence_data = []
                
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\nExiting application...")
        dualsense.close()
        exit()


def check_saved_files():
    files_to_check = [
        'gesture_model.keras',
        'scaler.save',
        'label_encoder.save'
    ]
    
    print("Checking for saved files:")
    missing_files = []
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✓ Found {file}")
        else:
            print(f"✗ Missing {file}")
            missing_files.append(file)
    
    if missing_files:
        print("\nError: Missing required files:")
        for file in missing_files:
            print(f"- {file}")
        print("\nPlease ensure all required files are present before running.")
        exit(1)
    
    print("\nAll required files found!")
    return True



def main():
    if check_saved_files():
        predict_controller_realtime(model)

if __name__ == "__main__":
    main()


