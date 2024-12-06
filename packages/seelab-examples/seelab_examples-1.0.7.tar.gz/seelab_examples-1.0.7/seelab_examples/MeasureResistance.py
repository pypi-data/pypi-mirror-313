import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap  # Import QPixmap for image handling
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtCore import Qt  # Import Qt for alignment
from .layouts.gauge import Gauge
from .interactive.myUtils import CustomGraphicsView

class Expt(QtWidgets.QMainWindow):
    def __init__(self, device):
        super().__init__()
        self.device = device  # Device handler passed to the Expt class.

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Create a QSplitter for vertical layout with equal sizes
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, central_widget)
        splitter.setSizes([1, 1])  # Ensure equal widths for the splitter sections
        
        self.gauge_widget = Gauge(self, 'RES')
        self.gauge_widget.setObjectName('RES')
        self.gauge_widget.set_MinValue(0)
        self.max_value = 1000
        self.gauge_widget.set_MaxValue(1000)
        self.gauge_widget.setMinimumWidth(400)

        
        # Create a layout for the right side (image)
        image_widget = QtWidgets.QWidget()  # Placeholder for the image
        image_layout = QtWidgets.QVBoxLayout(image_widget)  # Create a layout for the image widget
        

        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove the frame border

        imagepath = os.path.join(os.path.dirname(__file__),'interactive/MeasureResistance.jpg')
        

        mypxmp = QPixmap(imagepath)
        myimg = QGraphicsPixmapItem(mypxmp)
        myimg.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(myimg)


        # Create a horizontal frame for radio buttons and warning label
        range_frame = QtWidgets.QFrame(self)
        range_layout = QtWidgets.QHBoxLayout(range_frame)
        range_frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Create a horizontal frame for radio buttons and warning label
        radio_frame = QtWidgets.QFrame(self)
        radio_layout = QtWidgets.QHBoxLayout(radio_frame)
        radio_frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        left_frame = QtWidgets.QFrame(self)
        left_layout = QtWidgets.QVBoxLayout(left_frame)

        # Create radio buttons for 1K, 10K, 20K, 100K
        self.radio_1K = QtWidgets.QRadioButton("1K")
        self.radio_1K.setStyleSheet("color: #992;")
        self.radio_10K = QtWidgets.QRadioButton("10K")
        self.radio_10K.setStyleSheet("color: green;")
        self.radio_20K = QtWidgets.QRadioButton("20K")
        self.radio_20K.setStyleSheet("color: blue;")
        self.radio_100K = QtWidgets.QRadioButton("100K")
        self.radio_100K.setStyleSheet("color: orange;")  # Added color for 100K

        # Set 1K as the default selected option
        self.radio_1K.setChecked(True)

        # Create a label for A1 selection warning
        self.warning_label = QtWidgets.QLabel("Out of range")
        self.warning_label.setStyleSheet("color: red;")
        self.warning_label.setVisible(False)  # Initially hidden

        # Add radio buttons and warning label to the horizontal layout
        radio_layout.addWidget(self.radio_1K)
        radio_layout.addWidget(self.radio_10K)
        radio_layout.addWidget(self.radio_20K)
        radio_layout.addWidget(self.radio_100K)
        radio_layout.addWidget(self.warning_label)

        # Connect radio button toggles to update gauge maximum
        self.radio_1K.toggled.connect(lambda: self.gauge_widget.set_MaxValue(1000))
        self.radio_10K.toggled.connect(lambda: self.gauge_widget.set_MaxValue(10000))
        self.radio_20K.toggled.connect(lambda: self.gauge_widget.set_MaxValue(20000))
        self.radio_100K.toggled.connect(lambda: self.gauge_widget.set_MaxValue(100000))

        # Add widgets to the splitter
        splitter.addWidget(left_frame)
        splitter.addWidget(self.view)
        
        # Set the splitter as the layout for the central widget
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Add the radio frame to the layout above the gauge
        left_layout.addWidget(radio_frame)  # Add the frame to the main layout
        left_layout.addWidget(self.gauge_widget)
        left_layout.addWidget(range_frame)

        layout.addWidget(splitter)

        # Create a QTimer for periodic voltage measurement
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_voltage)  # Connect the timeout signal to the update method
        self.timer.start(100)  # Start the timer with a 200ms interval

    def update_voltage(self):
        resistance = self.device.get_resistance()
        self.gauge_widget.update_value(resistance)  # Update the gauge with the new voltage value
        
        # Check if resistance exceeds the maximum value and show/hide the warning label
        if resistance > self.max_value:  # Assuming get_MaxValue() method exists
            self.warning_label.setVisible(True)  # Show the warning label
        else:
            self.warning_label.setVisible(False)  # Hide the warning label

    def update_gauge_max(self, max_value):
        self.max_value = max_value
        self.gauge_widget.set_MaxValue(max_value)  # Update the gauge maximum value

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 