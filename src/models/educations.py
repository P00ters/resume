from addresses import Address
from orgs import Org
from skills import Skill

import addresses
import accounts
import orgs
import skills

class Education:
	def __init__ (self, id, org, degree, gpa, skill_ids, date_stop, desc_short, desc_long, created_by, modified_by):
		self.id = id
		self.org = org
		self.degree = degree
		self.gpa = gpa 
		self.skill_ids = skill_ids
		self.date_stop = date_stop 
		self.desc_short = desc_short
		self.desc_long = desc_long
		self.created_by = created_by
		self.modified_by = modified_by
		
	def create (self, dbm):
		query = '''INSERT INTO Education
					('id', 'org', 'degree', 'gpa', 'skill_ids', 'date_stop', 'desc_short', 'desc_long', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		
		dbm.execute_d(query, (self.id, self.org.id, self.degree, self.gpa, self.skill_ids, self.date_stop, self.desc_short, self.desc_long, self.created_by.id, self.modified_by.id))
		
	def update (self, dbm):
		query = '''UPDATE Education
					SET id=?, org=?, degree=?, gpa=?, skill_ids=?, date_stop=?, desc_short=?, desc_long=?, created_by=?, modified_by=?
					WHERE id=?;'''
		
		dbm.execute_d(query, (self.id, self.org.id, self.degree, self.gpa, self.skill_ids, self.date_stop, self.desc_short, self.desc_long, self.created_by.id, self.modified_by.id, self.id))
		
	def delete (self, dbm):
		query = 'DELETE FROM Education WHERE id="' + self.id + '";'
		
		dbm.execute(query)
		
	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		org = kwargs.get('org', None)
		degree = kwargs.get('degree', None)
		gpa = kwargs.get('gpa', None)
		skill_ids = kwargs.get('skill_ids', None)
		date_stop = kwargs.get('date_stop', None)
		desc_short = kwargs.get('desc_short', None)
		desc_long = kwargs.get('desc_long', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)
		
		query = '''SELECT Education.id, Orgs.id, Orgs.name, Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by, Orgs.modified_by, Addresses.id, Addresses.name, Addresses.uri, Addresses.created_by, Addresses.modified_by, Education.degree, Education.gpa, Education.skill_ids, Education.date_stop, Education.desc_short, Education.desc_long, Education.created_by, Education.modified_by
		FROM Education, Orgs, Addresses
		WHERE Education.org = Orgs.id AND Orgs.address = Addresses.id AND '''
		
		if id != None or org != None or degree != None or gpa != None or skill_ids != None or date_stop != None or desc_short != None or desc_long != None or created_by != None or modified_by != None:
			if id != None:
				query += 'Education.id="' + id + '" AND '
			if org != None:
				query += 'Educiation.org="' + org + '" AND '
			if degree != None:
				query += 'Education.degree="' + degree + '" AND '
			if gpa != None:
				query += 'Education.gpa=' + gpa + ' AND '
			if skill_ids != None:
				query += 'Education.skill_ids="' + skill_ids + '" AND '
			if date_stop != None:
				query += 'Education.date_stop="' + date_stop + '" AND '
			if desc_short != None:
				query += 'Education.desc_short="' + desc_short + '" AND '
			if desc_long != None:
				query += 'Education.desc_long="' + desc_long + '" AND '
			if created_by != None:
				query += 'Education.created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'Education.modified_by="' + modified_by + '";'
			
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'
				
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					row = result[0]
					o = orgs.NoneOrg()
					if not o.retrieve(dbm, id=row[1]):
						o = orgs.NoneOrg()
					cb = accounts.NoneAccount()
					if not cb.retrieve(dbm, id=row[21]):
						cb = accounts.NoneAccount()
					mb = accounts.NoneAccount()
					if not mb.retrieve(dbm, id=row[22]):
						mb = accounts.NoneAccount()
				
					row = result[0]
					self.id = row[0]
					self.org = o
					self.degree = row[15]
					self.gpa = row[16]
					self.skill_ids = row[17]
					self.date_stop = row[18]
					self.desc_short = row[19]
					self.desc_long = row[20]
					self.created_by = cb
					self.modified_by = mb
					return True
			
			return False
			
	def skills (self, dbm):
		query = '''SELECT id, name, exposure, soft_or_hard, reference, icon, category,
						desc_short, desc_long, created_by, modified_by
						FROM Skills
						WHERE '''
						
		s_ids = self.skill_ids.split(',')
		for i in range(len(s_ids)):
			if i != len(s_ids) - 1:
				query += 'id="' + s_ids[i] + '" OR '
			else:
				query += 'id="' + s_ids[i] + '";'
				
		result = dbm.execute(query)
		if result != None:
			result = dbm.cur.fetchall()
			if len(result) > 0:
				all_skills = []
				for row in result:
					s = Skill(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
					all_skills.append(s)
				return all_skills
		return []
		
	def is_empty (self):
		if self.id == None and self.org == None and self.degree == None and self.gpa == None and self.skill_ids == None and self.date_stop == None and self.desc_short == None and self.desc_long == None and self.created_by == None and self.modified_by == None:
			return True
		return False
		
	def degug (self):
		obj = 	{
					'id': self.id,
					'org': 	{
								'id': self.org.id,
								'name': self.org.name,
								'address':	{
												'id': self.org.address.id,
												'name': self.org.address.name,
												'uri': self.org.address.uri,
												'created_by': 	{
																	'id': self.org.address.created_by.id,
																	'username': self.org.address.created_by.username,
																	'password': self.org.address.created_by.password,
																	'salt': self.org.address.created_by.salt,
																	'name': self.org.address.created_by.name,
																	'group':	{
																					'id': self.org.address.created_by.group.id,
																					'name': self.org.address.created_by.group.name,
																					'auth_key': self.org.address.created_by.group.auth_key
																				}
																},
												'modified_by': {
																	'id': self.org.address.modified_by.id,
																	'username': self.org.address.modified_by.username,
																	'password': self.org.address.modified_by.password,
																	'salt': self.org.address.modified_by.salt,
																	'name': self.org.address.modified_by.name,
																	'group':	{
																					'id': self.org.address.modified_by.group.id,
																					'name': self.org.address.modified_by.group.name,
																					'auth_key': self.org.address.modified_by.group.auth_key
																				}
																}
											},
								'phone': self.org.phone,
								'desc_short': self.org.desc_short,
								'website': self.org.website,
								'logo': self.org.logo,
								'image_head': self.org.image_head,
								'created_by': 	{
													'id': self.org.created_by.id,
													'username': self.org.created_by.username,
													'password': self.org.created_by.password,
													'salt': self.org.created_by.salt,
													'name': self.org.created_by.name,
													'group':	{
																	'id': self.org.created_by.group.id,
																	'name': self.org.created_by.group.name,
																	'auth_key': self.org.created_by.group.auth_key
																}
												},
								'modified_by': {
													'id': self.org.modified_by.id,
													'username': self.org.modified_by.username,
													'password': self.org.modified_by.password,
													'salt': self.org.modified_by.salt,
													'name': self.org.modified_by.name,
													'group':	{
																	'id': self.org.modified_by.group.id,
																	'name': self.org.modified_by.group.name,
																	'auth_key': self.org.modified_by.group.auth_key
																}
												}
							},
						'degree': self.degree,
						'gpa': self.gpa,
						'skill_ids': self.skill_ids,
						'date_stop': self.date_stop,
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
		
		
def NoneEducation ():
	return Education(None, None, None, None, None, None, None, None, None, None)
	
def retrieve_all_educations (dbm):
	query = "SELECT * FROM Education;"
	
	all_edus = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[1]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				e = Education(row[0], o, row[2], row[3], row[4], row[5], row[6], row[7], cb, mb)
				all_edus.append(e)
				
	return all_edus
	
	
def retrieve_educations (dbm, **kwargs):
	id = kwargs.get('id', None)
	org = kwargs.get('org', None)
	degree = kwargs.get('degree', None)
	gpa = kwargs.get('gpa', None)
	skill_ids = kwargs.get('skill_ids', None)
	date_stop = kwargs.get('date_stop', None)
	desc_short = kwargs.get('desc_short', None)
	desc_long = kwargs.get('desc_long', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)
	
	query = "SELECT * FROM Education"
	
	if id != None or org != None or degree != None or gpa != None or skill_ids != None or date_stop != None or desc_short != None or desc_long != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if org != None:
			query += 'org="' + org + '" AND '
		if degree != None:
			query += 'degree="' + degree + '" AND '
		if gpa != None:
			query += 'gpa=' + gpa + ' AND '
		if skill_ids != None:
			query += 'skill_ids="' + skill_ids + '" AND '
		if date_stop != None:
			query += 'date_stop="' + date_stop + '" AND '
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
	
	es = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[1]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				e = Education(row[0], o, row[2], row[3], row[4], row[5], row[6], row[7], cb, mb)
				es.append(e)
				
	return es
	
def retrieve_educations_custom (dbm, sql):
	query = "SELECT * FROM Education " + sql
	
	es = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[1]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				e = Education(row[0], o, row[2], row[3], row[4], row[5], row[6], row[7], cb, mb)
				es.append(e)
				
	return es
	
def edus_date_sort (edu_list):
	n = len(edu_list)
	for i in range(n):
		for j in range(0, n-i-1):
			if edu_list[j].date_stop > edu_list[j+1].date_stop:
				edu_list[j], edu_list[j+1] = edu_list[j+1], edu_list[j]
	