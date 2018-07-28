from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import io

# GOOGLE_APPLICATION_CREDENTIALS="/home/lego1st/Documents/Contests/VPBank18/SpeechToText/service-account-file.json"

def initEnv():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service-account-file.json"
    client = speech.SpeechClient()
    return client

def recognize(client, data):
    # with io.open(filename, 'rb') as audio_file:
    #    content = audio_file.read()
    # print (content)
    # print('recognize')
    content = data
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(\
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,\
            sample_rate_hertz=16000,\
            language_code="vi-VN")

    response = client.recognize(config, audio)
    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
    return transcripts

if __name__ == "__main__":
    client = initEnv()
    recognize(client, 'data')
    # with open('data', 'rb') as au:
    #     content = au.read()
    #     recognize(client, au)
