from intent_service import YesNoClassifier, IntentClassifier
from sound_handler import SoundHandler
# from verify_service import Verifier
from db import Database
from session import Session

intent_classifier = IntentClassifier()
yesno_classifier = YesNoClassifier()
sound_handler = SoundHandler()
sound_handler.start()
verifier = None
db = Database()
while(True):
    phone_num = input("Phone number: ")
    sess = Session(phone_num, intent_classifier, yesno_classifier, sound_handler, verifier, db)
    sess.run()