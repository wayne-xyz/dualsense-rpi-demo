# this script is for using the invesitgation of the LRA linear resonat actuator 

import sys
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QSpinBox, QHBoxLayout
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
import pyqtgraph as pg
import pydualsense as ds
from scipy.fft import fft, fftfreq

class DataCollector(QThread):
    """Thread for high-frequency data collection"""
    data_ready = pyqtSignal(float, float, float, float)  # time, x, y, z
    
    def __init__(self, dualsense, sample_rate=500):
        super().__init__()
        self.dualsense = dualsense
        self.running = False
        self.sample_rate = sample_rate
        self.sleep_time = 1.0 / sample_rate
        self.start_time = None
    
    def run(self):
        self.running = True
        self.start_time = time.time()
        
        while self.running:
            start_loop = time.time()
            
            # Get sensor data
            acc = self.dualsense.state.accelerometer
            current_time = time.time() - self.start_time
            
            # Emit the data
            self.data_ready.emit(current_time, acc.X, acc.Y, acc.Z)
            
            # Precise timing control
            elapsed = time.time() - start_loop
            if elapsed < self.sleep_time:
                time.sleep(self.sleep_time - elapsed)
    
    def stop(self):
        self.running = False

class VibrationController(QThread):
    """Thread for controlling vibration patterns"""
    def __init__(self, dualsense):
        super().__init__()
        self.dualsense = dualsense
        self.running = False
        self.pattern = None
        self.frequency = 1.0  # Default 1Hz
        self.intensity = 255  # Default full intensity
        self.pulse_on_time = 0.1  # 100ms for pulse on
        self.pulse_off_time = 0.1  # 100ms for pulse off
    
    def set_pattern(self, pattern, frequency=1.0, intensity=255, pulse_on_time=0.1, pulse_off_time=0.1):
        self.pattern = pattern
        self.frequency = frequency
        self.intensity = intensity
        self.pulse_on_time = pulse_on_time
        self.pulse_off_time = pulse_off_time
    
    def run(self):
        self.running = True
        start_time = time.time()
        
        while self.running:
            if self.pattern == 'constant':
                self.dualsense.setLeftMotor(self.intensity)
                self.dualsense.setRightMotor(self.intensity)
                time.sleep(0.001)
            elif self.pattern == 'sine':
                t = time.time() - start_time
                value = int(self.intensity/2 * (np.sin(2 * np.pi * self.frequency * t) + 1))
                self.dualsense.setLeftMotor(value)
                self.dualsense.setRightMotor(value)
                time.sleep(0.001)
            elif self.pattern == 'pulse':
                # Pulse ON
                self.dualsense.setLeftMotor(self.intensity)
                self.dualsense.setRightMotor(self.intensity)
                time.sleep(self.pulse_on_time)
                
                # Pulse OFF
                self.dualsense.setLeftMotor(0)
                self.dualsense.setRightMotor(0)
                time.sleep(self.pulse_off_time)
    
    def stop(self):
        self.running = False
        self.dualsense.setLeftMotor(0)
        self.dualsense.setRightMotor(0)

