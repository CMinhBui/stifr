import sqlite3

sqlite_file = 'bankdb.sqlite'

class Database():
	def __init__(self):
		self.db = sqlite3.connect(sqlite_file)

	def has_phone_num(self, phonenum):
		c = self.db.cursor()
		c.execute('SELECT * FROM {} WHERE {} = {}'.format('customer', 'phone', phonenum))
		id_exists = c.fetchone()
		return id_exists

	def get_profile_id(self, phonenum):
		detail = self.has_phone_num(phonenum)
		if detail:
			return detail[-1]
		else:
			return None

if __name__ == "__main__":
	d = Database()
	print(d.has_phone_num('01693530097'))