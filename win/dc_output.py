import numpy as np
import time
import sys
from pydualsense import pydualsense
import pyaudio
import wave
from pydualsense.enums import TriggerModes
import threading

def sine_wave_feedback():
    dualsense = pydualsense()
    dualsense.init()

    # Play a smooth feedback using the haptic feedback by a sine wave for 1 minute
    duration = 30  # 1 minute
    start_time = time.time()

    while time.time() - start_time < duration:
        # Calculate the sine value (-1 to 1)
        t = time.time() - start_time
        sine_value = np.sin(2 * np.pi * t)
        
        # Convert sine value to motor intensity (0 to 255)
        # Use abs() to ensure positive values, and multiply by 127.5 to max out at 255
        force = int(abs(sine_value) * 127.5)
        
        # Ensure force never exceeds 255
        force = min(force, 255)
        
        # Set the motor intensity for both motors
        dualsense.setLeftMotor(force)
        dualsense.setRightMotor(force)
        
        # Sleep for a short duration to control update rate
        time.sleep(0.001)  # This gives approximately 1000 updates per second

    # Turn off both motors at the end
    dualsense.setLeftMotor(0)
    dualsense.setRightMotor(0)
    dualsense.close()


def sound_haptic_feedback():
    dualsense = pydualsense()
    dualsense.init()

    # Open the WAV file
    wave_file = "footsteps-1.wav"
    wf = wave.open(wave_file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Define callback function to process audio data and set haptic feedback
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        
        if len(data) == 0:  # End of file
            return (data, pyaudio.paComplete)
        
        # Convert byte data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate RMS (Root Mean Square) as a measure of sound level
        squared_data = np.square(audio_data.astype(np.float64))
        mean_squared = np.mean(squared_data)
        
        if mean_squared > 0:
            rms = np.sqrt(mean_squared)
            # Normalize RMS to 0-255 range for haptic feedback
            max_int16 = 32767  # Max value for 16-bit audio
            normalized_level = int(min(255, max(0, (rms / max_int16) * 255))/2)
        else:
            normalized_level = 0
        
        # Set haptic feedback
        dualsense.setLeftMotor(normalized_level)
        dualsense.setRightMotor(normalized_level)
        
        return (data, pyaudio.paContinue)

    # Open stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    # Start the stream
    stream.start_stream()

    # Wait for the stream to finish
    while stream.is_active():
        time.sleep(0.1)

    # Clean up
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    dualsense.close()



def trigger_haptic_feedback():
    dualsense = pydualsense()
    dualsense.init()

    start_time = time.time()
    duration = 30  # Run for 30 seconds

    try:
        while time.time() - start_time < duration:
            state = dualsense.state
            trigger_movement_L2 = state.L2
            trigger_movement_R2 = state.R2
            intensity_L2 = int(trigger_movement_L2 )  # Scale to 0-255 range
            intensity_R2 = int(trigger_movement_R2 )  # Scale to 0-255 range
            
            # Print remaining time
            remaining_time = int(duration - (time.time() - start_time))
            print(f"Remaining time: {remaining_time} seconds", end='\r')
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        dualsense.setLeftMotor(0)
        dualsense.setRightMotor(0)
        dualsense.close()
        print("\nHaptic feedback session ended.")


if __name__ == "__main__":
    #  two modes: sine wave feedback and sound haptic with parameter: sin sound when using python xxxx.py sin  python xxx.py sound
    if len(sys.argv) > 1:
        if sys.argv[1] == "sin":
            sine_wave_feedback()
        elif sys.argv[1] == "sound":
            sound_haptic_feedback()
        elif sys.argv[1] == "trigger":
            trigger_haptic_feedback()
    else:   
        print("Usage: python xxxx.py sin/sound/trigger")


