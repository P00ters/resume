from addresses import Address
from accounts import Account

import accounts
import addresses

class Contact:
	def __init__ (self, id, name, address, phone1, phone2, email, objective, created_by, modified_by):
		self.id = id
		self.name = name
		self.address = address
		self.phone1 = phone1
		self.phone2 = phone2
		self.email = email 
		self.objective = objective
		self.created_by = created_by
		self.modified_by = modified_by
		
	def create (self, dbm):
		query = '''INSERT INTO Contact
					('id', 'name', 'address', 'phone1', 'phone2', 'email', 'objective', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		
		dbm.execute_d(query, (self.id, self.name, self.address.id, self.phone1, self.phone2, self.email, self.objective, self.created_by.id, self.modified_by.id))
		
	def update (self, dbm):
		query = '''UPDATE Contact
					SET id=?, name=?, address=?, phone1=?, phone2=?, email=?, objective=?, created_by=?, modified_by=?)
					WHERE id=?;'''
					
		dbm.execute_d(query, (self.id, self.name, self.address, self.phone1, self.phone2, self.email, self.objective, self.created_by.id, self.modified_by.id, self.id))
		
	def delete (self, dbm):
		query = 'DELETE FROM Contact WHERE id="' + self.id + '";'
		
		dbm.execute(query)
		
	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		name = kwargs.get('name', None)
		address = kwargs.get('address', None)
		phone1 = kwargs.get('phone1', None)
		phone2 = kwargs.get('phone2', None)
		email = kwargs.get('email', None)
		objective = kwargs.get('objective', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)
		
		query = '''SELECT Contact.id, Contact.name, Addresses.id, Addresses.name, Addresses.uri, Addresses.created_by, Addresses.modified_by, Contact.phone1, Contact.phone2, Contact.email, Contact.objective, Contact.created_by, Contact.modified_by
		FROM Contact, Addresses
		WHERE Contact.address = Addresses.id AND '''
		if id != None or name != None or address != None or phone1 != None or phone2 != None or email != None or objective != None or created_by != None or modified_by != None:
			if id != None:
				query += 'Contact.id="' + id + '" AND '
			if name != None:
				query += 'Contact.name="' + name + '" AND '
			if address != None:
				query += 'Contact.address="' + address + '" AND '
			if phone1 != None:
				query += 'Contact.phone1="' + phone1 + '" AND '
			if phone2 != None:
				query += 'Contact.phone2="' + phone2 + '" AND '
			if email != None:
				query += 'Contact.email="' + email + '" AND '
			if objective != None:
				query += 'Contact.objective="' + objective + '" AND '
			if created_by != None:
				query += 'Contact.created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'Contact.modified_by="' + modified_by + '";'
				
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'
				
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					cb = accounts.NoneAccount()
					if not cb.retrieve(dbm, id=result[0][11]):
						cb = accounts.NoneAccount()
					mb = accounts.NoneAccount()
					if not mb.retrieve(dbm, id=result[0][12]):
						mb = accounts.NoneAccount()
					addr = addresses.NoneAddress()
					if not addr.retrieve(dbm, id=result[0][2]):
						addr = addresses.NoneAddress()
				
					self.id = result[0][0]
					self.name = result[0][1]
					self.address = addr
					self.phone1 = result[0][7]
					self.phone2 = result[0][8]
					self.email = result[0][9]
					self.objective = result[0][10]
					self.created_by = cb
					self.modified_by = mb
					return True
		
		return False
		
		def is_empty (self):
			if self.id == None and self.name == None and self.address == None and self.phone1 == None and self.phone2 == None and self.email == None and self.objective == None and self.created_by == None and self.modified_by == None:
				return True
			return False
		
		def debug (self):
			obj = 	{
						'id': self.id,
						'name': self.name,
						'address': {
										'id': self.address.id,
										'name': self.address.name,
										'uri': self.address.uri,
										'created_by': 	{
															'id': self.address.created_by.id,
															'username': self.address.created_by.username,
															'password': self.address.created_by.password,
															'salt': self.address.created_by.salt,
															'name': self.address.created_by.name,
															'group':	{
																			'id': self.address.created_by.group.id,
																			'name': self.address.created_by.group.name,
																			'auth_key': self.address.created_by.group.auth_key
																		}
														},
										'modified_by': 	{
															'id': self.address.modified_by.id,
															'username': self.address.modified_by.username,
															'password': self.address.modified_by.password,
															'salt': self.address.modified_by.salt,
															'name': self.address.modified_by.name,
															'group':	{
																			'id': self.address.modified_by.group.id,
																			'name': self.address.modified_by.group.name,
																			'auth_key': self.address.modified_by.group.auth_key
																		}
														}
									},
						'phone1': self.phone1,
						'phone2': self.phone2,
						'email': self.email,
						'objective': self.objective,
						'created_by': 	{
											'id': self.created_by.id,
											'username': self.created_by.username,
											'password': self.created_by.password,
											'salt': self.created_by.salt,
											'name': self.created_by.name,
											'group':	{
															'id': self.created_by.group.id,
															'name': self.created_by.group.name,
															'auth_key': self.created_by.group.auth_key
														}
										},
						'modified_by': 	{
											'id': self.modified_by.id,
											'username': self.modified_by.username,
											'password': self.modified_by.password,
											'salt': self.modified_by.salt,
											'name': self.modified_by.name,
											'group':	{
															'id': self.modified_by.group.id,
															'name': self.modified_by.group.name,
															'auth_key': self.modified_by.group.auth_key
														}
										}
					}
			print(str(obj))
			
def retrieve_all_contacts (dbm):
	query = "SELECT * FROM Contacts;"
	
	all_contacts = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[7]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[8]):
					mb = accounts.NoneAccount()
					
				c = Contact(row[0], row[1], addr, row[3], row[4], row[5], row[6], cb, mb)
				all_contacts.append(c)
	
	return all_contacts
	

def retrieve_contacts (dbm, **kwargs):
	id = kwargs.get('id', None)
	name = kwargs.get('name', None)
	address = kwargs.get('address', None)
	phone1 = kwargs.get('phone1', None)
	phone2 = kwargs.get('phone2', None)
	email = kwargs.get('email', None)
	objective = kwargs.get('objective', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)
	
	query = "SELECT * FROM Contact"
	
	if id != None or name != None or address != None or phone1 != None or phone2 != None or email != None or objective != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if name != None:
			query += 'name="' + name + '" AND '
		if address != None:
			query += 'address="' + address + '" AND '
		if phone1 != None:
			query += 'phone1="' + phone1 + '" AND '
		if phone2 != None:
			query += 'phone2="' + phone2 + '" AND '
		if email != None:
			query += 'email="' + email + '" AND '
		if objective != None:
			query += 'objective="' + objective + '" AND '
		if created_by != None:
			query += 'created_by="' + created_by + '" AND '
		if modified_by != None:
			query += 'modified_by="' + modified_by + '";'
	else:
		query += ';'
		
	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'
		
	cs = []
	
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[7]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[8]):
					mb = accounts.NoneAccount()
					
				c = Contact(row[0], row[1], addr, row[3], row[4], row[5], row[6], cb, mb)
				cs.append(c)
				
	return cs
	
def retrieve_contacts_custom (dbm, sql):
	query += "SELECT * FROM Contact " + sql
	
	cs = []
	
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[7]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[8]):
					mb = accounts.NoneAccount()
					
				c = Contact(row[0], row[1], addr, row[3], row[4], row[5], row[6], cb, mb)
				cs.append(c)
				
	return cs
	