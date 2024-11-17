import pydualsense as ds 
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import plotly.graph_objects as go
from scipy.signal import spectrogram
import time
import plotly.io as pio
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore



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



def show_audio_time_freq_realtime_pyqt(mic_index=None, duration=30, rate=48000, chunk=2048):
    """Real-time audio visualization using PyQtGraph"""
    app = pg.mkQApp()
    
    # Create window with GraphicsLayoutWidget
    win = pg.GraphicsLayoutWidget()

    # get the device name
    pa = pyaudio.PyAudio()
    device_info = pa.get_device_info_by_index(mic_index)
    device_name = device_info['name']

    win.setWindowTitle(f'Real-time Audio Analysis - {device_name}')
    win.resize(1200, 800)
    
    # Create plots
    p1 = win.addPlot(row=0, col=0)
    p1.setLabel('left', "Amplitude")
    p1.setLabel('bottom', "Time", units='s')
    
    p2 = win.addPlot(row=1, col=0)
    p2.setLabel('left', "Frequency", units='Hz')
    p2.setLabel('bottom', "Time", units='s')
    p2.setLogMode(y=True)  # Log scale for frequency
    p2.setYRange(20, 24000)  # Changed minimum to 20Hz due to log scale
    
    # Add frequency ticks
    ticks = [20, 50, 100, 200, 500, 1000, 2000, 4000, 8000, 12000, 16000, 20000, 24000]
    p2.getAxis('left').setTicks([[(v, f'{v}') for v in ticks]])
    
    # Initialize data
    time_curve = p1.plot(pen='y')
    img = pg.ImageItem()
    p2.addItem(img)
    
    # Set up colormap
    colormap = pg.colormap.get('viridis')
    img.setColorMap(colormap)
    
    # Add colorbar
    colorbar = pg.ColorBarItem(
        values=(-100, 0),
        colorMap=colormap,
        label='Magnitude (dB)',
        limits=(-100, 0)
    )
    colorbar.setImageItem(img)
    win.addItem(colorbar, row=1, col=1)  # Add colorbar to the right of spectrogram
    
    # Calculate scales
    freq_scale = np.linspace(0, 24000, chunk//2 + 1)
    time_scale = np.arange(100) * chunk/rate
    
    # Set the transform for proper scaling
    tr = QtGui.QTransform()
    tr.scale(chunk/rate, 24000/(chunk//2))
    img.setTransform(tr)
    
    # Set position to fill the plot
    img.setPos(0, 0)  # Start from origin
    
    # Set up audio buffer and processing
    buffer_size = chunk * 4
    audio_buffer = np.zeros(buffer_size, dtype=np.int16)
    spec_data = np.zeros((chunk//2 + 1, 100))
    
    # Audio callback
    def audio_callback(in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        audio_buffer[:-frame_count] = audio_buffer[frame_count:]
        audio_buffer[-frame_count:] = audio_data
        return (in_data, pyaudio.paContinue)
    
    # Update function
    def update():
        nonlocal spec_data
        
        # Get latest audio data
        latest_data = audio_buffer[-chunk:]
        
        # Update time domain
        time_curve.setData(np.arange(chunk) / rate, latest_data)
        
        # Update spectrogram
        fft_data = np.fft.rfft(latest_data * np.hanning(chunk))
        magnitude_db = 20 * np.log10(np.abs(fft_data) + 1e-10)
        
        # Change the roll direction and data assignment
        spec_data = np.roll(spec_data, -1, axis=1)  # Roll horizontally
        spec_data[:, -1] = magnitude_db[::-1]  # Flip the frequency data vertically
        
        # Update image
        img.setImage(spec_data.T, levels=(-100, 0))  # Transpose the data for correct orientation
    
    # Set up audio stream
    pa = pyaudio.PyAudio()
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
    
    # Set up timer for updates
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(30)  # 30ms update interval
    
    # Show window and start
    win.show()
    app.exec()
    
    # Cleanup
    stream.stop_stream()
    stream.close()
    pa.terminate()



def main():
    list_audio_devices()
    show_audio_time_freq_realtime_pyqt(mic_index=1, duration=30, rate=48000, chunk=2048)


# Example usage:
if __name__ == "__main__":
    main()
    
