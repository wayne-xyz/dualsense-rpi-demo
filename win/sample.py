from pydualsense import pydualsense
import time
import sys
import copy



def sample_rate_test():
    

    dualsense = pydualsense()
    dualsense.init()

    print("Checking accelerometer polling rate. Move the controller...")
    print("This test will run for 5 seconds.")

    start_time = time.time()
    end_time = start_time + 5  # Run for 5 seconds
    last_accel = None
    state_changes = 0
    
    try:
        while time.time() < end_time:
            current_accel = (
                dualsense.state.accelerometer.X,
                dualsense.state.accelerometer.Y,
                dualsense.state.accelerometer.Z
            )
            
            if last_accel is not None and current_accel != last_accel:
                state_changes += 1

            last_accel = current_accel
            time.sleep(0.001)  # Sleep for 1ms to avoid overwhelming the CPU

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    finally:
        dualsense.close()

    elapsed_time = time.time() - start_time
    polling_rate = state_changes / elapsed_time if elapsed_time > 0 else 0

    print(f"\nTest completed.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Accelerometer state changes detected: {state_changes}")
    print(f"Estimated accelerometer polling rate: {polling_rate:.2f} Hz")


if __name__ == "__main__":
    sample_rate_test()

