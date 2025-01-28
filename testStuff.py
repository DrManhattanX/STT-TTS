import tkinter as tk
from tkinter import ttk
import pyaudio
 
class Window:
    def __init__(self, master):
        self.master = master
 
        # Frame
        self.frame = tk.Frame(self.master, width = 200, height = 200)
        self.frame.pack()
 
        self.VoiceSBox = ["am_michael", "af_nicole", "af_bella", "af_sarah", "am_adam", "bf_emma", "bf_isabella", "bm_george", "bm_lewis", "af_sky"]
        self.Voicecombo = ttk.Combobox(self.frame, values = self.VoiceSBox, state = "readonly")
        self.Voicecombo.set("Pick an Option")
        self.Voicecombo.place(x = 20, y = 40)

        self.OutCableSBox = self.getAllAudioDevices()
        self.OutCablecombo = ttk.Combobox(self.frame, values = self.OutCableSBox, state = "readonly")
        self.OutCablecombo.set("Pick an Option")
        self.OutCablecombo.place(x = 20, y = 80)

        self.InCableSBox = self.getAllAudioDevices()
        self.InCablecombo = ttk.Combobox(self.frame, values = self.InCableSBox, state = "readonly")
        self.InCablecombo.set("Pick an Option")
        self.InCablecombo.place(x = 20, y = 120)
    
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
 
 
root = tk.Tk()
root.title("Tkinter")
 
window = Window(root)
root.mainloop()