class Group:
	def __init__ (self, id, name, auth_key):
		self.id = id
		self.name = name
		self.auth_key = auth_key

	def create (self, dbm):
		query = '''INSERT INTO 'Groups'
					('id', 'name', 'auth_key') VALUES
					(?, ?, ?);'''
		dbm.execute_d(query, (self.id, self.name, self.auth_key))

	def update (self, dbm):
		query = '''UPDATE 'Groups'
					SET id=?, name=?, auth_key=?
					WHERE id=?;'''
		dbm.execute_d(query, (self.id, self.name, self.auth_key, self.id))

	def delete (self, dbm):
		query = '''DELETE FROM 'Groups'
					WHERE id="'''+self.id+'''";'''
		dbm.execute(query)

	def retrieve (self, dbm, **kwargs):
		name = kwargs.get('name', None)
		id = kwargs.get('id', None)
		auth_key = kwargs.get('auth_key', None)

		query = "SELECT * FROM Groups WHERE "
		if name != None or id != None or auth_key != None:
			if id != None:
				query += 'id="' + id + '" AND '
			if name != None:
				query += 'name="' + name + '" AND '
			if auth_key != None:
				query += 'auth_key="' + auth_key + '";'

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					self.id = result[0][0]
					self.name = result[0][1]
					self.auth_key = result[0][2]
					return True
		return False

	def is_empty (self):
		if (self.id == None and self.name == None and self.auth_key == None):
			return True
		return False

	def debug (self):
		obj = 	{
					'id': self.id,
					'name': self.name,
					'auth_key': self.auth_key
				}
		print(str(obj))

	def dict (self):
		obj = 	{
					'id': self.id,
					'name': self.name,
					'auth_key': self.auth_key
				}
		return obj


def NoneGroup ():
	return Group(None, None, None)

def retrieve_all_groups (dbm):
	query = "SELECT * FROM Groups;"

	all_groups = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				g = Group(row[0], row[1], row[2])
				all_groups.append(g)

	return all_groups

def retrieve_groups (dbm, **kwargs):
	id = kwargs.get('id', None)
	name = kwargs.get('name', None)
	auth_key = kwargs.get('auth_key', None)

	query = "SELECT * FROM Groups"

	if id != None or name != None or auth_key != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if name != None:
			query += 'name="' + name + '" AND '
		if auth_key != None:
			query += 'auth_key="' + auth_key + '";'
	else:
		query += ';'

	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'

	gs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				g = Group(row[0], row[1], row[2])
				gs.append(g)

	return gs


def retrieve_groups_custom (dbm, sql):
	query = "SELECT * FROM Groups " + sql

	gs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				g = Group(row[0], row[1], row[2])
				gs.append(g)

	return gs

def retrieve_groups_fcustom (dbm, query):

	gs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				g = Group(row[0], row[1], row[2])
				gs.append(g)

	return gs
