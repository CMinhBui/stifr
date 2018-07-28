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
            if intent == "lock":
                self.process_lock()
            elif intent == "credit_due":
                self.process_credit_due()
            elif intent == "registration":
                self.process_regist()
            elif intent == "call_person":
                self.process_call()
                break
            else:
                is_done = self.process_unknown()

            intent, is_done = self.ask_again()
            if(is_done):
                break

    def process_lock(self):
        if(not self.database.has_phone_num(self.phone_num)):
            self.sound_handler.play_sound("num_not_exist.wav")
        elif not self.loggin_state:
            self.loggin()

        if self.loggin_state:
            #if logged in, ask what card user need to lock
            self.sound_handler.play_sound("ask_card.wav")
            response = self.sound_handler.recognize()
            keyword = self._extract_keyword_lockcard(response)

            if keyword == "debit":
                self.sound_handler.play_sound("lock_debit.wav")
            elif keyword == "credit":
                self.sound_handler.play_sound("lock_credit.wav")
            elif keyword == "atm":
                self.sound_handler.play_sound("lock_atm.wav")
            else:
                self.process_unknown()

    def process_credit_due(self):
        pass

    def process_regist(self):
        pass
        
                

    def process_unknown(self):
        #say that not understand the answer and ask if need to connect with person
        self.sound_handler.play_sound("unknown.wav")
        text = self.sound_handler.recognize()
        intent = self.intent_classifier.classify(text)
        yesno_answer = self.yesno_classifier.classify(text)
        
        if(intent == "call_person" or yesno_answer == "yes"):
            self.process_call()

        return is_done

    def hello(self):
        self.sound_handler.play_sound("hello.wav")
        text = self.sound_handler.recognize()
        intent = self.intent_classifier.classify(text)

        return intent

    def loggin(self):
        self.sound_handler.play_sound("require_login.wav")
        audio_data = self.sound_handler.record_sound()
        result = self.verifier.verify(self.phone_num, audio_data)
        if result:
            self.loggin_state = True
        else:
            self.sound_handler.play_sound("not_success.wav")

    def ask_again(self):
        self.sound_handler.play_sound("ask_again.wav")
        text = self.sound_handler.recognize()
        is_done = False

        intent = self.intent_classifier.classify(text)
        if intent = "unknow":
            yesno_answer = self.yesno_classifier(text)
            if yesno_answer == "no":
                is_done = True
            else:
                self.process_unknown()

        return intent, is_done
        