import hashlib
import uuid

from groups import Group

class Account:
	def __init__ (self, id, username, password, salt, name, group):
		self.id = id
		self.username = username
		self.password = password
		self.salt = salt
		self.name = name
		self.group = group

	def create (self, dbm):
		query = '''INSERT INTO 'Accounts'
					('id', 'name', 'username', 'password', 'salt', 'group_id')
					VALUES
					(?, ?, ?, ?, ?, ?);'''

		dbm.execute_d(query, (self.id, self.name, self.username, self.password, self.salt, self.group.id))

	def update (self, dbm):
		query = '''UPDATE Accounts
					SET id=?, name=?, username=?, password=?, salt=?, group_id=?
					WHERE id=?;'''
		dbm.execute_d(query, (self.id, self.name, self.username, self.password, self.salt, self.group.id, self.id))

	def delete (self, dbm):
		query = '''DELETE FROM Accounts
					WHERE id="'''+self.id+'''";'''
		dbm.execute(query)

	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		name = kwargs.get('name', None)
		username = kwargs.get('username', None)
		password = kwargs.get('password', None)
		salt = kwargs.get('salt', None)
		group_name = kwargs.get('group_name', None)
		group_id = kwargs.get('group_id', None)

		query = "SELECT Accounts.id, Accounts.username, Accounts.password, Accounts.salt, Accounts.name, Groups.id, Groups.name, Groups.auth_key FROM Accounts, Groups WHERE Accounts.group_id = Groups.id AND "
		if id != None or name != None or username != None or password != None or salt != None or group_id != None or group_name != None:
			if id != None:
				query += 'Accounts.id="' + id + '" AND '
			if name != None:
				query += 'Accounts.name="' + name + '" AND '
			if username != None:
				query += 'Accounts.username="' + username + '" AND '
			if password != None:
				query += 'Accounts.password="' + password + '" AND '
			if salt != None:
				query += 'Accounts.salt="' + salt + '" AND '
			if group_name != None:
				query += 'Groups.name="' + group_name + '" AND '
			if group_id != None:
				query += 'Accounts.group_id="' + group_id + '";'

		if query[-4:] == 'AND ':
			query = query[:-4]
			query += ';'

		result = dbm.execute(query)
		if result != None:
			result = dbm.cur.fetchall()
			if len(result) == 1:
				self.id = result[0][0]
				self.username = result[0][1]
				self.password = result[0][2]
				self.salt = result[0][3]
				self.name = result[0][4]
				self.group = Group(result[0][5], result[0][6], result[0][7])
				return True


		return False

	def is_empty (self):
		if self.id == None and self.username == None and self.password == None and self.salt == None and self.name == None and self.group_id == None:
			return True
		return False

	def password_equals(self, password):
		if self.password == hashlib.sha512((password + self.salt).encode('utf-8')).hexdigest():
			return True
		else:
			return False

	def debug (self):
		obj = 	{
					'id': self.id,
					'username': self.username,
					'password': self.password,
					'salt': self.salt,
					'name': self.name,
					'group': 	{
									'id': self.group.id,
									'name': self.group.name,
									'auth_key': self.group.auth_key
								}
				}
		print(str(obj))

	def dict (self):
		obj = 	{
					'id': self.id,
					'username': self.username,
					'password': self.password,
					'salt': self.salt,
					'name': self.name,
					'group': 	{
									'id': self.group.id,
									'name': self.group.name,
									'auth_key': self.group.auth_key
								}
				}
		return obj


def NoneAccount ():
	return Account(None, None, None, None, None, None)

def retrieve_all_accounts (dbm):
	query = "SELECT Accounts.id, Accounts.username, Accounts.password, Accounts.salt, Accounts.name, Groups.id, Groups.name, Groups.auth_key FROM Accounts, Groups WHERE Accounts.group_id=Groups.id;"

	all_accounts = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				a = Account(row[0], row[1], row[2], row[3], row[4], Group(row[5], row[6], row[7]))
				all_accounts.append(a)

	return all_accounts

def retrieve_accounts (dbm, **kwargs):
	id = kwargs.get('id', None)
	username = kwargs.get('username', None)
	password = kwargs.get('password', None)
	salt = kwargs.get('salt', None)
	name = kwargs.get('name', None)
	group_id = kwargs.get('group_id', None)

	query = "SELECT Accounts.id, Accounts.username, Accounts.password, Accounts.salt, Accounts.name, Groups.id, Groups.name, Groups.auth_key FROM Accounts, Groups"

	if id != None or username != None or password != None or salt != None or name != None or group_id != None:
		query += ' WHERE '
		if id != None:
			query += 'Accounts.id="' + id + '" AND '
		if username != None:
			query += 'Accounts.username="' + username + '" AND '
		if password != None:
			query += 'Accounts.password="' + password + '" AND '
		if salt != None:
			query += 'Accounts.salt="' + salt + '" AND '
		if name != None:
			query += 'Accounts.name="' + name + '" AND '
		if group_id != None:
			query += 'Accounts.group_id="' + group_id + '";'
	else:
		query += ';'

	if query[-4:] == 'AND ':
			query = query[:-4]
			query += ';'

	acts = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				a = Account(row[0], row[1], row[2], row[3], row[4], Group(row[5], row[6], row[7]))
				acts.append(a)

	return acts


def retrieve_accounts_custom (dbm, sql):
	query = "SELECT Accounts.id, Accounts.username, Accounts.password, Accounts.salt, Accounts.name, Groups.id, Groups.name, Groups.auth_key FROM Accounts, Groups WHERE Accounts.group_id=Groups.id AND " + sql

	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'

	acts = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				a = Account(row[0], row[1], row[2], row[3], row[4], Group(row[5], row[6], row[7]))
				acts.append(a)

	return acts

def retrieve_accounts_fcustom (dbm, query):

	acts = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				a = Account(row[0], row[1], row[2], row[3], row[4], Group(row[5], row[6], row[7]))
				acts.append(a)

	return acts
