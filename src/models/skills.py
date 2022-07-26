from accounts import Account
import accounts

class Skill:
	def __init__ (self, id, name, exposure, soft_or_hard, reference, icon, category, desc_short, desc_long, created_by, modified_by):
		self.id = id
		self.name = name
		self.exposure = exposure
		self.soft_or_hard = soft_or_hard
		self.reference = reference
		self.icon = icon
		self.category = category
		self.desc_short = desc_short
		self.desc_long = desc_long
		self.created_by = created_by
		self.modified_by = modified_by

	def create (self, dbm):
		query = '''INSERT INTO Skills
					('id', 'name', 'exposure', 'soft_or_hard', 'reference', 'icon', 'category', 'desc_short', 'desc_long', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		dbm.execute_d(query, (self.id, self.name, self.exposure, self.soft_or_hard, self.reference, self.icon, self.category, self.desc_short, self.desc_long, self.created_by.id, self.modified_by.id))

	def update (self, dbm):
		query = '''UPDATE Skills
					SET id=?, name=?, exposure=?, soft_or_hard=?, reference=?, icon=?, category=?, desc_short=?,
						desc_long=?, created_by=?, modified_by=?
					WHERE id=?;'''

		dbm.execute_d(query, (self.id, self.name, self.exposure, self.soft_or_hard, self.reference, self.icon, self.category, self.desc_short, self.desc_long, self.created_by.id, self.modified_by.id, self.id))

	def delete (self, dbm):
		query = 'DELETE FROM Skills WHERE id="' + self.id + '";'

		dbm.execute(query)

	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		name = kwargs.get('name', None)
		exposure = kwargs.get('exposure', None)
		soft_or_hard = kwargs.get('soft_or_hard', None)
		reference = kwargs.get('reference', None)
		icon = kwargs.get('icon', None)
		category = kwargs.get('category', None)
		desc_short = kwargs.get('desc_short', None)
		desc_long = kwargs.get('desc_long', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)

		query = "SELECT * FROM 'Skills' WHERE "
		if id != None or name != None or exposure != None or soft_or_hard != None or reference != None or category != None or desc_short != None or desc_long != None or created_by != None or modified_by != None:
			if id != None:
				query += 'id="' + id + '" AND '
			if name != None:
				query += 'name="' + name + '" AND '
			if exposure != None:
				query += 'exposure=' + exposure + ' AND '
			if soft_or_hard != None:
				query += 'soft_or_hard=' + soft_or_hard + ' AND '
			if reference != None:
				query += 'reference="' + reference + '" AND '
			if icon != None:
				query += 'icon="' + icon + '" AND '
			if category != None:
				query += 'category="' + category + '" AND '
			if desc_short != None:
				query += 'desc_short="' + desc_short + '" AND '
			if desc_long != None:
				query += 'desc_long="' + desc_long + '" AND '
			if created_by != None:
				query += 'created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'modified_by="' + modified_by + '";'

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					cb = accounts.NoneAccount()
					if not cb.retrieve(dbm, id=result[0][9]):
						cb = accounts.NoneAccount()
					mb = accounts.NoneAccount()
					if not mb.retrieve(dbm, id=result[0][10]):
						mb = accounts.NoneAccount()

					self.id = result[0][0]
					self.name = result[0][1]
					self.exposure = result[0][2]
					self.soft_or_hard = result[0][3]
					self.reference = result[0][4]
					self.icon = result[0][5]
					self.category = result[0][6]
					self.desc_short = result[0][7]
					self.desc_long = result [0][8]
					self.created_by = cb
					self.modified_by = mb
					return True

		return False

	def is_empty (self):
		if self.id == None and self.name == None and self.exposure == None and self.soft_or_hard == None and self.icon == None and self.category == None and self.desc_short == None and self.desc_long == None and self.created_by == None and self.modified_by == None:
			return True
		return False

	def dict (self):
		obj = 	{
					'id': self.id,
					'name': self.name,
					'exposure': self.exposure,
					'soft_or_hard': self.soft_or_hard,
					'reference': self.reference,
					'category': self.category,
					'desc_short': self.desc_short,
					'desc_long': self.desc_long,
					'icon': "data:image/png;base64," + self.icon.decode('utf-8'),
					'created_by': 	{
										'id': self.created_by.id,
										'username': self.created_by.username,
										'password': 'redacted',
										'salt': 'redacted',
										'name': self.created_by.name,
										'group':	{
														'id': self.created_by.group.id,
														'name': self.created_by.group.name,
														'auth_key': 'redacted'
													}
									},
					'modified_by': 	{
										'id': self.modified_by.id,
										'username': self.modified_by.username,
										'password': 'redacted',
										'salt': 'redacted',
										'name': self.modified_by.name,
										'group':	{
														'id': self.modified_by.group.id,
														'name': self.modified_by.group.name,
														'auth_key': 'redacted'
													}
									}
				}
		return obj

	def debug (self):
		obj = 	{
					'id': self.id,
					'name': self.name,
					'exposure': self.exposure,
					'soft_or_hard': self.soft_or_hard,
					'reference': self.reference,
					'icon': self.icon,
					'category': self.category,
					'desc_short': self.desc_short,
					'desc_long': self.desc_long,
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


def NoneSkill ():
	return Skill(None, None, None, None, None, None, None, None, None, None, None)

def retrieve_all_skills (dbm):
	query = "SELECT * FROM Skills;"

	all_skills = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()

				s = Skill(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], cb, mb)
				all_skills.append(s)

	return all_skills


def retrieve_skills (dbm, **kwargs):
	id = kwargs.get('id', None)
	name = kwargs.get('name', None)
	exposure = kwargs.get('exposure', None)
	soft_or_hard = kwargs.get('soft_or_hard', None)
	reference = kwargs.get('reference', None)
	icon = kwargs.get('icon', None)
	category = kwargs.get('category', None)
	desc_short = kwargs.get('desc_short', None)
	desc_long = kwargs.get('desc_long', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)

	query = "SELECT * FROM Skills"

	if id != None or name != None or exposure != None or soft_or_hard != None or reference != None or icon != None or category != None or desc_short != None or desc_long != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if name != None:
			query += 'name="' + name + '" AND '
		if exposure != None:
			query += 'exposure=' + exposure + ' AND '
		if soft_or_hard != None:
			query += 'soft_or_hard=' + soft_or_hard + ' AND '
		if reference != None:
			query += 'reference="' + reference + ' AND '
		if icon != None:
			query += 'icon="' + icon + '" AND '
		if category != None:
			query += 'category="' + category + '" AND '
		if desc_short != None:
			query += 'desc_short="' + desc_short + '" AND '
		if desc_long != None:
			query += 'desc_long="' + desc_long + '" AND '
		if created_by != None:
			query += 'created_by="' + created_by + '" AND '
		if modified_by != None:
			query += 'modified_by="' + modified_by + '";'
	else:
		query += ';'

	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'

	ss = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()

				s = Skill(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], cb, mb)
				ss.append(s)

	return ss

def retrieve_skills_custom (dbm, sql):
	query = "SELECT * FROM Skills " + sql

	ss = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()

				s = Skill(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], cb, mb)
				ss.append(s)

	return ss

def retrieve_skills_fcustom (dbm, query):
	ss = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()

				s = Skill(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], cb, mb)
				ss.append(s)

	return ss
