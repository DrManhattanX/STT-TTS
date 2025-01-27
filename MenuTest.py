 
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QLabel, QComboBox
import sys

#https://www.pythonguis.com/tutorials/pyside6-layouts/

if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("My App")
            self.button_is_checked = True

            self.box1 = ""

            combobox1 = QComboBox()
            combobox1.addItems(["One", "Two", "Three"])
            combobox1.currentTextChanged.connect(self.qbox1)

            layout = QGridLayout()
            layout.addWidget(combobox1)

            container = QWidget()
            container.setLayout(layout)

            self.setMinimumSize(QSize(400, 300))

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        def setbox1(self, text): 
            self.box1 = text


    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
