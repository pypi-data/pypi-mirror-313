# seelab_examples/__init__.py

import sys,os
from .layouts import QtVersion,utils  # Added import for QtVersion
from PyQt5 import QtWidgets
import argparse  # Added import for argparse

from .script_runner import ScriptRunner  # Adjust the import based on your actual script structure

def main():
    """Main entry point for the app_examples module."""
    parser = argparse.ArgumentParser(description='Run a specific script from seelab_examples.')
    parser.add_argument('script', nargs='?', help='The name of the script to run (without .py extension).')
    args = parser.parse_args()

    os.chdir(os.path.dirname(__file__))
    app = QtWidgets.QApplication(sys.argv)
    window = ScriptRunner(args)
    window.show()
    sys.exit(app.exec_())

# No need for the if __name__ == "__main__": block here anymore
