from Identification import IdentificationServiceHttpClientHelper
from db import Database
import wave
import os

class Verifier:

	def __init__(self, database, api_key='178ffd64a74f49f799a20e1d247056f0'):
		self.helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(api_key)
		self.db = database


	def verify(self, phone_number, data):
		profile_id = self.db.get_profile_id(phone_number)
		file_path = "verify_data.wav"
		with wave.open(file_path, 'wb') as file:
			file.setnchannels(1)
			file.setsampwidth(2)
			file.setframerate(16000)

			file.writeframes(data)

		identification_response = self.helper.identify_file(file_path, [profile_id], True)
		os.remove(file_path)
		print(identification_response.get_identified_profile_id())
		print(identification_response.get_confidence())


		return identification_response.get_identified_profile_id() == profile_id

