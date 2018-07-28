# from utils import questions, tags
from regist import Registration
from ner_service import NerDetect
from constants import *

class Session:
    
    def __init__(self, phone_num, intent_classifier, yesno_classifier, sound_handler, verifier, database):
        self.phone_num = phone_num
        self.intent_classifier = intent_classifier
        self.yesno_classifier = yesno_classifier
        self.sound_handler = sound_handler
        self.verifier = verifier
        self.database = database
        self.loggin_state = False

    def run(self):
        intent = self.hello()
        is_done = False
        
        while(True):
            print(intent)
            if intent == "lock":
                is_done = self.process_lock()
            
            elif intent == "credit_due":
                self.process_credit_due()

            elif intent == "registration":
                is_done = self.process_regist()
            
            elif intent == "call_person":
                self.process_call()
                break
            
            else:
                is_done = self.process_unknown()

            if(is_done):
                break

            intent, is_done = self.ask_again()
            if(is_done):
                break

    def process_lock(self):
        is_done = False

        if(not self.database.has_phone_num(self.phone_num)):
            self.sound_handler.play_sound("num_not_exist.wav")
        elif not self.loggin_state:
            self.loggin()

        if self.loggin_state:
            #if logged in, ask what card user need to lock
            self.sound_handler.play_sound("ask_lock.wav")
            response = self.sound_handler.recognize().lower()
            
            if "tín dụng" in response or "credit" in response or "ghi nợ" in response or "debit" in response or "atm" in response:
                self.sound_handler.play_sound("lock_success.wav")
            else:                
                is_done = self.process_unknown()

        return is_done

    def process_credit_due(self):
        if(not self.database.has_phone_num(self.phone_num)):
            self.sound_handler.play_sound("num_not_exist.wav")
        elif not self.loggin_state:
            self.loggin()

        if self.loggin_state:
            self.sound_handler.play_sound("credit_due.wav")

    def process_regist(self):
        ner = NerDetect()
        regist = Registration(self.sound_handler, ner, QUESTIONS, TAGS, self)
        information, is_done = regist.process()
        print(information)

        return is_done

    def process_unknown(self):
        #say that not understand the answer and ask if need to connect with person
        self.sound_handler.play_sound("unknown.wav")
        text = self.sound_handler.recognize()
        intent = self.intent_classifier.classify(text)
        yesno_answer = self.yesno_classifier.classify(text)
        is_done = False
        
        if(intent == "call_person" or yesno_answer == "yes"):
            self.process_call()
            is_done = True

        return is_done

    def process_call(self):
        self.sound_handler.play_sound("calling_person.wav")

    def hello(self):
        self.sound_handler.play_sound("hello.wav")
        text = self.sound_handler.recognize()
        intent = self.intent_classifier.classify(text)

        return intent

    def loggin(self):
        self.sound_handler.play_sound("require_login.wav")
        self.sound_handler.play_sound("voice_verify.wav")
        audio_data = self.sound_handler.start_record()
        
        # result = self.verifier.verify(self.phone_num, audio_data)
        result = True
        if result:
            self.loggin_state = True
        else:
            self.sound_handler.play_sound("not_success.wav")

    def ask_again(self):
        self.sound_handler.play_sound("ask_again.wav")
        text = self.sound_handler.recognize()
        is_done = False

        intent = self.intent_classifier.classify(text)
        if intent == "unknown":
            yesno_answer = self.yesno_classifier.classify(text)
            if yesno_answer == "no":
                is_done = True

        return intent, is_done
        