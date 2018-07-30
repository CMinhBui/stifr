import requests

INTENT_URL = 'http://localhost:1812/intention'
YESNO_URL = 'http://localhost:1812/yesno'

class IntentClassifier:
    def classify(self, text):
        res = requests.post(INTENT_URL, json={'text' : text.lower()})
        response = res.text
        print(text)
        if(response == 'unknown'):
            if 'khóa' in text.lower():
                response = 'lock'
                print("yes")
            elif 'mở' in text.lower() or 'đăng ký' in text.lower() or 'làm thẻ' in text.lower():
                response = 'registration'

        return response

class YesNoClassifier:
    def classify(self, text):
        res = requests.post(YESNO_URL, json={'text' : text.lower()})
        return res.text

if __name__ == "__main__":
    intentclassifier = IntentClassifier()
    print(intentclassifier.classify('mình muốn khóa thẻ'))
    yesnoclassifier = YesNoClassifier()
    print(yesnoclassifier.classify('Không cần đâu'))