import json
import sys
import time
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np  # Import numpy
import pyqtgraph as pg  # Import pyqtgraph

import json
import threading


class Expt(QtWidgets.QMainWindow):
    responseReceived = pyqtSignal(dict)
    def __init__(self, device):
        super().__init__()
        self.device = device  # Device handler passed to the Expt class.
        self.map_server = None
        self.coordinates_changed=True
        
        # Initialize latitude and longitude variables
        #coordinates for new delhi
        self.latitude = 28.6139
        self.longitude = 77.2090

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout
        layout = QtWidgets.QHBoxLayout(central_widget)  # Change to HBox layout for side-by-side frames

        # Create a frame to limit maximum width
        self.frame = QtWidgets.QFrame(self)
        self.frame.setMaximumWidth(400)  # Set maximum width to 400px
        frame_layout = QtWidgets.QVBoxLayout(self.frame)
        layout.addWidget(self.frame)  # Add frame to the main layout

        # Add a button to launch the map server
        self.map_button = QtWidgets.QPushButton("Launch Map To Locate Coordinates")
        self.map_button.clicked.connect(self.show_local_map)  # Connect button click to show_help
        frame_layout.addWidget(self.map_button)  # Add button to the frame layout

        # Create double spin boxes for latitude and longitude
        self.lat_spinbox = QtWidgets.QDoubleSpinBox(self); self.lat_spinbox.setValue(0.0)
        self.lat_spinbox.setDecimals(8)
        self.lat_spinbox.setValue(self.latitude)
        self.lat_spinbox.editingFinished.connect(self.update_coordinates)  # Connect to update on finish
        frame_layout.addWidget(self.lat_spinbox)  # Add latitude spinbox to the frame layout

        self.lon_spinbox = QtWidgets.QDoubleSpinBox(self); self.lon_spinbox.setValue(0.0)
        self.lon_spinbox.setDecimals(8)
        self.lon_spinbox.setValue(self.longitude)
        self.lon_spinbox.editingFinished.connect(self.update_coordinates)  # Connect to update on finish
        frame_layout.addWidget(self.lon_spinbox)  # Add longitude spinbox to the frame layout

        # Label to display coordinates
        self.coordinates_label = QtWidgets.QLabel(f"Coordinates: ({self.latitude}, {self.longitude})", self)
        frame_layout.addWidget(self.coordinates_label)

        # Add text fields for user input
        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setPlaceholderText("Your Name")
        frame_layout.addWidget(self.name_input)

        self.sensor_name_input = QtWidgets.QLineEdit(self)
        self.sensor_name_input.setPlaceholderText("Sensor Name")
        frame_layout.addWidget(self.sensor_name_input)

        self.parameter_name_input = QtWidgets.QLineEdit(self)
        self.parameter_name_input.setPlaceholderText("Parameter Name")
        frame_layout.addWidget(self.parameter_name_input)

        self.command_input = QtWidgets.QLineEdit(self)
        self.command_input.setText("p.get_voltage('A1')")
        self.command_input.setPlaceholderText("p.get_voltage('A1')")
        frame_layout.addWidget(self.command_input)

        self.interval_frame = QtWidgets.QFrame(self)
        self.interval_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_layout.addWidget(self.interval_frame)
        self.interval_layout = QtWidgets.QHBoxLayout(self.interval_frame)

        self.interval_label = QtWidgets.QLabel("Interval (ms):")
        self.interval_layout.addWidget(self.interval_label)

        self.interval_spinbox = QtWidgets.QSpinBox(self)
        self.interval_spinbox.setRange(1, 10000)
        self.interval_spinbox.setValue(1000)
        self.interval_layout.addWidget(self.interval_spinbox)

        self.upload_checkbox = QtWidgets.QCheckBox("Upload data")
        self.interval_layout.addWidget(self.upload_checkbox)
        # Create a label for result
        self.result_label = QtWidgets.QTextBrowser(self)
        frame_layout.addWidget(self.result_label)

        self.upload_timer = QtCore.QTimer(self)  # Timer for posting data
        self.upload_timer.timeout.connect(self.post_data)  # Connect timeout to post_data method

        self.upload_checkbox.toggled.connect(self.toggle_upload)  # Connect checkbox toggle to new method

        # Add a button to launch the map server
        self.online_map_button = QtWidgets.QPushButton("Show Online Map")
        self.online_map_button.clicked.connect(self.show_online_map)  # Connect button click to show_help
        frame_layout.addWidget(self.online_map_button)  # Add button to the frame layout

        # Create a frame for the pyqtgraph plot
        self.plot_frame = QtWidgets.QFrame(self)
        layout.addWidget(self.plot_frame)  # Add plot frame to the main layout
        plot_layout = QtWidgets.QVBoxLayout(self.plot_frame)

        # Create a PlotWidget for plotting data
        self.plot_widget = pg.PlotWidget()
        plot_layout.addWidget(self.plot_widget)  # Add the plot widget to the plot frame

        # Example: Initialize plot data
        self.plot_data = []  # Placeholder for data to be plotted
        self.plot_widget.setTitle("Local Data Plot")
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Datapoints')

        self.waitingForResponse = False
        self.responseReceived.connect(self.parseResponse)

    def update_coordinates(self):
        self.coordinates_changed= True
        # Update latitude and longitude variables
        self.latitude = self.lat_spinbox.value()
        self.longitude = self.lon_spinbox.value()
        # Update the label with new coordinates
        self.coordinates_label.setText(f"Coordinates: ({self.latitude}, {self.longitude})")
        if self.upload_checkbox.isChecked():
            self.start_upload()  # Start the upload process if checkbox is checked

    def toggle_upload(self, checked):
        if checked:
            if self.latitude != 0.0 and self.longitude != 0.0 and self.name_input.text() and self.sensor_name_input.text() and self.parameter_name_input.text():
                self.start_upload()  # Start the upload process
                # Update graph title and Y-axis label
                self.plot_widget.setTitle(f"Name: {self.name_input.text()} - Sensor: {self.sensor_name_input.text()}")
                self.plot_widget.setLabel('left', self.parameter_name_input.text())  # Set Y-axis label
                self.plot_widget.clear()  # Clear the graph before starting
                self.plot_data = []
            else:
                self.result_label.setText("Latitude, Longitude, User Name, Sensor Name, and Parameter Name must be non-zero or filled to start upload.")
        else:
            self.upload_timer.stop()  # Stop the timer if checkbox is unchecked

    def start_upload(self):
        interval = self.interval_spinbox.value()
        self.upload_timer.start(interval)  # Start the timer with the specified interval


    def post_threaded_data(self, url, payload):
        # Run the request in a separate thread
        thread = threading.Thread(target=self._send_request, args=(url, payload))
        thread.daemon = True
        thread.start()

    def _send_request(self, url, payload):
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            self.responseReceived.emit(response.json())  # Emit the response data as a signal
        except requests.RequestException as e:
            # Handle errors by emitting an error response or logging
            self.responseReceived.emit({'error': str(e)})

    def post_data(self):
        if not self.upload_checkbox.isChecked():
            self.upload_timer.stop()  # Stop the timer if checkbox is unchecked
            return

        command = self.command_input.text()
        try:
            # Use eval to execute the command with self.device as globals
            value = eval(command, {"__builtins__": None,"np": np, "p":self.device}, vars(self.device))
            if value is not None:  # Check if command execution was successful
                # Update the plot with the new value
                if not self.waitingForResponse:
                    self.plot_data.append(value)  # Append new value to plot data
                    self.plot_widget.plot(self.plot_data, pen='g')  # Plot the data in green

                    payload = {
                        "token": "token1",
                        "user_name": self.name_input.text(),
                        "sensor_name": self.sensor_name_input.text(),
                        "parameter_name": self.parameter_name_input.text(),
                        "value": float(value),
                        "latitude": float(self.latitude),
                        "longitude": float(self.longitude)
                    }

                    self.post_threaded_data('https://expeyes.scischool.in:4000/gpsdata',payload)
                    self.result_label.setText(f"{time.ctime()}: uploading : {value}")
                    self.waitingForResponse=True
                else:
                    pass
                # Post the data to the /gpsdata endpoint
                #response = requests.post('https://expeyes.scischool.in:4000/gpsdata', json=payload)
                #response.raise_for_status()  # Raise an error for bad responses
                #self.result_label.setText(f"{time.ctime()}: {response.text}")  # Update result label
            else:
                self.result_label.setText("Command execution failed or is missing.")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")  # Handle any exceptions

    def parseResponse(self,resp):
        self.waitingForResponse = False
        if 'error' in resp:
            self.result_label.setText(f"Error: {resp['error']}")  # Handle any exceptions
            print('failed to upload',resp.error)
        else:
            self.result_label.setText(f"{time.ctime()}: {resp.text}")  # Update result label
 

    def createWebserver(self):
        if self.map_server is not None:
            return

        port = 8002
        server_address = ('0.0.0.0', port)
        from http.server import HTTPServer, SimpleHTTPRequestHandler

        # Start the server
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory='online', **kwargs)

            def do_GET(self):
                if self.path == '/coordinates':
                    # Respond with the stored latitude and longitude
                    coordinates = {
                        'latitude': self.server.expt.latitude,
                        'longitude': self.server.expt.longitude,
                        'changed': self.server.expt.coordinates_changed
                    }
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(coordinates).encode())
                    self.server.expt.coordinates_changed=False

                else:
                    super().do_GET()



            def do_POST(self):
                if self.path == '/update':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data)

                    # Update latitude and longitude in the Expt instance
                    self.server.expt.latitude = data['latitude']
                    self.server.expt.longitude = data['longitude']

                    # Update the spin boxes
                    self.server.expt.lat_spinbox.setValue(self.server.expt.latitude)
                    self.server.expt.lon_spinbox.setValue(self.server.expt.longitude)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Coordinates updated successfully')
                else:
                    super().do_POST()

        # Set up the HTTP server
        httpd = HTTPServer(server_address, Handler)
        httpd.expt = self  # Pass the Expt instance to the handler

        # Create a thread to run the server
        self.map_server = threading.Thread(target=httpd.serve_forever)
        self.map_server.daemon = True  # Allows the thread to exit when the main program does
        self.map_server.start()


    def show_local_map(self):
        import webbrowser
        self.createWebserver()
        webbrowser.open(f"http://localhost:8002/iot/map.html")  

    def show_online_map(self):
        import webbrowser
        self.createWebserver()
        webbrowser.open(f"https://expeyes.scischool.in:4000/information")  

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    import eyes17.eyes
    dev = eyes17.eyes.open()
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(dev)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 