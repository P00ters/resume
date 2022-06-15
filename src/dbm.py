import base64
import datetime
import hashlib
import os
import shutil
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
			
	def is_intact (self):
		owner_id = None
		query = '''SELECT Accounts.id 
					FROM Accounts, Groups
					WHERE Accounts.group_id = Groups.id
						AND Groups.name="Owners";'''
		result = self.execute(query)
		if result != None:
			result = self.cur.fetchall()
			if len(result) > 0:
				owner_id = result[0][0]
		
		if owner_id == None:
			return False
						
		tables = ['Addresses', 'Education', 'Jobs', 'Orgs', 'Skills']
		query = '''SELECT id, created_by, modified_by FROM '''
		
		for t in tables:
			q = query + t + ' WHERE created_by<>' + owner_id + ' OR modified_by<>' + owner_id + ';'
			result = self.execute(q)
			if result != None:
				result = self.cur.fetchall()
				if len(result) > 0:
					return False
		
		backuppath = self.db_path + '.bak.sqlite'
		md5_backup = hashlib.md5(open(backuppath, 'rb').read()).hexdigest()
		md5_current = hashlib.md5(open(self.db_path, 'rb').read()).hexdigest()
		if md5_backup != md5_current:
			return False
		
		return True

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
		
		self.do_backup()
	
	def do_backup (self):
		backuppath = self.db_path + '.bak.sqlite'
		shutil.copy(self.db_path, backuppath)
		
	def restore_from_backup (self):
		backuppath = self.db_path + '.bak.sqlite'
		shutil.copy(backuppath, self.db_path)
		
	def imgtobin(self, path):
		file = open(path, 'rb').read()
		file = base64.b64encode(file)
		return file
		