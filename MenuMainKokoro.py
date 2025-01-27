 
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QLabel, QComboBox, QVBoxLayout
from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, GTTSEngine ,SystemEngine, KokoroEngine
from datetime import time
from phonemizer.backend.espeak.wrapper import EspeakWrapper
import pyaudio
import sys
_ESPEAK_LIBRARY = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)
#https://www.pythonguis.com/tutorials/pyside6-layouts/
#https://github.com/KoljaB/RealtimeSTT
#https://github.com/KoljaB/RealtimeTTS


if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            kokoro_root = "C:/Users/ty10r/Desktop/Projects/Python Stuff/Kokoro-82M"

            self.engine = KokoroEngine(kokoro_root=kokoro_root,) # replace with your TTS engine
            self.stream = TextToAudioStream(engine=self.engine) #fake cable output_device_index=15
            self.engine.set_voice("am_michael")
            self.recorder = AudioToTextRecorder(language="en",enable_realtime_transcription=True,silero_sensitivity=0.4,post_speech_silence_duration=0.2,min_gap_between_recordings=0.5)


            self.setWindowTitle("My App")
            self.button_is_checked = True

            self.Voices = "am_michael"
            self.Output = 1
            self.Input = 1
            self.Running = False

            EngineLabel = QLabel("TTS Engine")

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
            layout.addWidget(EngineLabel)
            layout.addWidget(VoiceLabel)
            layout.addWidget(VoiceSelectionBox)
            layout.addWidget(OutputCableLabel)
            layout.addWidget(OutputCableSelectionBox)
            layout.addWidget(InputCableLabel)
            layout.addWidget(InputCableSelectionBox)
            button1 = QPushButton("Start!")
            button1.clicked.connect(self.mainloop)
            button2 = QPushButton("Kill!")
            button2.clicked.connect(self.killLoop)
            button3 = QPushButton("diag!")
            button3.clicked.connect(self.spitShit)
            layout.addWidget(button1)
            layout.addWidget(button2)
            layout.addWidget(button3)

            container = QWidget()
            container.setLayout(layout)

            self.setMinimumSize(QSize(400, 300))

            # Set the central widget of the Window.
            self.setCentralWidget(container)
        def setVoices(self, text):
            self.Voices = text
            self.engine.set_voice(text)
            print(text)
        def setOutput(self, text):
            self.Output = text
            self.stream.output_device_index = str(text[:1])
            print(text)
        def setInput(self, text):
            self.Input = text
            self.recorder.input_device_index = str(text[:1])
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
        def process_text(self,text):
            print(text)
            if "command 47" in text:
                self.Running = False
                self.engine.shutdown()
                self.recorder.shutdown()
                print("should shut down now")
            else:
                self.stream.feed(text)
                self.stream.play_async()
        def mainloop(self):
            print("Wait until it says 'speak now'")
            self.Running = True
            
            while self.Running:
                self.recorder.text(self.process_text)
        def killLoop(self):
            self.Running = False
        def spitShit(self):
            print("Stream odi: "+str(self.stream.output_device_index))
            print("Recorder odi: "+str(self.recorder.input_device_index))
            print("Running: "+str(self.Running))

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()
