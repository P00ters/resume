import random
import sys
sys.path.append('../')
sys.path.append('../models')

from contacts import Contact, retrieve_all_contacts
from dbm import DBM
from educations import Education, retrieve_all_educations, edus_date_sort
from jobs import Job, retrieve_all_jobs, jobs_date_sort
from orgs import Org, retrieve_all_orgs
from skills import retrieve_skills_custom, NoneSkill, Skill, retrieve_skills, retrieve_all_skills

class MasterController:
	def __init__ (self, dbm):
		self.dbm = dbm
		self.auth_keys = self.get_keys()
		
	def get_keys(self):
		query = '''SELECT * FROM Groups;'''
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			keys = {}
			for row in result:
				keys[row[1]] = row[2]
			return keys
		else:
			exit('Unable to load authorizations table.')
			
	
	def edus_byid_query (self, id):
		all_edus = retrieve_all_educations(self.dbm)
		edus_date_sort(all_edus)
		
		es = []
		for i in range(len(all_edus)):
			if all_edus[i].id == id:
				es.append(all_edus[i])
				if i != len(all_edus) - 1:
					es.append(all_edus[i+1])
				else:
					es.append(all_edus[0])
				if i != 0:
					es.append(all_edus[i-1])
				else:
					es.append(all_edus[len(all_edus) - 1])
					
		return es
	
	def edus_general_query (self):
		all_edus = retrieve_all_educations(self.dbm)
		if len(all_edus) == 0:
			return None
		else:
			all_edus = all_edus[::-1]
			return all_edus[0].id
			
	def home_contact_query (self):
		all_contacts = retrieve_all_contacts(self.dbm)
		if len(all_contacts) == 0:
			return None
		else:
			all_contacts = all_contacts[::-1]
			return all_contacts[0]
			
	def home_edu_query (self):
		all_edus = retrieve_all_educations(self.dbm)
		edus_date_sort(all_edus)
		
		if len(all_edus) > 3:
			all_edus = all_edus[-3:]
		return all_edus[::-1]
		
	def home_jobs_query (self):
		all_jobs = retrieve_all_jobs(self.dbm)
		jobs_date_sort(all_jobs)
		
		if len(all_jobs) > 4:
			all_jobs = all_jobs[-4:]
		return all_jobs[::-1]	
	
	def jobs_byid_query (self, id):
		all_jobs = retrieve_all_jobs(self.dbm)
		jobs_date_sort(all_jobs)
		
		js = []
		for i in range(len(all_jobs)):
			if all_jobs[i].id == id:
				js.append(all_jobs[i])
				if i != len(all_jobs) - 1:
					js.append(all_jobs[i+1])
				else:
					js.append(all_jobs[0])
				if i != 0:
					js.append(all_jobs[i-1])
				else:
					js.append(all_jobs[len(all_jobs) - 1])
					
		return js
	
	def jobs_general_query (self):
		all_jobs = retrieve_all_jobs(self.dbm)
		if len(all_jobs) == 0:
			return None
		else:
			all_jobs = all_jobs[::-1]
			return all_jobs[0].id
			
	def orgs_byid_query (self, id):
		all_orgs = retrieve_all_orgs(self.dbm)
		these_orgs = []
		for i in range(len(all_orgs)):
			if all_orgs[i].id == id:
				these_orgs.append(all_orgs[i])
				if i != len(all_orgs) - 1:
					these_orgs.append(all_orgs[i+1])
				else:
					these_orgs.append(all_orgs[0])
				if i == 0:
					these_orgs.append(all_orgs[len(all_orgs) - 1])
				else:
					these_orgs.append(all_orgs[i-1])
	
		return these_orgs
		
	def orgs_for_add_query (self):
		all_orgs = retrieve_all_orgs(self.dbm)
		if len(all_orgs) == 0:
			return []
		else:
			return all_orgs
		
	def orgs_general_query (self):
		all_orgs = retrieve_all_orgs(self.dbm)
		if len(all_orgs) == 0:
			return None
		else:
			all_orgs = all_orgs[::-1]
			return all_orgs[0].id
			
	def skills_byid_query (self, sid):
		this_skill = []
		similar = []
		appears_in = [[], []]
		
		s = NoneSkill()
		if not s.retrieve(self.dbm, id=sid):
			# return 404
			return []
		else:
			this_skill.append(s)
		
		similar = retrieve_skills(self.dbm, category=s.category)
		for sim in similar:
			if sim.id == sid:
				similar.remove(sim)
		random.shuffle(similar)
		similar = similar[:6]
		all_jobs = retrieve_all_jobs(self.dbm)
		for j in all_jobs:
			split = j.skill_ids.split(',')
			if sid in split:
				appears_in[0].append(j)
		all_edus = retrieve_all_educations(self.dbm)
		for e in all_edus:
			split = e.skill_ids.split(',')
			if sid in split:
				appears_in[1].append(e)
				

		this_skill.append(similar)
		this_skill.append(appears_in)
		return this_skill
		
	def skills_for_add_query (self):
		all_skills = retrieve_all_skills(self.dbm)
		if len(all_skills) == 0:
			return []
		else:
			return all_skills
		
	def skills_general_query (self):
		query = 'ORDER BY name ASC;'
		all_skills = retrieve_skills_custom(self.dbm, query)

		return all_skills
	
	
		
	