class AccelerometerPlotWindow(QMainWindow):
    """Main window for accelerometer visualization"""
    def __init__(self, dualsense):
        super().__init__()
        self.dualsense = dualsense
        self.setup_ui()
        self.setup_data_collection()
        self.setup_vibration_control()
    
    def setup_ui(self):
        self.setWindowTitle("LRA Investigation Tool")
        self.setGeometry(100, 100, 1000, 600)  # Reduced window size
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Controls at the top
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Vibration pattern selector
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(['none', 'constant', 'sine', 'pulse'])
        control_layout.addWidget(QLabel("Vibration Pattern:"))
        control_layout.addWidget(self.pattern_combo)
        
        # Pulse timing controls
        pulse_control = QWidget()
        pulse_layout = QVBoxLayout(pulse_control)
        
        # Pulse ON time
        self.pulse_on_spin = QSpinBox()
        self.pulse_on_spin.setRange(1, 1000)
        self.pulse_on_spin.setValue(100)
        pulse_layout.addWidget(QLabel("Pulse ON time (ms):"))
        pulse_layout.addWidget(self.pulse_on_spin)
        
        # Pulse OFF time
        self.pulse_off_spin = QSpinBox()
        self.pulse_off_spin.setRange(1, 1000)
        self.pulse_off_spin.setValue(100)
        pulse_layout.addWidget(QLabel("Pulse OFF time (ms):"))
        pulse_layout.addWidget(self.pulse_off_spin)
        
        control_layout.addWidget(pulse_control)
        
        # Start/Stop button
        self.start_stop_btn = QPushButton("Start")
        self.start_stop_btn.clicked.connect(self.toggle_data_collection)
        control_layout.addWidget(self.start_stop_btn)
        
        layout.addWidget(control_widget)
        
        # XYZ Accelerometer plot
        self.time_plot = pg.PlotWidget()
        self.time_plot.setLabel('left', 'Acceleration', units='m/s²')
        self.time_plot.setLabel('bottom', 'Time', units='s')
        self.time_plot.addLegend()
        self.time_plot.showGrid(x=True, y=True)
        
        layout.addWidget(self.time_plot)
        
        # Initialize curves
        self.time_curves = {
            'x': self.time_plot.plot(pen='r', name='X-axis'),
            'y': self.time_plot.plot(pen='g', name='Y-axis'),
            'z': self.time_plot.plot(pen='b', name='Z-axis')
        }
        
        # Data buffers
        self.buffer_size = 500
        self.data_buffers = {
            't': np.zeros(self.buffer_size),
            'x': np.zeros(self.buffer_size),
            'y': np.zeros(self.buffer_size),
            'z': np.zeros(self.buffer_size)
        }
        self.data_index = 0
    
    def setup_data_collection(self):
        self.data_collector = DataCollector(self.dualsense)
        self.data_collector.data_ready.connect(self.update_plot)
    
    def setup_vibration_control(self):
        self.vibration_controller = VibrationController(self.dualsense)
        self.pattern_combo.currentTextChanged.connect(self.change_vibration_pattern)
    
    def update_plot(self, t, x, y, z):
        # Update time domain buffers
        self.data_buffers['t'][self.data_index] = t
        self.data_buffers['x'][self.data_index] = x
        self.data_buffers['y'][self.data_index] = y
        self.data_buffers['z'][self.data_index] = z
        
        self.data_index = (self.data_index + 1) % self.buffer_size
        
        # Update XYZ plot
        for axis in ['x', 'y', 'z']:
            self.time_curves[axis].setData(
                self.data_buffers['t'],
                self.data_buffers[axis]
            )
        
        # Auto-range occasionally
        if self.data_index % 50 == 0:
            self.time_plot.enableAutoRange()
    
    def change_vibration_pattern(self, pattern):
        if pattern == 'none':
            self.vibration_controller.stop()
        else:
            # Get pulse timing values if in pulse mode
            pulse_on = self.pulse_on_spin.value() / 1000.0  # Convert to seconds
            pulse_off = self.pulse_off_spin.value() / 1000.0  # Convert to seconds
            
            self.vibration_controller.set_pattern(
                pattern,
                pulse_on_time=pulse_on,
                pulse_off_time=pulse_off
            )
            if not self.vibration_controller.isRunning():
                self.vibration_controller.start()
    
    def toggle_data_collection(self):
        if self.data_collector.isRunning():
            self.data_collector.stop()
            self.start_stop_btn.setText("Start")
        else:
            self.data_collector.start()
            self.start_stop_btn.setText("Stop")
    
    def closeEvent(self, event):
        self.data_collector.stop()
        self.vibration_controller.stop()
        self.dualsense.close()
        event.accept()

def main():
    # Initialize controller
    dualsense = ds.pydualsense()
    dualsense.init()
    print("Controller initialized.")
    
    # Create and run application
    app = QApplication(sys.argv)
    window = AccelerometerPlotWindow(dualsense)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()