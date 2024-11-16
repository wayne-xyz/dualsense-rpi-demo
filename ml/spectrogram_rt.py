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

def show_audio_time_freq_realtime(mic_index=None, duration=30, rate=48000, chunk=2048):
    """Show real-time time-domain and time-frequency (spectrogram) plots."""
    try:
        pa = pyaudio.PyAudio()
        
        # Validate mic_index
        try:
            pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=chunk
            ).close()
            print(f"Mic index {mic_index} is valid")
        except Exception as e:
            print(f"Mic index {mic_index} is not valid: {e}")
            return None
        
        device_info = pa.get_device_info_by_index(mic_index)
        print(f"Device name: {device_info['name']}")
        
        # Initialize plot
        plt.ion()
        fig, (ax_time, ax_spec) = plt.subplots(2, 1, figsize=(12, 12))
        
        # Time domain plot
        time_data = np.zeros(chunk)
        line_time, = ax_time.plot(np.arange(chunk) / rate, time_data)
        ax_time.set_title('Time Domain')
        ax_time.set_ylabel('Amplitude')
        ax_time.set_ylim(-32768, 32767)
        ax_time.grid(True)
        
        # Spectrogram plot
        spec_segments = 100  # Number of time segments to display
        freqs = np.fft.rfftfreq(chunk, 1/rate)
        spec_data = np.zeros((len(freqs), spec_segments))
        
        # Create initial spectrogram
        im = ax_spec.pcolormesh(np.arange(spec_segments) * chunk/rate, 
                               freqs, 
                               spec_data,
                               shading='gouraud',
                               cmap='viridis',
                               vmin=-100,
                               vmax=0)
        
        plt.colorbar(im, ax=ax_spec, label='Magnitude [dB]')
        ax_spec.set_title('Time-Frequency Domain (Spectrogram)')
        ax_spec.set_xlabel('Time [s]')
        ax_spec.set_ylabel('Frequency [Hz]')
        ax_spec.set_yscale('log')
        ax_spec.set_ylim(20, rate/2)
        
        # Create audio buffer
        buffer_size = chunk * 4
        audio_buffer = np.zeros(buffer_size, dtype=np.int16)
        
        # Audio stream with callback
        def audio_callback(in_data, frame_count, time_info, status):
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_buffer[:-frame_count] = audio_buffer[frame_count:]
            audio_buffer[-frame_count:] = audio_data
            return (in_data, pyaudio.paContinue)
        
        # Open stream with callback
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            input_device_index=mic_index,
            frames_per_buffer=chunk,
            stream_callback=audio_callback,
            start=True
        )
        
        print("\nRecording and plotting in realtime...")
        start_time = time.time()
        last_update = 0
        update_interval = 0.03  # 30ms update interval
        
        try:
            while time.time() - start_time < duration:
                current_time = time.time()
                
                if current_time - last_update >= update_interval:
                    # Get latest chunk of data
                    latest_data = audio_buffer[-chunk:]
                    
                    # Time domain update
                    line_time.set_ydata(latest_data)
                    
                    # Spectrogram update
                    fft_data = np.fft.rfft(latest_data * np.hanning(chunk))
                    magnitude_db = 20 * np.log10(np.abs(fft_data) + 1e-10)
                    
                    # Roll spectrogram data and update
                    spec_data = np.roll(spec_data, -1, axis=1)
                    spec_data[:, -1] = magnitude_db
                    
                    # Update spectrogram
                    im.set_array(spec_data.ravel())
                    
                    # Efficient plot update
                    fig.canvas.draw_idle()
                    fig.canvas.flush_events()
                    
                    last_update = current_time
                
                plt.pause(0.001)
                
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


def main():
    list_audio_devices()
    show_audio_time_freq_realtime(mic_index=1, duration=30, rate=48000, chunk=2048)


# Example usage:
if __name__ == "__main__":
    main()
    
