import requests
import json

URL = 'http://localhost:1207/'

class NER:
	def request_ner(self, text, tag):
		res = requests.post(URL, json={'text' : text})
		listNer = json.loads(res.text)
		try:
			out = listNer[tag]
		except:
			out = []
		return out


if __name__ == '__main__':
	ner = NER()
	txt = (ner.request_ner('Tao ở Hà Nội , và mới chuyển qua Hồ Chí Minh. à tiện tao tên là Nguyễn Huy Tuyển', 'PER'))
	print(txt)