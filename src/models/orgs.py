import addresses
import accounts
from accounts import Account
from addresses import Address

class Org:
	def __init__ (self, id, name, address, phone, desc_short, website, logo, image_head, created_by, modified_by):
		self.id = id
		self.name = name
		self.address = address
		self.phone = phone
		self.desc_short = desc_short
		self.website = website
		self.logo = logo
		self.image_head = image_head
		self.created_by = created_by
		self.modified_by = modified_by
		
	def create( self, dbm):
		query = '''INSERT INTO Orgs
					('id', 'name', 'address', 'phone', 'desc_short', 'website', 'logo', 'image_head', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		
		dbm.execute_d(query, (self.id, self.name, self.address.id, self.phone, self.desc_short, self.website, self.logo, self.image_head, self.created_by.id, self.modified_by.id))
		
	def update (self, dbm):
		query = '''UPDATE Orgs
					SET id=?, name=?, address=?, phone=?, desc_short=?, website=?, logo=?, image_head=?, created_by=?, modified_by=?
					WHERE id=?;'''
					
		dbm.execute_d(query, (self.id, self.name, self.address.id, self.phone, self.desc_short, self.website, self.logo, self.image_head, self.created_by.id, self.modified_by.id, self.id))
		
	def delete (self, dbm):
		query = 'DELETE FROM Orgs WHERE id="' + self.id + '";'
		
		dbm.execute(query)
		
	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		name = kwargs.get('name', None)
		address = kwargs.get('address', None)
		phone = kwargs.get('phone', None)
		desc_short = kwargs.get('desc_short', None)
		website = kwargs.get('website', None)
		logo = kwargs.get('logo', None)
		image_head = kwargs.get('image_head', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)
		
		query = "SELECT Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Addresses.created_by, Addresses.modified_by, Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by, Orgs.modified_by FROM Orgs, Addresses WHERE Orgs.address=Addresses.id AND "
		if id != None or name != None or address != None or phone != None or desc_short != None or website != None or logo != None or image_head != None or created_by != None or modified_by != None:
			if id != None:
				query += 'Orgs.id="' + id + '" AND '
			if name != None:
				query += 'Orgs.name="' + name + '" AND '
			if address != None:
				query += 'Orgs.address="' + address + '" AND '
			if phone != None:
				query += 'Orgs.phone="' + phone + '" AND '
			if desc_short != None:
				query += 'Orgs.desc_short="' + desc_short + '" AND '
			if website != None:
				query += 'Orgs.website="' + website + '" AND '
			if logo != None:
				query += 'Orgs.logo="' + logo + '" AND '
			if image_head != None:
				query += 'Orgs.image_head="' + image_head + '" AND '
			if created_by != None:
				query += 'Orgs.created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'Orgs.modified_by="' + modified_by + '";'
				
				
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'
				
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					self.id = result[0][0]
					self.name = result[0][1]
					adr = addresses.NoneAddress()
					if not adr.retrieve(dbm, id=result[0][2]):
						adr = addresses.NoneAddress()
					self.phone = result[0][7]
					self.desc_short = result[0][8]
					self.website = result[0][9]
					self.logo = result[0][10]
					self.image_head = result[0][11]
					cb = accounts.NoneAccount()
					if not cb.retrieve(dbm, id=result[0][12]):
						cb = accounts.NoneAccount()
					mb = accounts.NoneAccount()
					if not mb.retrieve(dbm, id=result[0][13]):
						mb = accounts.NoneAccount()
					
					
					self.created_by = cb
					self.modified_by = mb
					self.address = adr
					return True
					
			return False
			
	def is_empty (self):
		if self.id == None and self.name == None and self.address == None and self.phone == None and self.desc_short == None and self.website == None and self.logo == None and self.image_head == None and self.created_by == None and self.modified_by == None:
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
											'group': 	{
															'id': self.address.created_by.group.id,
															'name': self.address.created_by.group.name,
															'auth_key': self.address.created_by.group.auth_key
														}
										},
						'modified_by': {
											'id': self.address.modified_by.id,
											'username': self.address.modified_by.username,
											'password': self.address.modified_by.password,
											'salt': self.address.modified_by.salt,
											'name': self.address.modified_by.name, 
											'group': 	{
															'id': self.address.modified_by.group.id,
															'name': self.address.modified_by.group.name,
															'auth_key': self.address.modified_by.group.auth_key
														}
										}
					},
					'phone': self.phone,
					'desc_short': self.desc_short,
					'website': self.website,
					'logo': self.logo,
					'image_head': self.image_head,
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
			
			
def NoneOrg ():
	return Org(None, None, None, None, None, None, None, None, None, None)
	
def retrieve_all_orgs (dbm):
	query = '''SELECT 	Orgs.id, Orgs.name, 
						Addresses.id,
						Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by,
						Orgs.modified_by
				FROM	Orgs, Addresses
				WHERE	Orgs.address=Addresses.id;'''
				
	all_orgs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				o = Org(row[0], row[1], addr, row[3], row[4], row[5], row[6], row[7], cb, mb)
				all_orgs.append(o)
					
	return all_orgs
	
def retrieve_orgs (dbm, **kwargs):
	id = kwargs.get('id', None)
	name = kwargs.get('name', None)
	address = kwargs.get('address', None)
	phone = kwargs.get('phone', None)
	desc_short = kwargs.get('desc_short', None)
	website = kwargs.get('website', None)
	logo = kwargs.get('logo', None)
	image_head = kwargs.get('image_head', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)
	
	query = "SELECT * FROM Orgs"
	
	if id != None or name != None or address != None or phone != None or desc_short != None or website != None or logo != None or image_head != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if name != None:
			query += 'name="' + name + '" AND '
		if address != None:
			query += 'address="' + address + '" AND '
		if phone != None:
			query += 'phone="' + phone + '" AND '
		if desc_short != None:
			query += 'desc_short="' + desc_short + '" AND '
		if website != None:
			query += 'website="' + website + '" AND '
		if logo != None:
			query += 'logo="' + logo + '" AND '
		if image_head != None:
			query += 'image_head="' + image_head + '" AND '
		if created_by != None:
			query += 'created_by="' + created_by + '" AND '
		if modified_by != None:
			query += 'modified_by="' + modified_by + '";'
	else:
		query += ';'
		
	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'	
		
	os = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				o = Org(row[0], row[1], addr, row[3], row[4], row[5], row[6], row[7], cb, mb)
				os.append(o)
				
	return os
	

def retrieve_groups_custom (dbm, sql):
	query = "SELECT * FROM Orgs " + sql
	
	os = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				addr = addresses.NoneAddress()
				if not addr.retrieve(dbm, id=row[2]):
					addr = addresses.NoneAddress()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				o = Org(row[0], row[1], addr, row[2], row[3], row[4], row[5], row[6], row[7], cb, mb)
				os.append(o)

	return os
				
				
		