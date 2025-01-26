import numpy as np
from scipy.io import wavfile

def generate_sweep_file(filename, start_freq, end_freq, duration, volume=0.5, sample_rate=48000):
    """
    Generate and save a frequency sweep audio file that goes from start_freq to end_freq and back.
    
    Args:
        filename (str): Output filename (.wav)
        start_freq (float): Starting frequency in Hz
        end_freq (float): Ending frequency in Hz
        duration (float): Total duration of the sweep in seconds (both directions)
        volume (float): Amplitude scaling (0.0 to 1.0)
        sample_rate (int): Sample rate in Hz
    """
    # Calculate half duration for each sweep direction
    half_duration = duration / 2
    
    # Create time arrays for both halves
    t_half = np.linspace(0, half_duration, int(sample_rate * half_duration))
    
    # Generate logarithmic frequency sweeps
    freq_up = np.exp(np.log(start_freq) + (np.log(end_freq/start_freq) * t_half/half_duration))
    freq_down = np.exp(np.log(end_freq) + (np.log(start_freq/end_freq) * t_half/half_duration))
    
    # Combine frequency arrays
    freq = np.concatenate((freq_up, freq_down))
    
    # Calculate phase and generate sine wave
    phase = 2 * np.pi * freq.cumsum() / sample_rate
    sweep = np.sin(phase)
    
    # Apply volume and convert to 32-bit float
    audio_data = (sweep * volume).astype(np.float32)
    
    # Save to WAV file
    wavfile.write(filename, sample_rate, audio_data)
    print(f"Sweep saved to {filename}")

# Example usage:
generate_sweep_file("input_sweep.wav", 
                   start_freq=20, 
                   end_freq=2000, 
                   duration=20, 
                   volume=1)