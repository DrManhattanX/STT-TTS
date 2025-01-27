from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, GTTSEngine ,SystemEngine, KokoroEngine
from datetime import time
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from MenuMainKokoro import MainWindow as GUI
import pyaudio
import sys
_ESPEAK_LIBRARY = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)

#Please follow links to install dependencies
#https://github.com/KoljaB/RealtimeSTT
#https://github.com/KoljaB/RealtimeTTS

if __name__ == '__main__':

    def transcribe(file):
        if __name__ == '__main__':
            print("Wait until it says 'speak now'")
            recorder = AudioToTextRecorder(language="jp",enable_realtime_transcription=True,silero_sensitivity=0.6,post_speech_silence_duration=0.1,min_gap_between_recordings=0.2,use_microphone=False)
            with open(file, "rb") as f:
                audio_chunk = f.read()
            orig_stdout = sys.stdout
            f = open("output.txt", 'w')
            sys.stdout = f

            recorder.feed_audio(audio_chunk)
            print("Transcription: ", recorder.text())

            sys.stdout = orig_stdout
            f.close()
            
    transcribe("")
