
class Registration:
	def __init__(self, sound_handler, ner, questions, tags):
		self.sound_handler = sound_handler
		self.ner = ner
		self.questions = questions
		self.tags = tags
	
	def answer (self, file):
		### Change code here
		print(file)
		self.sound_handler.play_sound(file + '.wav')

	def getInfo(text, tag):
		return ner.request_ner(text, tag)

	def fill_form (self, text, questions, tags, num):
		if ('tín dụng' in text):
			answer('employee')
			return False
		elif ('ghi nợ' in text):
			count = 0
			n = questions.len()
			i = 0
			while i < n:
				ques = questions[i]
				tag = tags[i]
				answer(ques)
				text_received = self.sound_handler.recognize()
				info = getInfo(text_received, tag)
				if (len(info) == 0):
					count += 1
					if (count == 5):
						answer('employee')
						return False
					continue
				else:
					i += 1
					infomation.append(info)
			return True
		else:
			num += 1
			if (num == 5):
				answer('employee')
				return False
			answer('advise')
			text_received = self.sound_handler.recognize()
			return fill_form(text_received, questions, tags, num)

	def process():
		answer('card')
		text = self.sound_handler.recognize()
		if ('tín dụng' in text) or ('ghi nợ' in text):
			out = fill_form(text, self.questions, self.tags, 0)
		else:
			answer('advise')
			text = self.sound_handler.recognize()
			out = fill_form(text, self.questions, self.tags, 0)
		return out



