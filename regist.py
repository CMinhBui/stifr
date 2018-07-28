import pandas as pd
from constants import *
from sound_handler import SoundHandler
from ner_service import NerDetect


class Registration:
	def __init__(self, sound_handler, ner, questions, tags, session):
		self.sound_handler = sound_handler
		self.ner = ner
		self.questions = questions
		self.tags = tags
		self.session = session
	

	def getInfo(self, text, tag):
		return self.ner.request_ner(text, tag)

	def fill_form (self, text, questions, tags):
		is_done = False
		information = {}
		text = text.lower()

		if ('tín dụng' in text or 'credit' in text):
			self.sound_handler.play_sound('regist_credit.wav')
			text = self.sound_handler.recognize()
			
			intent = self.session.intent_classifier.classify(text)
			yesno_answer = self.session.yesno_classifier.classify(text)
			
			if(intent == "call_person" or yesno_answer == "yes"):
				self.session.process_call()
				is_done = True

		elif ('ghi nợ' in text or 'debit' in text):

			n = len(questions)
			i = 0
			while i < n:
				count = 0
				ques = questions[i]
				tag = tags[i]
				self.sound_handler.play_sound('ask_' + ques + '.wav')
				text_received = self.sound_handler.recognize()
				info = self.getInfo(text_received, tag)
				while(len(info) == 0 and count < 2):
					self.sound_handler.play_sound('reask_' + ques + '.wav')
					text_received = self.sound_handler.recognize()
					info = self.getInfo(text_received, tag)
					count += 1

				if(len(info) > 0):
					i += 1
					information[ques] = info[0]
				else:
					is_done = self.session.process_unknown()
					break

			if(len(information) == 3):
				self.sound_handler.play_sound("filled_form.wav")
			
		return information, is_done

	def process(self):
		self.sound_handler.play_sound("regist_card.wav")
		text = self.sound_handler.recognize()
		
		is_done = False
		out = None
		
		if ('tín dụng' in text) or ('ghi nợ' in text):
			out, is_done = self.fill_form(text, self.questions, self.tags)
		else:
			is_done = self.session.process_unknown()
		
		return out, is_done

if __name__ == '__main__':
	pass
	# session = Session()
	# sound_handler = SoundHandeler()
	# ner = NerDetect()
	# regist = Registration(sound_handler, ner, questions, tags, session)
	# out = regist.process()
	# print(out)