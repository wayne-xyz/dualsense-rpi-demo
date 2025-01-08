# a script to test the collecte.py script 


import collecte
import pydualsense as ds
import time



def test_start_vibration_pattern():
    dualsense = ds.pydualsense()
    dualsense.init()
    
    try:
        print("Testing pattern 1 (half intensity), for 2 seconds")
        stop_event, thread = collecte.start_vibration_pattern(1, dualsense)
        time.sleep(2)
        collecte.stop_vibration_pattern(dualsense, stop_event, thread)
        
        time.sleep(1)
        
        print("Testing pattern 2 (full intensity), for 2 seconds")
        stop_event, thread = collecte.start_vibration_pattern(2, dualsense)
        time.sleep(2)
        collecte.stop_vibration_pattern(dualsense, stop_event, thread)
        
        time.sleep(1)
        
        print("Testing pattern 3 (sine wave), for 5 seconds")
        stop_event, thread = collecte.start_vibration_pattern(3, dualsense)
        time.sleep(5)
        collecte.stop_vibration_pattern(dualsense, stop_event, thread)
        time.sleep(1)  # wait for stop fully executed then terminate the thread, or the controller will be disconnected whil it's still vib
        
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        dualsense.close()
        print("Controller disconnected")

def main():
    print("=== Testing Vibration Patterns ===")
    test_start_vibration_pattern()


if __name__ == "__main__":
    main()
