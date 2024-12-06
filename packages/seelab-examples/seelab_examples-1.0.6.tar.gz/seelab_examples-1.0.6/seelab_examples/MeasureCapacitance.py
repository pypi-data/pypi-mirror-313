import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QMovie  # Import QPixmap for image handling and QMovie for the spinning icon
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal  # Import Qt for alignment, QThread and pyqtSignal
from .layouts.gauge import Gauge
from .interactive.myUtils import CustomGraphicsView

class MeasureThread(QThread):
    measurement_done = pyqtSignal(float)  # Signal to indicate measurement completion

    def __init__(self, device):
        super().__init__()
        self.device = device

    def run(self):
        cap = self.device.get_capacitance()  # Perform the measurement
        if cap < 0:
            cap = 0
        self.measurement_done.emit(cap)  # Emit the result

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
        
        self.gauge_widget = Gauge(self, 'CAP')
        self.gauge_widget.setObjectName('CAP')
        self.gauge_widget.set_MinValue(0)
        self.max_value = 1000
        self.gauge_widget.set_MaxValue(1000)
        self.gauge_widget.setMinimumWidth(400)
        self.gauge_widget.title_fontsize = 28

        
        # Create a layout for the right side (image)
        image_widget = QtWidgets.QWidget()  # Placeholder for the image
        image_layout = QtWidgets.QVBoxLayout(image_widget)  # Create a layout for the image widget
        

        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove the frame border

        imagepath = os.path.join(os.path.dirname(__file__),'interactive/Measure Capacitance.jpg')
        

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
        self.radio_1nF = QtWidgets.QRadioButton("0-1000pF")
        self.radio_1nF.setStyleSheet("color: #771;border: 1px dotted blue;")
        self.radio_100nF = QtWidgets.QRadioButton("0-100nF")
        self.radio_100nF.setStyleSheet("color: green;border: 1px dotted blue;")
        self.radio_1uF = QtWidgets.QRadioButton("0-1uF")
        self.radio_1uF.setStyleSheet("color: blue;border: 1px dotted blue;")
        self.radio_100uF = QtWidgets.QRadioButton("0-100uF")
        self.radio_100uF.setStyleSheet("color: red;border: 1px dotted blue;")  # Added color for 100uF

        # Set 1nF as the default selected option
        self.radio_1nF.setChecked(True)

        # Create a label for A1 selection warning
        self.warning_label = QtWidgets.QLabel("Out of range")
        self.warning_label.setStyleSheet("color: red;")
        self.warning_label.setVisible(False)  # Initially hidden

        # Add radio buttons and warning label to the horizontal layout
        radio_layout.addWidget(self.radio_1nF)
        radio_layout.addWidget(self.radio_100nF)
        radio_layout.addWidget(self.radio_1uF)
        radio_layout.addWidget(self.radio_100uF)
        radio_layout.addWidget(self.warning_label)

        self.radio_1nF.setEnabled(False)
        self.radio_100nF.setEnabled(False)
        self.radio_1uF.setEnabled(False)
        self.radio_100uF.setEnabled(False)
        self.radio_1nF.setChecked(True)


        # Create a horizontal frame for radio buttons and warning label
        meas_frame = QtWidgets.QFrame(self)
        meas_layout = QtWidgets.QHBoxLayout(meas_frame)
        meas_frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        self.measure_button = QtWidgets.QPushButton("Measure Capacitance")
        self.measure_button.setStyleSheet("background-color: #cde;font-size: 30px;")
        self.measure_button.setMinimumHeight(90)
        meas_layout.addWidget(self.measure_button)
        self.measure_button.clicked.connect(self.start_measurement)

        # Create a label for the spinning icon
        self.loading_label = QtWidgets.QLabel(self)
        spingif = os.path.join(os.path.dirname(__file__),'interactive/spin.gif')

        self.loading_label.setFixedSize(90,90)
        self.loading_label.setScaledContents(True)  
        self.loading_movie = QMovie(spingif)  # Path to your spinning icon
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setVisible(False)  # Initially hidden
        # Add loading label to the layout
        meas_layout.addWidget(self.loading_label)


        # Add widgets to the splitter
        splitter.addWidget(left_frame)
        splitter.addWidget(self.view)
        
        # Set the splitter as the layout for the central widget
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Add the radio frame to the layout above the gauge
        left_layout.addWidget(radio_frame)  # Add the frame to the main layout
        left_layout.addWidget(self.gauge_widget)
        left_layout.addWidget(range_frame)
        left_layout.addWidget(meas_frame)

        layout.addWidget(splitter)



    def start_measurement(self):
        self.loading_label.setVisible(True)  # Show the loading icon
        self.loading_movie.start()  # Start the spinning animation
        self.measure_button.setEnabled(False)  # Disable the button

        self.measure_thread = MeasureThread(self.device)
        self.measure_thread.measurement_done.connect(self.on_measurement_done)
        self.measure_thread.start()  # Start the measurement in a separate thread

    def on_measurement_done(self, cap):
        print(cap)
        self.loading_movie.stop()  # Stop the spinning animation
        self.loading_label.setVisible(False)  # Hide the loading icon
        self.measure_button.setEnabled(True)  # Re-enable the button
        self.autoselectRange(cap)  # Call the existing method to handle the result
        # Update gauge value based on the selected radio button
        if self.radio_1nF.isChecked():
            self.gauge_widget.update_value(cap*1e12)  # Update the gauge with the new capacitance value
            if(cap>1e-9):
                self.warning_label.setVisible(True) 
        elif self.radio_100nF.isChecked():
            self.gauge_widget.update_value(cap*1e9)  # Update the gauge with the new capacitance value
            if(cap>100e-9):
                self.warning_label.setVisible(True) 
        elif self.radio_1uF.isChecked():
            self.gauge_widget.update_value(cap*1e6)  # Update the gauge with the new capacitance value
            if(cap>1e-6):
                self.warning_label.setVisible(True) 
        elif self.radio_100uF.isChecked():
            self.gauge_widget.update_value(cap*1e6)  # Update the gauge with the new capacitance value
            if(cap>120e-6):
                self.warning_label.setVisible(True) 

    def autoselectRange(self,c):
        if c<1000e-12:
            self.radio_1nF.setChecked(True)
        elif c<100e-9:
            self.radio_100nF.setChecked(True)
        elif c<1e-6:
            self.radio_1uF.setChecked(True)
        else:
            self.radio_100uF.setChecked(True)
        self.update_gauge_and_warning()


    def update_gauge_and_warning(self):
        self.warning_label.setVisible(False) 
        if self.radio_1nF.isChecked():
            self.gauge_widget.set_MaxValue(1e3)
            self.gauge_widget.title_text = 'CAP (pF)'
        elif self.radio_100nF.isChecked():
            self.gauge_widget.set_MaxValue(100)
            self.gauge_widget.title_text = 'CAP (nF)'
        elif self.radio_1uF.isChecked():
            self.gauge_widget.set_MaxValue(1)
            self.gauge_widget.title_text = 'CAP (uF)'
        elif self.radio_100uF.isChecked():
            self.gauge_widget.set_MaxValue(100)
            self.gauge_widget.title_text = 'CAP (uF)'
# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 