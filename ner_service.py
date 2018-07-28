import requests
import json

URL = 'http://localhost:1207/'

class NerDetect:
	def request_ner(self, text, tag):
		res = requests.post(URL, json={'text' : text})
		listNer = json.loads(res.text)
		print(listNer)
		try:
			out = listNer[tag]
		except:
			out = []
		return out


if __name__ == '__main__':
	ner = NerDetect()
	txt = (ner.request_ner('Tao ở Hà Nội , và mới chuyển qua Hồ Chí Minh. à tiện tao tên là Nguyễn Huy Tuyển, số điện thoại của tao là 01223530692', 'PER'))
	print(txt)