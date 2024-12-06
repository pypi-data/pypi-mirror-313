import platform
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from ..layouts import ui_spreadsheetLayout
import numpy as np
import matplotlib.pyplot as plt

class MySpreadsheet(QtWidgets.QWidget, ui_spreadsheetLayout.Ui_Form):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def plot(self):
        # Prepare data for plotting
        x = []
        y = []
        for i in range(self.tableWidget.rowCount()):
            item_x = self.tableWidget.item(i, 0)
            item_y = self.tableWidget.item(i, 1)
            
            # Check if both items are not None and have valid text
            if item_x is not None and item_y is not None:
                try:
                    x_value = float(item_x.text())
                    y_value = float(item_y.text())
                    x.append(x_value)
                    y.append(y_value)
                except (ValueError, AttributeError):
                    QtWidgets.QMessageBox.warning(self, "Data Entry Error", f"Invalid data at row {i + 1}.\nWill Plot what we have.")
                    if i<2:return
                    break
            else:
                # Stop collecting data if we hit an empty row
                break

        # Check if we have enough data to plot
        if len(x) < 1:
            QtWidgets.QMessageBox.warning(self, "Data Entry Error", "Not enough valid data to plot.")
            return

        # Create the plot in a separate timer to avoid event loop issues
        QTimer.singleShot(0, lambda: self.show_plot(x, y))


    def show_plot(self, x, y):
        plt.ion()
        plt.figure()
        plt.plot(x, y, marker='o')
        plt.title(f'X vs Y ({len(x)} Total points)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid()
        #plt.show()

    def addSine(self):
        self.clearIt()
        import numpy as np
        x = np.linspace(0, 2 * np.pi, 100)  # 100 points from 0 to 2π
        for i in range(100):
            self.tableWidget.item(i, 0).setText(f'{x[i]:.3f}')  
            self.tableWidget.item(i, 1).setText(f'{np.sin(x[i]):.3f}')  
    
    def clearIt(self):
        # Ensure at least 100 rows are displayed
        while self.tableWidget.rowCount() < 100:
            self.tableWidget.insertRow(self.tableWidget.rowCount())

        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item is None:
                    item = QtWidgets.QTableWidgetItem()  # Create a new QTableWidgetItem
                    self.tableWidget.setItem(row, column, item)  # Set the new item in the table
                self.tableWidget.item(row, column).setText("")  # Clear the contents of each cell

