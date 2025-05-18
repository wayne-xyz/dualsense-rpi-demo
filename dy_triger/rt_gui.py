import pydualsense as ds
import time


# shows the trigger positions plot real time

def real_time_plot():
    controller = ds.pydualsense()
    controller.init()

    triggerL = controller.triggerL
    triggerR = controller.triggerR

    start_time = time.time()
    duration = 30  # 30 seconds
    
    print(f"Starting data collection for {duration} seconds...")
    
    while time.time() - start_time < duration:
        print(f"L2: {controller.state.L2}, R2: {controller.state.R2}")
        time.sleep(0.1)
    
    elapsed_time = time.time() - start_time
    print(f"Data collection completed. Duration: {elapsed_time:.2f} seconds")
    
    controller.close()



    
def main():
    real_time_plot()

if __name__ == "__main__":
    main()

