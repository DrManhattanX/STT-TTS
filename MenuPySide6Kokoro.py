 
from PySide6.QtCore import QSize, Qt, QTimer, QRunnable, Slot, Signal, QObject, QProcess, QThreadPool
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QPlainTextEdit, QLabel, QComboBox, QVBoxLayout
import time
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import pyaudio
import sys
import traceback
_ESPEAK_LIBRARY = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)
#https://www.pythonguis.com/tutorials/pyside6-layouts/
#https://github.com/KoljaB/RealtimeSTT
#https://github.com/KoljaB/RealtimeTTS


if __name__ == '__main__':
    class WorkerSignals(QObject):
        finished = Signal()
        error = Signal(tuple)
        result = Signal(object)
        progress = Signal(int)


    class Worker(QRunnable):
        def __init__(self, fn, *args, **kwargs):
            super().__init__()

            # Store constructor arguments (re-used for processing)
            self.fn = fn
            self.args = args
            self.kwargs = kwargs
            self.signals = WorkerSignals()

        @Slot()
        def run(self):
            try:
                result = self.fn(*self.args, **self.kwargs)
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)  # Return the result of the processing
            finally:
                self.signals.finished.emit()  # Done
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Kokoro Engine STTS")
            
            self.p = None
            self.threadpool = QThreadPool()

            self.Voices = "am_michael"
            self.Output = 15
            self.Input = 1
            self.Running = False

            self.text = QPlainTextEdit()
            self.text.setReadOnly(True)

            VoiceLabel = QLabel("TTS Voices (Kokoro)")
            VoiceSelectionBox = QComboBox()
            VoiceSelectionBox.addItems(["am_michael", "af_nicole", "af_bella", "af_sarah", "am_adam", "bf_emma", "bf_isabella", "bm_george", "bm_lewis", "af_sky"])
            VoiceSelectionBox.currentTextChanged.connect(self.setVoices)

            OutputCableLabel = QLabel("Virtual Input Cable")
            OutputCableSelectionBox = QComboBox()
            OutputCableSelectionBox.addItems(self.getAllAudioDevices()) #GET CABLE LIST FOR OUTPUTS
            OutputCableSelectionBox.currentTextChanged.connect(self.setOutput)

            InputCableLabel = QLabel("Input Cable (Your Mic)")
            InputCableSelectionBox = QComboBox()
            InputCableSelectionBox.addItems(self.getAudioDevices()) #GET CABLE LIST FOR Input
            InputCableSelectionBox.currentTextChanged.connect(self.setInput)

            #LAYOUT STUFF
            layout = QVBoxLayout()
            layout.addWidget(VoiceLabel)
            layout.addWidget(VoiceSelectionBox)
            layout.addWidget(OutputCableLabel)
            layout.addWidget(OutputCableSelectionBox)
            layout.addWidget(InputCableLabel)
            layout.addWidget(InputCableSelectionBox)
            button1 = QPushButton("Start!")
            button1.clicked.connect(self.startLoop)
            button2 = QPushButton("Kill!")
            button2.clicked.connect(self.killLoop)
            layout.addWidget(self.text)
            layout.addWidget(button1)
            layout.addWidget(button2)

            container = QWidget()
            container.setLayout(layout)

            self.setMinimumSize(QSize(400, 300))

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        
        def message(self, s):
            self.text.appendPlainText(s)

        def setVoices(self, text):
            self.Voices = text
            print(text)

        def setOutput(self, text):
            self.Output = str(text[:1])
            print(text)

        def setInput(self, text):
            self.Input = str(text[:1])
            print(text)

        def getAudioDevices(self):
            p = pyaudio.PyAudio()
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            Devices = []
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                     Devices.append((str(i)+" - "+p.get_device_info_by_host_api_device_index(0, i).get('name')))
            return Devices
        
        def getAllAudioDevices(self):
            p = pyaudio.PyAudio()
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            Devices = []
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                     Devices.append((str(i)+" - "+p.get_device_info_by_host_api_device_index(0, i).get('name')))
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                     Devices.append((str(i)+" - "+p.get_device_info_by_host_api_device_index(0, i).get('name')))
            return Devices
        
        def startLoop(self):
            if self.p is None:
                self.p = QProcess()
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.finished.connect(self.process_finished)
                
                self.p.start("py -3.11", ['main.py', self.Voices, self.Output, self.Input])
                
                worker = Worker(self.statusLoop)
                self.threadpool.start(worker)

        def statusLoop(self):
            self.message(str(self.p.state()))
            while self.p.state() is not QProcess.Running:
                self.message(str(self.p.state()))
                time.sleep(5)
            self.message("running")

        def process_finished(self):
            self.p = None

        def killLoop(self):
            self.Running = False
            self.p.kill()

        def handle_stderr(self):
            data = self.p.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            self.message(stderr)

        def handle_stdout(self):
            data = self.p.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")
            self.message(stdout)

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
