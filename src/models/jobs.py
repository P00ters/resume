import accounts
import addresses
import orgs
import skills

from orgs import Org
from accounts import Account
from addresses import Address
from skills import Skill

class Job:
	def __init__ (self, id, title, present, date_start, date_stop, desc_short, desc_long, skill_ids, org, created_by, modified_by):
		self.id = id
		self.title = title
		self.present = present
		self.date_start = date_start
		self.date_stop = date_stop
		self.desc_short = desc_short
		self.desc_long = desc_long
		self.skill_ids = skill_ids
		self.org = org
		self.created_by = created_by
		self.modified_by = modified_by
		
	def create (self, dbm):
		query = '''INSERT INTO Jobs
					('id', 'title', 'present', 'date_start', 'date_stop', 'desc_short', 'desc_long', 'skill_ids', 'org', 'created_by', 'modified_by')
					VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		
		
		dbm.execute_d(query, (self.id, self.title, self.present, self.date_start, self.date_stop, self.desc_short, self.desc_long, self.skill_ids, self.org.id, self.created_by.id, self.modified_by.id))
		
	def update (self, dbm):
		query = '''UPDATE Jobs
					SET id=?, title=?, present=?, date_start=?, date_stop=?, desc_short=?, desc_long=?, skill_ids=?, org=?, created_by=?, modified_by=?
					WHERE id=?;'''
					
		dbm.execute_d(query, (self.id, self.title, self.present, self.date_start, self.date_stop, self.desc_short, self.desc_long, self.skill_ids, self.org.id, self.created_by.id, self.modified_by.id, self.id))
		
	def delete (self, dbm):
		query = 'DELETE FROM Jobs WHERE id="' + self.id + '";'
		
		dbm.execute(query)
		
	def retrieve (self, dbm, **kwargs):
		id = kwargs.get('id', None)
		title = kwargs.get('title', None)
		present = kwargs.get('present', None)
		date_start = kwargs.get('date_start', None)
		date_stop = kwargs.get('date_stop', None)
		desc_short = kwargs.get('desc_short', None)
		desc_long = kwargs.get('desc_long', None)
		skill_ids = kwargs.get('skill_ids', None)
		org = kwargs.get('org', None)
		created_by = kwargs.get('created_by', None)
		modified_by = kwargs.get('modified_by', None)
		
		query = '''SELECT Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Jobs.created_by, Jobs.modified_by, Orgs.id, Orgs.name, Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by, Orgs.modified_by, Addresses.id, Addresses.name, Addresses.uri, Addresses.created_by, Addresses.modified_by
		FROM Jobs, Orgs, Addresses
		WHERE Jobs.org = Orgs.id AND Orgs.address = Addresses.id AND '''
		if id != None or title != None or present != None or date_start != None or date_stop != None or desc_short != None or desc_long != None or skill_ids != None or org != None or created_by != None or modified_by != None:
			if id != None:
				query += 'Jobs.id="' + id + '" AND '
			if title != None:
				query += 'Jobs.title="' + title + '" AND '
			if present != None:
				query += 'Jobs.present=' + present + '" AND '
			if date_start != None:
				query += 'Jobs.date_start="' + date_start + '" AND '
			if date_stop != None: 
				query += 'Jobs.date_stop="' + date_stop + '" AND '
			if desc_short != None:
				query += 'Jobs.desc_short="' + desc_short + '" AND '
			if desc_long != None:
				query += 'Jobs.desc_long="' + desc_long + '" AND '
			if skill_ids != None:
				query += 'Jobs.skill_ids="' + skill_ids + '" AND '
			if org != None:
				query += 'Orgs.id="' + org + '" AND '
			if created_by != None:
				query += 'Jobs.created_by="' + created_by + '" AND '
			if modified_by != None:
				query += 'Jobs.modified_by="' + modified_by + '";'
		
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'
				
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
				if len(result) == 1:
					cb =  accounts.NoneAccount()
					if not cb.retrieve(dbm, id=result[0][8]):
						cb = accounts.NoneAccount()
					mb = accounts.NoneAccount()
					if not mb.retrieve(dbm, id=result[0][9]):
						mb = accounts.NoneAccount()
					o = orgs.NoneOrg()
					if not o.retrieve(dbm, id=result[0][10]):
						o = orgs.NoneOrg()
				
					self.id = result[0][0]
					self.title = result[0][1]
					self.present = result[0][2]
					self.date_start = result[0][3]
					self.date_stop = result[0][4]
					self.desc_short = result[0][5]
					self.desc_long = result[0][6]
					self.skill_ids = result[0][7]
					self.created_by = cb
					self.modified_by = mb
					self.org = o
					
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
		if self.id == None and self.title == None and self.present == None and self.date_start == None and self.date_stop == None and self.desc_short == None and self.desc_long == None and self.skill_ids == None and self.created_by == None and self.modified_by == None and self.org == None:
			return True
		return False
		
	def debug (self):
		obj =	{
					'id': self.id,
					'title': self.title,
					'present': self.present,
					'date_start': self.date_start,
					'date_stop': self.date_stop,
					'desc_short': self.desc_short,
					'desc_long': self.desc_long,
					'skill_ids': self.skill_ids,
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
									},
					'org': {
								'id': self.org.id,
								'name': self.org.name,
								'address': {
												'id': self.org.address.id,
												'name': self.org.address.name,
												'uri': self.org.address.uri,
												'created_by': 	{
																	'id': self.org.address.created_by.id,
																	'username': self.org.address.created_by.username,
																	'password': self.org.address.created_by.password,
																	'salt': self.org.address.created_by.salt,
																	'name': self.org.address.created_by.name,
																	'group': 	{
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
																	'group': 	{
																					'id': self.org.address.modified_by.group.id,
																					'name': self.org.address.modified_by.group.name,
																					'auth_key': self.org.address.modified_by.group.auth_key
																				}
																}
											},
								'phone': self.org.phone,
								'desc_short': self.org.desc_short,
								'website': self.org.website,
								'created_by': 	{
													'id': self.org.created_by.id,
													'username': self.org.created_by.username,
													'password': self.org.created_by.password,
													'salt': self.org.created_by.salt,
													'name': self.org.created_by.name,
													'group': 	{
																	'id': self.org.created_by.group.id,
																	'name': self.org.created_by.group.name,
																	'auth_key': self.org.created_by.group.auth_key
																}
												},
								'modified_by': 	{
													'id': self.org.modified_by.id,
													'username': self.org.modified_by.username,
													'password': self.org.modified_by.password,
													'salt': self.org.modified_by.salt,
													'name': self.org.modified_by.name,
													'group': 	{
																	'id': self.org.modified_by.group.id,
																	'name': self.org.modified_by.group.name,
																	'auth_key': self.org.modified_by.group.auth_key
																}
												}
							}
				}
		print(str(obj))
		
def NoneJob ():
	return Job(None, None, None, None, None, None, None, None, None, None, None)
	
def retrieve_all_jobs (dbm):
	query = "SELECT Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Jobs.created_by, Jobs.modified_by, Jobs.org FROM Jobs;"
	
	all_jobs = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[10]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[8]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[9]):
					mb = accounts.NoneAccount()
					
				j = Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], o, cb, mb)
				all_jobs.append(j)
				
	return all_jobs
	
	
def retrieve_jobs (dbm, **kwargs):
	id = kwargs.get('id', None)
	title = kwargs.get('title', None)
	present = kwargs.get('present', None)
	date_start = kwargs.get('date_start', None)
	date_stop = kwargs.get('date_stop', None)
	desc_short = kwargs.get('desc_short', None)
	desc_long = kwargs.get('desc_long', None)
	skill_ids = kwargs.get('skill_ids', None)
	org = kwargs.get('org', None)
	created_by = kwargs.get('created_by', None)
	modified_by = kwargs.get('modified_by', None)
	
	query = "SELECT * FROM Jobs"
	
	if id != None or title != None or present != None or date_start != None or date_stop != None or desc_short != None or desc_long != None or skill_ids != None or org != None or created_by != None or modified_by != None:
		query += ' WHERE '
		if id != None:
			query += 'id="' + id + '" AND '
		if title != None:
			query += 'title="' + title + '" AND '
		if present != None:
			query += 'present=' + present + ' AND '
		if date_start != None:
			query += 'date_start="' + date_start + '" AND '
		if date_stop != None:
			query += 'date_stop="' + date_stop + '" AND '
		if desc_short != None:
			query += 'desc_short="' + desc_short + '" AND '
		if desc_long != None:
			query += 'desc_long="' + desc_long + '" AND '
		if skill_ids != None:
			query += 'skill_ids="' + skill_ids + '" AND '
		if org != None: 
			query += 'org="' + org + '" AND '
		if created_by != None:
			query += 'created_by="' + created_by + '" AND '
		if modified_by != None:
			query += 'modified_by="' + modified_by + '";'
	else:
		query += ';'
		
	if query[-4:] == 'AND ':
		query = query[:-4]
		query += ';'
		
	js = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[8]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()
					
				j = Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], o, cb, mb)
				js.append(j)
	
	return js
	
def retrieve_jobs_custom (dbm, sql):
	query = "SELECT * FROM Jobs " + sql
	
	js = []
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if len(result) > 0:
			for row in result:
				o = orgs.NoneOrg()
				if not o.retrieve(dbm, id=row[8]):
					o = orgs.NoneOrg()
				cb = accounts.NoneAccount()
				if not cb.retrieve(dbm, id=row[9]):
					cb = accounts.NoneAccount()
				mb = accounts.NoneAccount()
				if not mb.retrieve(dbm, id=row[10]):
					mb = accounts.NoneAccount()
					
				j = Job(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], o, cb, mb)
				js.append(j)
	
	return js
	
	
def jobs_date_sort (job_list):
	n = len(job_list)
	for i in range(n):
		for j in range(0, n-i-1):
			if job_list[j].date_start > job_list[j+1].date_start:
				job_list[j], job_list[j+1] = job_list[j+1], job_list[j]