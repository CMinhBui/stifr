import pyaudio

USER_ID = 'usr_f1865f5c17b047b18a29686099d7fa45'
CHUNK_SIZE = 320
RATE = 16000
FORMAT = pyaudio.paInt16

PATH_TO_QUESTION = 'source/registration/'
questions = ['name', 'phone', 'idcard', 'email', 'location']
tags = ['PER', 'NUM', 'NUM', 'EMAIL', 'LOC']
