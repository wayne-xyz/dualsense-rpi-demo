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
        self.setGeometry(100, 100, 1000, 800)  # Increased height for two plots
        
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
        
        # Sine wave controls
        sine_control = QWidget()
        sine_layout = QVBoxLayout(sine_control)
        
        # Frequency control
        self.frequency_spin = QSpinBox()
        self.frequency_spin.setRange(1, 100)  # 1-100 Hz
        self.frequency_spin.setValue(1)  # Default 1 Hz
        self.frequency_spin.setSuffix(" Hz")
        sine_layout.addWidget(QLabel("Sine Wave Frequency:"))
        sine_layout.addWidget(self.frequency_spin)
        
        # Initially hide sine controls
        sine_control.setVisible(False)
        self.sine_control_widget = sine_control  # Store reference
        
        control_layout.addWidget(sine_control)
        
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
        
        # Plot switch button
        self.plot_switch_btn = QPushButton("Show Magnitude")
        self.plot_switch_btn.clicked.connect(self.toggle_plot_view)
        control_layout.addWidget(self.plot_switch_btn)
        
        layout.addWidget(control_widget)
        
        # Create plots container
        plots_widget = QWidget()
        plots_layout = QVBoxLayout(plots_widget)
        
        # XYZ Accelerometer plot
        self.time_plot = pg.PlotWidget()
        self.time_plot.setLabel('left', 'Acceleration', units='m/s²')
        self.time_plot.setLabel('bottom', 'Time', units='s')
        self.time_plot.addLegend()
        self.time_plot.showGrid(x=True, y=True)
        plots_layout.addWidget(self.time_plot)
        
        # Magnitude plot
        self.magnitude_plot = pg.PlotWidget()
        self.magnitude_plot.setLabel('left', 'Magnitude', units='m/s²')
        self.magnitude_plot.setLabel('bottom', 'Time', units='s')
        self.magnitude_plot.showGrid(x=True, y=True)
        plots_layout.addWidget(self.magnitude_plot)
        
        # Initially hide magnitude plot
        self.magnitude_plot.hide()
        
        layout.addWidget(plots_widget)
        
        # Initialize curves for XYZ plot
        self.time_curves = {
            'x': self.time_plot.plot(pen='r', name='X-axis'),
            'y': self.time_plot.plot(pen='g', name='Y-axis'),
            'z': self.time_plot.plot(pen='b', name='Z-axis')
        }
        
        # Initialize curve for magnitude plot
        self.magnitude_curve = self.magnitude_plot.plot(
            pen=pg.mkPen('w', width=2),  # White, thicker line
            name='Magnitude'
        )
        
        # Data buffers
        self.buffer_size = 250
        self.data_buffers = {
            't': np.zeros(self.buffer_size),
            'x': np.zeros(self.buffer_size),
            'y': np.zeros(self.buffer_size),
            'z': np.zeros(self.buffer_size),
            'magnitude': np.zeros(self.buffer_size)
        }
        self.data_index = 0
        
        # Track current view state
        self.showing_xyz = True
        
        # Connect frequency change signal
        self.frequency_spin.valueChanged.connect(self.update_sine_frequency)
        # Connect pattern change to control visibility
        self.pattern_combo.currentTextChanged.connect(self.update_control_visibility)
    
    def setup_data_collection(self):
        self.data_collector = DataCollector(self.dualsense)
        self.data_collector.data_ready.connect(self.update_plot)
    
    def setup_vibration_control(self):
        self.vibration_controller = VibrationController(self.dualsense)
        self.pattern_combo.currentTextChanged.connect(self.change_vibration_pattern)
    
    def calculate_magnitude(self, x, y, z):
        """Calculate the magnitude from three axis components"""
        return np.sqrt(x**2 + y**2 + z**2)
    
    def update_plot(self, t, x, y, z):
        # Update buffers
        self.data_buffers['t'][self.data_index] = t
        self.data_buffers['x'][self.data_index] = x
        self.data_buffers['y'][self.data_index] = y
        self.data_buffers['z'][self.data_index] = z
        
        # Calculate magnitude
        magnitude = self.calculate_magnitude(x, y, z)
        self.data_buffers['magnitude'][self.data_index] = magnitude
        
        self.data_index = (self.data_index + 1) % self.buffer_size
        
        # Update only the visible plot
        if self.showing_xyz:
            for axis in ['x', 'y', 'z']:
                self.time_curves[axis].setData(
                    self.data_buffers['t'],
                    self.data_buffers[axis]
                )
            if self.data_index % 50 == 0:
                self.time_plot.enableAutoRange()
        else:
            self.magnitude_curve.setData(
                self.data_buffers['t'],
                self.data_buffers['magnitude']
            )
            if self.data_index % 50 == 0:
                self.magnitude_plot.enableAutoRange()
    
    def update_control_visibility(self, pattern):
        """Show/hide controls based on selected pattern"""
        # Show/hide sine controls
        self.sine_control_widget.setVisible(pattern == 'sine')
        
        # Show/hide pulse controls
        pulse_controls_visible = pattern == 'pulse'
        self.pulse_on_spin.parent().setVisible(pulse_controls_visible)
        
        # Update vibration pattern
        self.change_vibration_pattern(pattern)
    
    def update_sine_frequency(self, value):
        """Update sine wave frequency when spinbox value changes"""
        if self.pattern_combo.currentText() == 'sine':
            self.vibration_controller.set_pattern(
                'sine',
                frequency=value
            )
    
    def change_vibration_pattern(self, pattern):
        if pattern == 'none':
            self.vibration_controller.stop()
        else:
            if pattern == 'pulse':
                # Get pulse timing values
                pulse_on = self.pulse_on_spin.value() / 1000.0
                pulse_off = self.pulse_off_spin.value() / 1000.0
                self.vibration_controller.set_pattern(
                    pattern,
                    pulse_on_time=pulse_on,
                    pulse_off_time=pulse_off
                )
            elif pattern == 'sine':
                # Get frequency value
                frequency = self.frequency_spin.value()
                self.vibration_controller.set_pattern(
                    pattern,
                    frequency=frequency
                )
            else:  # constant pattern
                self.vibration_controller.set_pattern(pattern)
            
            if not self.vibration_controller.isRunning():
                self.vibration_controller.start()
    
    def toggle_data_collection(self):
        if self.data_collector.isRunning():
            self.data_collector.stop()
            self.start_stop_btn.setText("Start")
        else:
            self.data_collector.start()
            self.start_stop_btn.setText("Stop")
    
    def toggle_plot_view(self):
        """Switch between XYZ and magnitude plots"""
        if self.showing_xyz:
            # Switch to magnitude view
            self.time_plot.hide()
            self.magnitude_plot.show()
            self.plot_switch_btn.setText("Show XYZ")
            self.showing_xyz = False
        else:
            # Switch to XYZ view
            self.magnitude_plot.hide()
            self.time_plot.show()
            self.plot_switch_btn.setText("Show Magnitude")
            self.showing_xyz = True
    
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