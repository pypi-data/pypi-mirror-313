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
        
        self.gauge_widget = Gauge(self, 'A1')
        self.gauge_widget.setObjectName('A1')
        self.gauge_widget.set_MinValue(-16)
        self.gauge_widget.set_MaxValue(16)
        self.gauge_widget.setMinimumWidth(400)

        
        # Create a layout for the right side (image)
        image_widget = QtWidgets.QWidget()  # Placeholder for the image
        image_layout = QtWidgets.QVBoxLayout(image_widget)  # Create a layout for the image widget
        

        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove the frame border

        imagepath = os.path.join(os.path.dirname(__file__),'interactive/DC_Voltmeter.jpg')
        

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

        # Create radio buttons for A1, A2, A3
        self.radio_A1 = QtWidgets.QRadioButton("A1")
        self.radio_A1.setStyleSheet("color: #992;")
        self.radio_A2 = QtWidgets.QRadioButton("A2")
        self.radio_A2.setStyleSheet("color: green;")
        self.radio_A3 = QtWidgets.QRadioButton("A3")
        self.radio_A3.setStyleSheet("color: blue;")

        # Set A1 as the default selected option
        self.radio_A1.setChecked(True)

        # Create a label for A1 selection warning
        self.warning_label = QtWidgets.QLabel("A1 is not selected")
        self.warning_label.setStyleSheet("color: red;")
        self.warning_label.setVisible(False)  # Initially hidden

        # Add radio buttons and warning label to the horizontal layout
        radio_layout.addWidget(self.radio_A1)
        radio_layout.addWidget(self.radio_A2)
        radio_layout.addWidget(self.radio_A3)
        radio_layout.addWidget(self.warning_label)

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
        self.timer.start(200)  # Start the timer with a 200ms interval

    def update_voltage(self):
        # Determine which radio button is selected
        if self.radio_A1.isChecked():
            voltage = self.device.get_voltage('A1')  # Get the voltage from A1
            self.warning_label.setVisible(False)  # Hide warning if A1 is selected
        elif self.radio_A2.isChecked():
            voltage = self.device.get_voltage('A2')  # Get the voltage from A2
            self.warning_label.setVisible(True)  # Show warning if A1 is not selected
        else:
            voltage = self.device.get_voltage('A3')  # Get the voltage from A3
            self.warning_label.setVisible(True)  # Show warning if A1 is not selected
        self.gauge_widget.update_value(voltage)  # Update the gauge with the new voltage value

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 