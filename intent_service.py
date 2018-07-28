import requests

INTENT_URL = 'http://localhost:1812/intention'
YESNO_URL = 'http://localhost:1812/yesno'

class IntentClassifier:
    def classify(self, text):
        res = requests.post(INTENT_URL, json={'text' : text})
        return res.text

class YesNoClassifier:
    def classify(self, text):
        res = requests.post(YESNO_URL, json={'text' : text})
        return res.text

if __name__ == "__main__":
    intentclassifier = IntentClassifier()
    print(intentclassifier.classify('mình muốn khóa thẻ'))
    yesnoclassifier = YesNoClassifier()
    print(yesnoclassifier.classify('tớ có'))