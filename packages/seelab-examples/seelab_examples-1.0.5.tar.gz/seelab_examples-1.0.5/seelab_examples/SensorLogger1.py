import sys
from PyQt5 import QtWidgets, QtCore
import time
import pyqtgraph as pg

class Expt(QtWidgets.QMainWindow):
    def __init__(self, dev):
        super().__init__()
        self.device = dev
        self.setWindowTitle("Four Channel Oscilloscope")
        self.setGeometry(100, 100, 1000, 600)

        # Create a QSplitter for vertical layout
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        # Create left widget for controls
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout(self.left_widget)

        # Create UI components for sensor data collection
        self.sensor_name_dropdown = QtWidgets.QComboBox()
        self.sensor_name_dropdown.addItems(['BMP280', 'BME280', 'MPU6050', 'VL53L0X', 'HMC5883L', 'SR04'])

        self.parameter_index_spinbox = QtWidgets.QSpinBox()
        self.parameter_index_spinbox.setMinimum(0)
        self.parameter_index_spinbox.setMaximum(10)  # Adjust based on your sensor parameters

        self.points_spinbox = QtWidgets.QSpinBox()
        self.points_spinbox.setMinimum(1)
        self.points_spinbox.setMaximum(100000)  # Adjust based on your needs
        self.points_spinbox.setValue(1000)

        self.interval_spinbox = QtWidgets.QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(1000)  # Maximum interval in milliseconds

        self.collect_data_button = QtWidgets.QPushButton("Collect Data")
        self.collect_data_button.clicked.connect(self.start_data_collection)

        # Add UI components to the left layout
        self.left_layout.addWidget(QtWidgets.QLabel("Sensor Name:"))
        self.left_layout.addWidget(self.sensor_name_dropdown)
        self.left_layout.addWidget(QtWidgets.QLabel("Parameter Index:"))
        self.left_layout.addWidget(self.parameter_index_spinbox)
        self.left_layout.addWidget(QtWidgets.QLabel("Points:"))
        self.left_layout.addWidget(self.points_spinbox)
        self.left_layout.addWidget(QtWidgets.QLabel("Interval (ms):"))
        self.left_layout.addWidget(self.interval_spinbox)
        self.left_layout.addWidget(self.collect_data_button)

        # Add the left widget to the splitter
        self.splitter.addWidget(self.left_widget)

        # Create right widget for plotting
        self.plot_widget = pg.PlotWidget()
        self.splitter.addWidget(self.plot_widget)

        # Initialize the sensor data thread
        self.sensor_data_thread = None
        self.collected_data = []  # Store collected data for plotting

    def start_data_collection(self):
        """Start collecting data from the selected sensor."""
        if self.sensor_data_thread is not None and self.sensor_data_thread.isRunning():
            self.sensor_data_thread.stop()  # Stop any existing thread

        self.collected_data = []  # Store collected data for plotting
        sensor_name = self.sensor_name_dropdown.currentText()
        parameter_index = self.parameter_index_spinbox.value()
        points = self.points_spinbox.value()
        interval = self.interval_spinbox.value()

        # Create and start the sensor data thread
        self.sensor_data_thread = SensorDataThread(self.device, sensor_name, parameter_index, points, interval)
        self.sensor_data_thread.data_collected.connect(self.update_plot_with_sensor_data)
        self.sensor_data_thread.start()

    def update_plot_with_sensor_data(self, new_data):
        """Update the plot with the collected sensor data."""
        self.collected_data.extend(new_data)  # Keep a copy of all collected data
        self.plot_widget.clear()  # Clear previous data
        self.plot_widget.plot(self.collected_data, pen='b')  # Plot new data in blue

class SensorDataThread(QtCore.QThread):
    data_collected = QtCore.pyqtSignal(list)  # Signal to send collected data to the UI

    def __init__(self, device, sensor_name, parameter_index, points, interval):
        super().__init__()
        self.device = device
        self.sensor_name = sensor_name
        self.parameter_index = parameter_index
        self.points = points
        self.interval = interval / 1000.0  # Convert to seconds
        self.running = True
        self.data = []
        self.sent_points = 0  # Track how many points have been sent

    def run(self):
        while self.running and len(self.data) < self.points:
            # Collect sensor data
            value = self.device.get_sensor(self.sensor_name, self.parameter_index)
            self.data.append(value)

            # Emit data every 200ms or when enough points have been collected
            if len(self.data) - self.sent_points >= int(200 / (self.interval * 1000)):
                new_data = self.data[self.sent_points:]  # Get new data since last sent
                self.data_collected.emit(new_data)
                self.sent_points = len(self.data)  # Update the count of sent points

            time.sleep(self.interval)  # Wait for the specified interval

        # After the loop ends, emit any remaining data
        if self.running and self.sent_points < len(self.data):
            remaining_data = self.data[self.sent_points:]  # Get any remaining data
            self.data_collected.emit(remaining_data)

    def stop(self):
        self.running = False
        self.wait()

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 