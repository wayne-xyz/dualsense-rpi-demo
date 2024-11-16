import pydualsense as ds 
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import plotly.graph_objects as go
from scipy.signal import spectrogram
import time
import plotly.io as pio




def search_dualsense_mic():
    """Search for DualSense microphone and verify device functionality"""
    try:
        pa = pyaudio.PyAudio()
        dualsense_index = None
        
        # First find all input devices
        for i in range(pa.get_device_count()):
            dev = pa.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                if "dualsense" in dev['name'].lower():
                    # Try to open a test stream to verify device works
                    try:
                        test_stream = pa.open(
                            format=pyaudio.paInt16,
                            channels=1,
                            rate=int(dev['defaultSampleRate']),
                            input=True,
                            input_device_index=i,
                            frames_per_buffer=1024
                        )
                        test_stream.close()
                        print(f"Found working DualSense device: {dev['name']}")
                        print(f"Device index: {i}")
                        print(f"Sample rate: {int(dev['defaultSampleRate'])} Hz")
                        print(f"Input channels: {dev['maxInputChannels']}")
                        dualsense_index = i
                        break
                    except Exception:
                        print(f"Found DualSense device at index {i} but it appears non-functional")
                        continue
        
        pa.terminate()
        
        if dualsense_index is None:
            print("No working DualSense microphone found")
            return None
            
        return dualsense_index
        
    except Exception as e:
        print(f"Error searching for DualSense mic: {str(e)}")
        return None
    


def get_dualsense_audio_realtime_matplotlib(duration=10, rate=48000, chunk=1024,mic_index=None):
    """Capture and plot audio in real-time with Matplotlib"""
    try:
        # Initialize PyAudio
        pa = pyaudio.PyAudio()
        
        # Find DualSense mic
        if mic_index is None:
            mic_index = search_dualsense_mic()
            if mic_index is None:
                print("Could not find DualSense microphone!")
                return None
        print(f"current mic_index: {mic_index}")
        
        # Get device info
        device_info = pa.get_device_info_by_index(mic_index)
        print(f"\nUsing device: {device_info['name']}")
        
        # Set up the plot
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Buffer for audio data
        buffer_size = rate  # 1 second buffer
        audio_buffer = np.zeros(buffer_size)
        
        # Create initial spectrogram
        Pxx, freqs, bins, im = ax.specgram(
            audio_buffer,
            NFFT=1024,
            Fs=rate,
            noverlap=512,
            cmap='viridis',
            mode='magnitude',
            scale='dB',
            vmin=-100,
            vmax=0
        )
        
        plt.colorbar(im, label='Intensity [dB]')
        ax.set_title('Real-Time Audio Spectrogram')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Frequency [Hz]')
        ax.set_ylim(20, rate/2)  # Set frequency range
        ax.set_yscale('log')     # Log scale for frequency
        
        # Open stream
        try:
            stream = pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=chunk
            )
        except OSError as e:
            print(f"Error opening stream: {e}")
            pa.terminate()
            return None
            
        print("\nRecording and plotting in realtime...")
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Read audio data
                data = stream.read(chunk, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                
                # Update buffer
                audio_buffer = np.roll(audio_buffer, -len(audio_chunk))
                audio_buffer[-len(audio_chunk):] = audio_chunk
                
                # Clear previous plot
                ax.clear()
                
                # Update spectrogram
                Pxx, freqs, bins, im = ax.specgram(
                    audio_buffer,
                    NFFT=1024,
                    Fs=rate,
                    noverlap=512,
                    cmap='viridis',
                    mode='magnitude',
                    scale='dB',
                    vmin=-100,
                    vmax=0
                )
                
                # Restore plot settings
                ax.set_title('Real-Time Audio Spectrogram')
                ax.set_xlabel('Time [s]')
                ax.set_ylabel('Frequency [Hz]')
                ax.set_ylim(20, rate/2)
                ax.set_yscale('log')
                
                # Force update
                fig.canvas.draw()
                fig.canvas.flush_events()
                
        except Exception as e:
            print(f"Error during recording: {e}")
            raise e  # Show full error details
        
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            plt.ioff()
            plt.close()
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    

# using scipy.signal.spectrogram to show the spectrogram

def get_dualsense_audio_realtime_scipy(duration=10, rate=48000, chunk=1024, mic_index=None):
    """Display real-time spectrogram using scipy.signal"""
    try:
        if mic_index is None:
            mic_index = search_dualsense_mic()
            if mic_index is None:
                print("Could not find DualSense microphone!")
                return None
        
        print(f"current mic_index: {mic_index}")

        # Initialize plot
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Increase buffer size for smoother display
        buffer_duration = 2  # 2 seconds of audio buffer
        buffer_size = int(rate * buffer_duration)
        audio_buffer = np.zeros(buffer_size)
        
        # Initial spectrogram calculation
        f, t, Sxx = spectrogram(
            audio_buffer,
            fs=rate,
            nperseg=1024,
            noverlap=768,
            nfft=2048,
            window='hann'
        )
        
        # Create initial plot
        im = ax.pcolormesh(t, f, np.zeros_like(Sxx),
                          cmap='viridis',
                          shading='gouraud',
                          vmin=-100,
                          vmax=0)
        
        plt.colorbar(im, label='Intensity [dB]')
        ax.set_title('Real-Time Audio Spectrogram')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Frequency [Hz]')
        
        # Set frequency range
        min_freq = 20
        max_freq = 24000  # Extended range to 24kHz
        ax.set_yscale('log')
        ax.set_ylim(min_freq, max_freq)
        
        # Add frequency ticks
        freq_ticks = [20, 50, 100, 200, 500, 1000, 2000, 4000, 8000, 12000, 16000, 20000, 24000]
        ax.set_yticks(freq_ticks)
        ax.set_yticklabels([f'{f:g}' for f in freq_ticks])
        
        # Open audio stream
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=chunk,
            stream_callback=None,
            start=True
        )

        print("\nRecording and plotting in realtime...")
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                try:
                    data = stream.read(chunk, exception_on_overflow=False)
                    audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                    
                    # Update buffer with overlap
                    audio_buffer = np.roll(audio_buffer, -len(audio_chunk))
                    audio_buffer[-len(audio_chunk):] = audio_chunk
                    
                    # Calculate spectrogram with updated buffer
                    f, t, Sxx = spectrogram(
                        audio_buffer,
                        fs=rate,
                        nperseg=1024,
                        noverlap=768,
                        nfft=2048,
                        window='hann'
                    )
                    
                    # Convert to dB scale
                    Sxx_db = 10 * np.log10(Sxx + 1e-10)
                    Sxx_db = np.clip(Sxx_db, -100, 0)
                    
                    # Update plot
                    im.set_array(Sxx_db.T.ravel()) 
                    
                    # Force update with reduced frequency
                    if time.time() % 0.1 < 0.05:  # Update every 100ms
                        fig.canvas.draw_idle()
                        fig.canvas.flush_events()
                    
                except IOError as e:
                    print(f"Warning: Buffer overflow - {e}")
                    continue

                plt.pause(0.01)  # Small pause

        except Exception as e:
            print(f"Error during recording: {e}")
            raise e
            
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            plt.ioff()
            plt.close()

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
        

