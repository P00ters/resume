import base64
import datetime
import hashlib
import os
import sqlite3
from urllib.parse import urlencode
import uuid

from populate import Populate


class DBM:
	def __init__(self, db_path, init):
		self.db_path = db_path
		self.init = init
		if self.valid():
			self.connect()
		else:
			self.instantiate()
			
	def execute(self, query):
		try:
			res = self.cur.execute(query)
			self.con.commit()
			return res
		except sqlite3.Error as e:
			print(e.args[0])
			return None
	
	def execute_d(self, query, data):
		try: 
			res = self.cur.execute(query, data)
			self.con.commit()
			return res
		except sqlite3.Error as e:
			print(e.args[0])
			return None

	def connect(self):
		self.con = sqlite3.connect(self.db_path, check_same_thread=False)
		self.cur = self.con.cursor()

	def close(self):
		self.cur.close()
		self.con.close()

	def valid(self):
		if os.path.isfile(self.db_path):
			return True
		else:
			return False
			
	def genid(self):
		id = uuid.uuid4().hex
		id = "-".join(id[i:i+8] for i in range(0, len(id), 8))
		return id
		
	def reset(self):
		self.close()
		if os.path.exists(self.db_path):
			os.remove(self.db_path)
			self.instantiate()

	def instantiate(self):
		db = open(self.db_path, "x")
		db.close()
		self.connect()
		
		with open('../dat/def/schema.sql') as sql:
			script = sql.read()
			
		self.cur.executescript(script)
		
		p = Populate(self)
		p.population()
		
		if (self.init):
			p.custom_population()
		
	def imgtobin(self, path):
		file = open(path, 'rb').read()
		file = base64.b64encode(file)
		return file
		