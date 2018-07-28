# -*- coding: utf-8 -*-
from AudioRecog import *
from Record import *
import fastText
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == "__main__":
    model = fastText.load_model('intent.bin')
    client = initEnv()
    data = record_to_file('demo.wav')
    print("done - result is loading to recognize")
    start = time.time()
    transcripts = recognize(client, data)
    end = time.time()
    print(end-start)
    start = end
    intent = model.predict(transcripts[0])
    print(u"Ý định của bạn là  {}".format(intent[0][0][9:]))
    end = time.time()
    print(end-start)