# 
def list_audio_devices():
    """List all available audio devices"""
    p = pyaudio.PyAudio()
    info = []
    
    print("\nAvailable Audio Devices:")
    print("-" * 60)
    
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info['maxInputChannels'] > 0:  # Only show input devices
            print(f"Index: {i}")
            print(f"Name: {dev_info['name']}")
            print(f"Channels: {dev_info['maxInputChannels']}")
            print(f"Sample Rate: {dev_info['defaultSampleRate']}")
            print("-" * 60)
            info.append(dev_info)
    
    p.terminate()
    return info


def show_audio_frequency_realtime(mic_index=None, duration=30, rate=48000, chunk=2048):
    """Show real-time frequency line plot for a specific audio device"""
    try:
        # Check if mic_index is valid
        pa = pyaudio.PyAudio()
        try:
            stream = pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=chunk
            )
            stream.close()
            print(f"Mic index {mic_index} is valid")
        except Exception as e:
            print(f"Mic index {mic_index} is not valid: {e}")
            return None
        
        # Print device info
        device_info = pa.get_device_info_by_index(mic_index)
        print(f"Device name: {device_info['name']}")
        
        # Initialize plot
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate frequency bins
        freq_bins = np.fft.rfftfreq(chunk, 1/rate)
        
        # Create initial empty line plot
        line, = ax.plot(freq_bins, np.zeros_like(freq_bins))
        
        # Set up plot parameters
        ax.set_title(f'Real-Time Frequency Analysis - {device_info["name"]}')
        ax.set_xlabel('Frequency [Hz]')
        ax.set_ylabel('Magnitude [dB]')
        ax.set_xscale('log')
        ax.set_xlim(20, 20000)  # Audio frequency range
        ax.set_ylim(-100, 0)    # dB range
        ax.grid(True)
        
        # Add frequency ticks
        freq_ticks = [20, 50, 100, 200, 500, 1000, 2000, 4000, 8000, 12000, 16000, 20000]
        ax.set_xticks(freq_ticks)
        ax.set_xticklabels([f'{f:g}' for f in freq_ticks])
        
        # Open audio stream
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=chunk,
            start=True
        )
        
        print("\nRecording and plotting in realtime...")
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                try:
                    # Read audio data
                    data = stream.read(chunk, exception_on_overflow=False)
                    audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                    
                    # Compute FFT
                    fft_data = np.fft.rfft(audio_chunk * np.hanning(len(audio_chunk)))
                    
                    # Convert to magnitude in dB
                    magnitude_db = 20 * np.log10(np.abs(fft_data) + 1e-10)
                    
                    # Update line data
                    line.set_ydata(magnitude_db)
                    
                    # Update plot
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                    plt.pause(0.01)
                    
                except IOError as e:
                    print(f"Warning: Buffer overflow - {e}")
                    continue
                
        except Exception as e:
            print(f"Error during recording: {e}")
            raise e
            
        finally:
            # Cleanup
            stream.stop_stream()
            stream.close()
            pa.terminate()
            plt.ioff()
            plt.close()
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None



def main():
    list_audio_devices()
    show_audio_frequency_realtime(
        mic_index=2,     # Specify your device index
        duration=30,     # Run for 30 seconds
        rate=48000,      # Sample rate
        chunk=2048       # Buffer size
    )


# Example usage:
if __name__ == "__main__":
    main()
    
