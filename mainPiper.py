if __name__ == '__main__':
    from RealtimeSTT import AudioToTextRecorder
    from RealtimeTTS import TextToAudioStream, PiperEngine, PiperVoice
    from datetime import time
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    import pyaudio
    import sys
    _ESPEAK_LIBRARY = 'C:/Program Files/eSpeak NG/libespeak-ng.dll'
    EspeakWrapper.set_library(_ESPEAK_LIBRARY)

    #Please follow links to install dependencies
    #https://github.com/KoljaB/RealtimeSTT
    #https://github.com/KoljaB/RealtimeTTS

    #vars
    if len(sys.argv) > 1:
        outputARG = int(sys.argv[2])
        inputARG = int(sys.argv[3])
    else: #9 for system /// 15 for Vcable
        outputARG = 9
        inputARG = 1

    Running = False

    voice = PiperVoice(
        model_file="C:/Users/ty10r/Desktop/Projects/Python Stuff/piper/piper-voices/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx",
        config_file="C:/Users/ty10r/Desktop/Projects/Python Stuff/piper/piper-voices/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json",
    )

    engine = PiperEngine(
        piper_path="C:/Users/ty10r/Desktop/Projects/Python Stuff/piper/piper.exe",
        voice=voice,
    )
    stream = TextToAudioStream(engine=engine,output_device_index=outputARG) #fake cable output_device_index=15
    recorder = AudioToTextRecorder(language="en",enable_realtime_transcription=True,silero_sensitivity=0.4,post_speech_silence_duration=0.2,min_gap_between_recordings=0.5,input_device_index=inputARG)


    def process_text(text):
        print(text)
        if "command 47" in text:
            engine.shutdown()
            recorder.shutdown()
            print("should shut down now")
            global Running
            Running = False
        else:
            stream.feed(text)
            stream.play_async()
        
    def mainloop():
        print("Wait until it says 'speak now'")
        global Running
        Running = True
        while Running:
            recorder.text(process_text)
                
    def test():
        stream.feed("This is piper tts speaking.")
        stream.play()
            

    #mainloop()
    test()
    engine.shutdown()
    exit()