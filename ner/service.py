from flask import request, Flask, jsonify

from model import EntityLSTM
import pickle
import tensorflow as tf
from constants import *
from dataset import Dataset, MappingAndEmbedding

sess = tf.Session()
pretrained_model_folder = MODELS_FOLDER + '/vi.vec_100d_89_f1_macro'

with open(pretrained_model_folder + MAPPING_EMBEDDING_FILE, 'rb') as file:
	mapping_embedding = pickle.load(file)

model = EntityLSTM(mapping_embedding.embedding_tensor, 32)
transition_params = model.restore_pretrained_model(sess, pretrained_model_folder)

def valid_entity(result):
	output = {}
	for pair in result:
		tag = pair[1]
		NameEntity = ''
		n = len(pair[0]) - 1
		for i in range(n):
			NameEntity += pair[0][i] + ' '
		NameEntity += pair[0][n]
		try:
			output[tag].append(NameEntity)
		except:
			output[tag] = [NameEntity]
	return output
def valid_email(str_):
	email = re.findall(r'\d*[a-z]+\d*@[a-z]+.[a-z]+', str_)
	if (len(email)):
		return email
	return []

def valid_number(str_):
	num = re.findall(r'\d{9,}', str_)
	if (len(num)):
		return num
	return []

def valid_date(str_):
	date = re.findall(r'\d+', str_)
	if (len(date) < 3):
		return [] 
	elif date[0] > 31 or date[1] > 12 or date[2] < 40 or (date[2] > 99 and date[2] < 1940) or date[2] > 2000 :
		return[]
	if (date[2] < 100):
		date[2] = 1900 + date[2]
	out = str(date[0]) + ' / ' + str(date[1]) + '  / ' + str(date[2])
	return [out]

app = Flask(__name__)

@app.route('/', methods=["POST"])
def service():
	index_input = request.json['text']
	text = str(index_input)

	result = model.predict(sess, transition_params, mapping_embedding, text)
	result['EMAIL'] = valid_email(text)
	result['NUM'] = valid_number(text)
	result['DATE'] = valid_date(text)

	output_list = valid_entity(result)
	print(output_list)
	print(len(output_list))
	return jsonify(output_list)

app.run('0.0.0.0', port=1207)
