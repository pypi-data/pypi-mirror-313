import os
import socket
import sys
import time
import webbrowser
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap

class Expt(QtWidgets.QMainWindow):
    logThis = QtCore.pyqtSignal(str)
    showStatusSignal = QtCore.pyqtSignal(str, bool)
    serverSignal = QtCore.pyqtSignal(str)

    def __init__(self, device):
        super().__init__()
        self.device = device  # Device handler passed to the Expt class.
        self.serverActive = False
        self.external = None
        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        # Create a layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        # Add a label
        self.label = QtWidgets.QLabel("Visual Programming!", self)
        layout.addWidget(self.label)

        # Create a button to launch the pip installer
        self.pip_button = QtWidgets.QPushButton("Install Missing Packages", self)
        self.pip_button.clicked.connect(self.launchPipInstaller)  # Connect button to method
        layout.addWidget(self.pip_button)  # Add button to layout

        # Create a button to open the browser
        self.browser_button = QtWidgets.QPushButton("Open Browser", self)
        self.browser_button.clicked.connect(self.openBrowser)  # Connect button to method
        layout.addWidget(self.browser_button)  # Add button to layout

        # Create a text browser for displaying debug messages
        self.debug_text_browser = QtWidgets.QTextBrowser(self)
        layout.addWidget(self.debug_text_browser)  # Add text browser to layout

        self.activateCompileServer()


    def activateCompileServer(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)  # Set a timeout to avoid blocking indefinitely
        try:
            s.connect(("8.8.8.8", 80))  # Connect to a public IP address
            self.local_ip = s.getsockname()[0]
        except:
            self.local_ip = 'localhost'

        from .online.compile_server import create_server
        self.compile_thread = create_server(self.showStatusSignal, self.serverSignal, os.path.join(os.path.dirname(__file__), 'blockly'), self.local_ip, self.device)

        self.showStatusSignal.connect(self.showStatus)
        self.serverSignal.connect(self.showServerStatus)
        s.close()
        self.showStatus("Visual Coding Active at " + self.local_ip + ":8888", False)
        #self.compile_thread_button.setText(self.local_ip)
        self.serverActive = True


    def closeEvent(self, event):
        """Ensure the thread is stopped when the dialog is closed."""
        event.ignore()
        print('closing...')
        if self.external is not None:
            print('terminating term...')
            self.external.terminate()
            self.external.waitForFinished(1000)

        event.accept()

    def openBrowser(self, url):
        webbrowser.open(f"http://localhost:8888/visual"+ '?connected='+str(self.device.connected))  # Adjust the URL as needed

    def showStatus(self, msg, error=None):
        # Append messages to the text browser instead of printing
        self.debug_text_browser.append(f"{msg} {'(Error)' if error else ''}")
        # Optionally, you can still print to the terminal if needed
        # print(msg, error)

    def showServerStatus(self, msg):
        self.showStatus("Compiler: Error Launching Server (Restart app) ", True)
        QtWidgets.QMessageBox.warning(self, 'Server Error', msg)


    def showPipInstaller(self, name):
        from .utilities.pipinstallerMP import PipInstallDialog
        self.pipdialog = PipInstallDialog(name, self)
        self.pipdialog.show()

    def launchPipInstaller(self):
        self.showPipInstaller("Package Name")  # Replace "Package Name" with actual package name or logic to determine missing packages

# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 