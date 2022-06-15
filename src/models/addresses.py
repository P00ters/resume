import accounts
from accounts import Account

class Address:
	def __init__ (self, id, name, uri, created_by, modified_by):
		self.id = id
		self.name = name
		self.uri = uri
		self.created_by = created_by
		self.modified_by = modified_by
		
	def create (self, dbm):
		query = '''INSERT INTO 'Addresses'
					('id', 'name', 'uri', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?);'''
					
		dbm.execute_d(query, (self.id, self.name, self.uri, self.created_by.id, self.modified_by.id))
		
	def update (self, dbm):
		query = '''UPDATE Addresses
					SET id=?, name=?, uri=?, created_by=?, modified_by=?
					WHERE id=?;'''
					
		dbm.execute_d(query, (self.id, self.name, self.uri, self.created_by.id, self.modified_by.id, self.id))
		
	def delete (self, dbm):
		query = '''DELETE FROM Addresses
					WHERE id="'''+self.id+'''";'''
		
		dbm.execute(query)
		
	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		name = kwargs.get('name', None)
		uri = kwargs.get('uri', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)
		
		query = "SELECT Addresses.id, Addresses.name, Addresses.uri, Addresses.created_by, Addresses.modified_by FROM 'Addresses' WHERE "
		if id != None or name != None or uri != None or created_by != None or modified_by != None:
			if id != None:
				query += 'Addresses.id="' + id + '" AND '
			if name != None:
				query += 'Addresses.name="' + name + '" AND '
			if uri != None:
				query += 'Addresses.uri="' + uri + '" AND '
			if created_by != None:
				query += 'Addresses.created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'Addresses.modified_by="' + modified_by + '";'
				
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'
				
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					self.id = result[0][0]
					self.name = result[0][1]
					self.uri = result[0][2]
					created_by = result[0][3]
					cb = accounts.NoneAccount()
					if cb.retrieve(dbm, id=created_by):
						self.created_by = cb
					else:
						self.created_by = accounts.NoneAccount()
					modified_by = result[0][4]
					mb = accounts.NoneAccount()
					if mb.retrieve(dbm, id=modified_by):
						self.modified_by = mb
					else:
						self.modified_by = accounts.NoneAccount()
					
					return True
					
		return False
	
	def is_empty (self):
		if (self.id == None and self.name == None and self.uri == None and self.created_by == None and self.modified_by == None):
			return True
		return False
		
	def debug (self):
		obj = 	{
					'id': self.id, 
					'name': self.name,
					'uri': self.uri,
					'created_by': 	{
										'id': self.created_by.id,
										'username': self.created_by.username,
										'password': self.created_by.password,
										'salt': self.created_by.salt,
										'name': self.created_by.name,
										'group': 	{
														'id': self.created_by.group.id,
														'name': self.created_by.group.name,
														'auth_key': self.created_by.group.auth_key
													}
									},
					'modified_by':	{
										'id': self.modified_by.id,
										'username': self.modified_by.username,
										'password': self.modified_by.password,
										'salt': self.modified_by.salt,
										'name': self.modified_by.name,
										'group': 	{
														'id': self.modified_by.group.id,
														'name': self.modified_by.group.name,
														'auth_key': self.modified_by.group.auth_key
													}
									}
		
				}
		print(str(obj))
		

def NoneAddress ():
	return Address(None, None, None, None, None)
	
def retrieve_all_addresses (dbm):
	query = "SELECT * FROM Addresses;"
	
	all_addresses = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[3]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[4]):
					mb = accounts.NoneAccount()
					
				a = Address(row[0], row[1], row[2], cb, mb)
				all_addresses.append(a)
				
	return all_addresses
	
def retrieve_addresses (dbm, **kwargs):
	id = kwargs.get('id', None)
	name = kwargs.get('name', None)
	uri = kwargs.get('uri', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)
	
	query = "SELECT * FROM Addresses"
	
	if id != None or name != none or uri != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'Addresses.id="' + id + '" AND '
		if name != None:
			query += 'Addresses.name="' + name + '" AND '
		if uri != None:
			query += 'Addresses.uri="' + uri + '" AND '
		if created_by != None:
			query += 'Addresses.created_by="' + created_by + '" AND '
		if modified_by != None:
			query += 'Addresses.modified_by="' + modified_by + '";'
	else:
		query += ';'
		
	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'
		
	addrs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[3]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[4]):
					mb = accounts.NoneAccount()
				a = Address(row[0], row[1], row[2], cb, mb)
				addrs.append(a)
	
	return addrs
	
	
def retrieve_addresses_custom (dbm, sql):
	query = "SELECT * FROM Addresses " + sql
	
	addrs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[3]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[4]):
					mb = accounts.NoneAccount()
				a = Address(row[0], row[1], row[2], cb, mb)
				addrs.append(a)
	
	return addrs
	