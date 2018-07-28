import pyaudio
import webrtcvad
from constants import CHUNK_SIZE, FORMAT, RATE
import os
import wave
import AudioRecog

class SoundHandler:

    def __init__(self, stop_delay=100):
        self.is_recording = False
        self.data_buffer = []
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(1)
        self.p = None
        self.stream = None
        self.stop_delay = stop_delay
        self.silent_count = 0
        self.stream_out = None
        self.client = AudioRecog.initEnv()
    
    def _callback(self, in_data, frame_count, time_info, status):
        if(self.is_recording):
            self.data_buffer.append(in_data)
            # print(self.silent_count)
            try:
                if(self.vad.is_speech(in_data, RATE)):
                    self.silent_count = 0
                else:
                    self.silent_count += 1

            except:
                print(in_data)
                raise

            if(self.silent_count > self.stop_delay):
                self.is_recording = False
                self.silent_count = 0
        
        return (in_data, pyaudio.paContinue)
        
    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=1,
            rate=RATE,
            input=True,
            stream_callback=self._callback,
            frames_per_buffer=CHUNK_SIZE
        )
        self.stream.start_stream()

        self.stream_out = self.p.open(
            format=FORMAT,
            channels=1,
            rate=RATE,
            input=False,
            output=True
        )

    def end(self):
        if(self.stream != None and self.p != None and self.stream_out != None):
            self.stream.stop_stream()
            self.stream.close()
            self.stream_out.stop_stream()
            self.stream_out.close()
            self.p.terminate()
            self.p = None
            self.stream = None
            self.stream_out = None

    def start_record(self):
        if(not self.is_recording):
            self.is_recording = True
            print("Recording...")

        while(self.is_recording):
            pass

        result = []
        if(len(self.data_buffer) > 0):
            result = self.data_buffer
            self.data_buffer = []
        
        result = b''.join(result)
        return result

    def recognize(self):
        data = self.start_record()
        transcripts = AudioRecog.recognize(self.client, data)
        return transcripts[0]

    def play_sound(self, filepath):
        sound_wave = wave.open(filepath, 'rb')
        data = sound_wave.readframes(sound_wave.getnframes())
        self.stream_out.write(data)

if __name__ == "__main__":
    tmp = SoundHandler()
    tmp.start()
    print(tmp.recognize())
    tmp.end()