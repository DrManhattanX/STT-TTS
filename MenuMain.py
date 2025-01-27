 
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QLabel, QComboBox, QVBoxLayout
import pyaudio
import sys

#https://www.pythonguis.com/tutorials/pyside6-layouts/

if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("My App")
            self.button_is_checked = True

            self.Engine = "Kokoro"
            self.Voices = "am_michael"
            self.Output = 1
            self.Input = 1

            EngineLabel = QLabel("TTS Engine")
            EngineSelectionBox = QComboBox()
            EngineSelectionBox.addItems(["Kokoro", "GTTSEngine", "SystemEngine"])
            EngineSelectionBox.currentTextChanged.connect(self.setEngine)

            VoiceLabel = QLabel("TTS Voices (Kokoro)")
            VoiceSelectionBox = QComboBox()
            VoiceSelectionBox.addItems(["am_michael", "af_nicole", "af_bella", "af_sarah", "am_adam", "bf_emma", "bf_isabella", "bm_george", "bm_lewis", "af_sky"])
            VoiceSelectionBox.currentTextChanged.connect(self.setVoices)

            OutputCableLabel = QLabel("Virtual Input Cable")
            OutputCableSelectionBox = QComboBox()
            OutputCableSelectionBox.addItems(self.setAudioDevices()) #GET CABLE LIST FOR OUTPUTS
            OutputCableSelectionBox.currentTextChanged.connect(self.setOutput)

            InputCableLabel = QLabel("Input Cable (Your Mic)")
            InputCableSelectionBox = QComboBox()
            InputCableSelectionBox.addItems(self.setAudioDevices()) #GET CABLE LIST FOR Input
            InputCableSelectionBox.currentTextChanged.connect(self.setInput)

            #LAYOUT STUFF
            layout = QVBoxLayout()
            layout.addWidget(EngineLabel)
            layout.addWidget(EngineSelectionBox)
            layout.addWidget(VoiceLabel)
            layout.addWidget(VoiceSelectionBox)
            layout.addWidget(OutputCableLabel)
            layout.addWidget(OutputCableSelectionBox)
            layout.addWidget(InputCableLabel)
            layout.addWidget(InputCableSelectionBox)

            container = QWidget()
            container.setLayout(layout)

            self.setMinimumSize(QSize(400, 300))

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        def setEngine(self, text):
            self.Engine = text
            print(text)
        def setVoices(self, text):
            self.Voices = text
            print(text)
        def setOutput(self, text):
            self.Output = text
            print(text)
        def setInput(self, text):
            self.Input = text
            print(text)
        def setAudioDevices(self):
            p = pyaudio.PyAudio()
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            Devices = []
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                     Devices.append((str(i)+" - "+p.get_device_info_by_host_api_device_index(0, i).get('name')))
            return Devices

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
