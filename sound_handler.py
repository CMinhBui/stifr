import pyaudio
import webrtcvad
from constants import CHUNK_SIZE, FORMAT, RATE
import os
import wave
import AudioRecog
from fake_answers import FAKE_ANSWER

class SoundHandler:

    def __init__(self, stop_delay=75):
        self.is_recording = False
        self.data_buffer = []
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)
        self.p = None
        self.stream = None
        self.stop_delay = stop_delay
        self.silent_count = 0
        self.stream_out = None
        self.client = AudioRecog.initEnv()
        self.is_speech_start = False
        self.continuos_speech_count = 0
    
    def _callback(self, in_data, frame_count, time_info, status):
        if(self.is_recording):
            self.data_buffer.append(in_data)
            # print(self.silent_count)
            try:
                if(self.vad.is_speech(in_data, RATE)):
                    self.continuos_speech_count += 1
                    if self.continuos_speech_count > 10:
                        self.silent_count = 0
                else:
                    if self.continuos_speech_count > 15:
                        self.is_speech_start = True
                    self.continuos_speech_count = 0
                    if self.is_speech_start:
                        self.silent_count += 1
                        
            except:
                print(in_data)
                raise

            if(self.silent_count > self.stop_delay):
                self.is_recording = False
                self.is_speech_start = False
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
            start_at = 0
            while(not self.vad.is_speech(result[start_at], RATE)):
                start_at += 1
            end_at = len(result) - 50
            result = result[start_at-1:end_at]

        result = b''.join(result)
        return result

    def recognize(self):
        data = self.start_record()
        transcripts = AudioRecog.recognize(self.client, data)
        transcripts = map(lambda x: x.strip(), transcripts)
        return ' '.join(transcripts)
        

    def play_sound(self, filepath):
        print('\n' + FAKE_ANSWER[filepath] + '\n')
        # sound_wave = wave.open(filepath, 'rb')
        # data = sound_wave.readframes(sound_wave.getnframes())
        # self.stream_out.write(data)

if __name__ == "__main__":
    tmp = SoundHandler()
    tmp.start()
    data = tmp.start_record()
    with wave.open("data.wav", 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000)

        file.writeframes(data)

    transcripts = AudioRecog.recognize(tmp.client, data)
    transcripts = map(lambda x: x.strip(), transcripts)
    print(' '.join(transcripts))
    tmp.end()
