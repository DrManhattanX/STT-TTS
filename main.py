from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, GTTSEngine ,SystemEngine, KokoroEngine
from datetime import time
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from MenuMain import MainWindow as GUI
import pyaudio
import sys
_ESPEAK_LIBRARY = 'C:\Program Files\eSpeak NG\libespeak-ng.dll'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)

#Please follow links to install dependencies
#https://github.com/KoljaB/RealtimeSTT
#https://github.com/KoljaB/RealtimeTTS

if __name__ == '__main__':
    kokoro_root = "C:/Users/ty10r/Desktop/Projects/Python Stuff/Kokoro-82M"

    engine = KokoroEngine(kokoro_root=kokoro_root,) # replace with your TTS engine
    stream = TextToAudioStream(engine=engine) #fake cable output_device_index=15
    engine.set_voice("bm_george")
        # Pick one of: 
        # "af_nicole", 
        # "af",
        # "af_bella",
        # "af_sarah",
        # "am_adam",
        # "am_michael",
        # "bf_emma",
        # "bf_isabella",
        # "bm_george",
        # "bm_lewis",
        # "af_sky"
        ############## am_michael & bm_george for male | bf_isabella for female

    def process_text(text):
        print(text)
        if "command 47" in text:
            quit()
        else:
            stream.feed(text)
            stream.play_async()
        
    def mainloop():
        if __name__ == '__main__':
            print("Wait until it says 'speak now'")
            recorder = AudioToTextRecorder(language="en",enable_realtime_transcription=True,silero_sensitivity=0.4,post_speech_silence_duration=0.2,min_gap_between_recordings=0.5)

            while True:
                recorder.text(process_text)
                
    def test():
        stream.feed("bro coli is the way to play the dang game.")
        stream.play()
            

    #mainloop()
    #test()
    #engine.shutdown()
