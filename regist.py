import pandas as pd
from constants import *
from sound_handler import SoundHandeler
from ner_service import NerDetect


class Registration:
	def __init__(self, sound_handler, ner, questions, tags):
		self.sound_handler = sound_handler
		self.ner = ner
		self.questions = questions
		self.tags = tags
	
	# def __init__(self, ner, questions, tags):
	# 	self.ner = ner
	# 	self.questions = questions
	# 	self.tags = tags

	def answer (self, file):
		self.sound_handler.play_sound(file + '.wav')
		# print(file)

	def getInfo(self, text, tag):
		return ner.request_ner(text, tag)

	def fill_form (self, text, questions, tags, num):
		if ('tín dụng' in text):
			self.answer('employee')
			return False
		elif ('ghi nợ' in text):
			count = 0
			n = len(questions)
			i = 0
			infomation = []
			while i < n:
				ques = questions[i]
				tag = tags[i]
				self.answer(ques)
				text_received = self.sound_handler.recognize()
				# text_received = input('recognize : ')
				info = self.getInfo(text_received, tag)
				if (len(info) == 0):
					count += 1
					if (count == 5):
						self.answer('employee')
						return False
					continue
				else:
					i += 1
					infomation.append(info)
			
			print(infomation)
			self.answer('ending')
			return True
		else:
			num += 1
			if (num == 5):
				self.answer('employee')
				return False
			self.answer('advise')
			text_received = self.sound_handler.recognize()
			# text_received = input('recognize : ')
			return self.fill_form(text_received, questions, tags, num)

	def process(self):
		self.answer('card')
		text = self.sound_handler.recognize()
		# text = input('recognize : ')
		if ('tín dụng' in text) or ('ghi nợ' in text):
			out = self.fill_form(text, self.questions, self.tags, 0)
		else:
			self.answer('advise')
			text = self.sound_handler.recognize()
			# text = input('recognize : ')
			out = self.fill_form(text, self.questions, self.tags, 0)
		return out

if __name__ == '__main__':
	# sound_handler = SoundHandeler()
	ner = NerDetect()
	regist = Registration(ner, questions, tags)
	out = regist.process()
	print(out)

