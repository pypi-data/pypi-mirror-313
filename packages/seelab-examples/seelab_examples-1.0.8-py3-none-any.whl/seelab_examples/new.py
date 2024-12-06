import sys
from PyQt5 import QtWidgets, QtCore

class Expt(QtWidgets.QMainWindow):
    def __init__(self, device):
        super().__init__()
        self.device = device  # Device handler passed to the Expt class.

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        # Add a label
        self.label = QtWidgets.QLabel("Welcome to the Sample Experiment!", self)
        layout.addWidget(self.label)

        # Add a button
        self.button = QtWidgets.QPushButton("Click To Read A1 Voltage", self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

    def on_button_click(self):
        """Handle button click event."""
        self.label.setText("A1 Voltage: %.3f"%(self.device.get_voltage('A1')))

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 