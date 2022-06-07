import os
import base64
import binascii
import codecs
import hashlib
import random
import sqlite3
import uuid
import datetime

from flask import Flask, session, render_template, request, redirect
from dbm import DBM

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"


class CRender:
	def __init__ (self, dbm, auth_keys):
		self.dbm = dbm
		self.auth_keys = auth_keys

	"""
		DB Query Methods
	"""

	def jobs_jobs_general_query(self):
		query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop,
							Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo
					FROM Jobs, Orgs, Addresses
					WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		job_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				job = 	{
							'id': row[0],
							'title': row[1],
							'present': row[2],
							'date_start': row[3],
							'date_stop': row[4],
							'desc_short': row[5],
							'desc_long': row[6],
							'skills': row[7],
							'org': {
								'id': row[8],
								'name': row[9],
								'address': {
									'id': row[10],
									'name': row[11],
									'uri': row[12]
								},
								'phone': row[13],
								'website': row[14],
								'logo': row[15]
							}
						}

				skills = row[7].split(',')
				if len(skills) > 0:
					query = 'SELECT id, name, exposure, soft_or_hard, reference, icon, category FROM Skills WHERE '
					for i in range(len(skills)):
						if i != len(skills) - 1:
							query += 'id="' + skills[i] + '" OR '
						else:
							query += 'id="' + skills[i] + '";'
					result = self.dbm.execute(query)
					if result != None:
						result = self.dbm.cur.fetchall()
						skills_list = []
						for i in range(len(result)):
							s = {
									'id': result[i][0],
									'name': result[i][1],
									'exposure': result[i][2],
									'soft_or_hard': result[i][3],
									'reference': result[i][4],
									'icon': result[i][5],
									'category': result[i][6]
								}
							skills_list.append(s)
						job['skills'] = skills_list
					else:
						job['skills'] = None

				job_rows.append(job)

		job_rows = job_rows[-4:]
		job_rows = job_rows[::-1]
		return job_rows[0]['id']

	def jobs_jobs_query(self, id):
		query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop,
							Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.desc
					FROM Jobs, Orgs, Addresses
					WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		job_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				job = 	{
							'id': row[0],
							'title': row[1],
							'present': row[2],
							'date_start': row[3],
							'date_stop': row[4],
							'desc_short': row[5],
							'desc_long': row[6],
							'skills': row[7],
							'org': {
								'id': row[8],
								'name': row[9],
								'address': {
									'id': row[10],
									'name': row[11],
									'uri': row[12]
								},
								'phone': row[13],
								'website': row[14],
								'logo': row[15],
								'header': row[16],
								'desc': row[17]
							}
						}

				skills = row[7].split(',')
				if len(skills) > 0:
					query = 'SELECT id, name, exposure, soft_or_hard, reference, icon, category FROM Skills WHERE '
					for i in range(len(skills)):
						if i != len(skills) - 1:
							query += 'id="' + skills[i] + '" OR '
						else:
							query += 'id="' + skills[i] + '";'
					result = self.dbm.execute(query)
					if result != None:
						result = self.dbm.cur.fetchall()
						skills_list = []
						for i in range(len(result)):
							s = {
									'id': result[i][0],
									'name': result[i][1],
									'exposure': result[i][2],
									'soft_or_hard': result[i][3],
									'reference': result[i][4],
									'icon': result[i][5],
									'category': result[i][6]
								}
							skills_list.append(s)
						job['skills'] = skills_list
					else:
						job['skills'] = None

				job_rows.append(job)

		a_job = {}
		for i in range(len(job_rows)):
			if job_rows[i]['id'] == id:
				a_job['this'] = job_rows[i]
				if (i == len(job_rows) - 1):
					a_job['next'] = job_rows[0]
				else:
					a_job['next'] = job_rows[i+1]
				if (i == 0):
					a_job['last'] = job_rows[len(job_rows)-1]
				else:
					a_job['last'] = job_rows[i-1]
		return a_job

	def home_jobs_query(self):
		query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop,
							Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo
					FROM Jobs, Orgs, Addresses
					WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		job_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				job = 	{
							'id': row[0],
							'title': row[1],
							'present': row[2],
							'date_start': row[3],
							'date_stop': row[4],
							'desc_short': row[5],
							'desc_long': row[6],
							'skills': row[7],
							'org': {
								'id': row[8],
								'name': row[9],
								'address': {
									'id': row[10],
									'name': row[11],
									'uri': row[12]
								},
								'phone': row[13],
								'website': row[14],
								'logo': row[15]
							}
						}

				skills = row[7].split(',')
				if len(skills) > 0:
					query = 'SELECT id, name FROM Skills WHERE '
					for i in range(len(skills)):
						if i != len(skills) - 1:
							query += 'id="' + skills[i] + '" OR '
						else:
							query += 'id="' + skills[i] + '";'
					result = self.dbm.execute(query)
					if result != None:
						result = self.dbm.cur.fetchall()
						skills_list = []
						for i in range(len(result)):
							s = {
									'id': result[i][0],
									'name': result[i][1]
								}
							skills_list.append(s)
						job['skills'] = skills_list
					else:
						job['skills'] = None

				job_rows.append(job)

		job_rows = job_rows[-4:]
		return job_rows[::-1]

	def edus_edus_general_query(self):
		query = '''SELECT 	Education.id, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.desc,
							Orgs.website, Orgs.logo, Orgs.image_head, Education.degree, Education.gpa,
							Education.skill_ids, Education.date_end, Education.desc_short, Education.desc_long
					FROM	Education, Orgs, Addresses
					WHERE	Education.org = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		edu_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				edu = 	{
							'id': row[0],
							'org': {
								'id': row[1],
								'name': row[2],
								'address': {
									'id': row[3],
									'name': row[4],
									'uri': row[5]
								},
								'phone': row[6],
								'website': row[8],
								'logo': row[9],
								'header': row[10],
								'desc': row[7]
							},
							'degree': row[11],
							'gpa': row[12],
							'date_stop': row[14],
							'desc_short': row[15],
							'desc_long': row[16],
							'skills': row[13],
						}

				skills = row[7].split(',')
				if len(skills) > 0:
					query = 'SELECT id, name, exposure, soft_or_hard, reference, icon, category FROM Skills WHERE '
					for i in range(len(skills)):
						if i != len(skills) - 1:
							query += 'id="' + skills[i] + '" OR '
						else:
							query += 'id="' + skills[i] + '";'
					result = self.dbm.execute(query)
					if result != None:
						result = self.dbm.cur.fetchall()
						skills_list = []
						for i in range(len(result)):
							s = {
									'id': result[i][0],
									'name': result[i][1],
									'exposure': result[i][2],
									'soft_or_hard': result[i][3],
									'reference': result[i][4],
									'icon': result[i][5],
									'category': result[i][6]
								}
							skills_list.append(s)
						edu['skills'] = skills_list
					else:
						edu['skills'] = None

				edu_rows.append(edu)
		edu_rows = edu_rows[-4:]
		edu_rows = edu_rows[::-1]
		return edu_rows[0]['id']

	def edus_edus_query(self, id):
		query = '''SELECT 	Education.id, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.desc,
							Orgs.website, Orgs.logo, Orgs.image_head, Education.degree, Education.gpa,
							Education.skill_ids, Education.date_end, Education.desc_short, Education.desc_long
					FROM	Education, Orgs, Addresses
					WHERE	Education.org = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		edu_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				edu = 	{
							'id': row[0],
							'org': {
								'id': row[1],
								'name': row[2],
								'address': {
									'id': row[3],
									'name': row[4],
									'uri': row[5]
								},
								'phone': row[6],
								'website': row[8],
								'logo': row[9],
								'header': row[10],
								'desc': row[7]
							},
							'degree': row[11],
							'gpa': row[12],
							'date_stop': row[14],
							'desc_short': row[15],
							'desc_long': row[16],
							'skills': row[13],
						}

				skills = row[13].split(',')
				if len(skills) > 0:
					query = 'SELECT id, name, exposure, soft_or_hard, reference, icon, category FROM Skills WHERE '
					for i in range(len(skills)):
						if i != len(skills) - 1:
							query += 'id="' + skills[i] + '" OR '
						else:
							query += 'id="' + skills[i] + '";'
					print(query)
					result = self.dbm.execute(query)
					if result != None:
						result = self.dbm.cur.fetchall()
						skills_list = []
						for i in range(len(result)):
							s = {
									'id': result[i][0],
									'name': result[i][1],
									'exposure': result[i][2],
									'soft_or_hard': result[i][3],
									'reference': result[i][4],
									'icon': result[i][5],
									'category': result[i][6]
								}
							skills_list.append(s)
						edu['skills'] = skills_list
					else:
						edu['skills'] = None

				edu_rows.append(edu)

		a_edu = {}
		for i in range(len(edu_rows)):
			if edu_rows[i]['id'] == id:
				a_edu['this'] = edu_rows[i]
				if (i == len(edu_rows) - 1):
					a_edu['next'] = edu_rows[0]
				else:
					a_edu['next'] = edu_rows[i+1]
				if (i == 0):
					a_edu['last'] = edu_rows[len(edu_rows)-1]
				else:
					a_edu['last'] = edu_rows[i-1]
		return a_edu

	def orgs_orgs_general_query(self):
		query = '''SELECT 	Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri,
							Orgs.desc, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.phone
					FROM 	Orgs, Addresses
					WHERE	Orgs.address = Addresses.id;'''

		results = self.dbm.execute(query)

		org_rows = []
		if results != None:
			results = self.dbm.cur.fetchall()
			for row in results:
				o = {
						'id': row[0],
						'name': row[1],
						'address': {
										'id': row[2],
										'name': row[3],
										'uri': row[4]
									},
						'desc': row[5],
						'website': row[6],
						'logo': row[7],
						'header': row[8],
						'phone': row[9]
					}
				org_rows.append(o)

		org_rows = org_rows[-4:]
		org_rows = org_rows[::-1]
		return org_rows[0]['id']

	def orgs_orgs_query(self, id):
		query = '''SELECT 	Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri,
							Orgs.desc, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.phone
					FROM 	Orgs, Addresses
					WHERE	Orgs.address = Addresses.id;'''

		results = self.dbm.execute(query)

		org_rows = []
		if results != None:
			results = self.dbm.cur.fetchall()
			for row in results:
				o = {
						'id': row[0],
						'name': row[1],
						'address': {
										'id': row[2],
										'name': row[3],
										'uri': row[4]
									},
						'desc': row[5],
						'website': row[6],
						'logo': row[7],
						'header': row[8],
						'phone': row[9]
					}
				org_rows.append(o)

		orgs = {}
		for i in range(len(org_rows)):
			if (org_rows[i]['id'] == id):
				orgs['this'] = org_rows[i]
				if i == len(org_rows) - 1:
					orgs['next'] = org_rows[0]
				else:
					orgs['next'] = org_rows[i + 1]
				if i == 0:
					orgs['last'] = org_rows[len(org_rows) - 1]
				else:
					orgs['last'] = org_rows[i - 1]
		return orgs

	def home_edu_query(self):
		query = '''SELECT	Education.id, Education.degree, Education.gpa, Education.skill_ids, Education.date_end, Education.desc_short,
							Education.desc_long, Orgs.id, Orgs.name, Orgs.phone, Orgs.website, Orgs.logo, Addresses.id, Addresses.name,
							Addresses.uri
					FROM	Education, Orgs, Addresses
					WHERE   Education.org = Orgs.id AND Orgs.address = Addresses.id;'''

		result = self.dbm.execute(query)
		edu_rows = []
		if result != None:
			result = self.dbm.cur.fetchall()

			for row in result:
				edu = {
					'id': row[0], 'degree': row[1], 'gpa': row[2], 'skills': row[3], 'date_end': row[4], 'desc_short': row[5],
					'desc_long': row[6],
					'org': {
						'id': row[7], 'name': row[8], 'phone': row[9], 'website': row[10], 'logo': row[11],
						'address': {
							'id': row[12], 'name': row[13], 'uri': row[14]
						}
					}
				}

				if row[3] != None:
					skills = row[3].split(',')
					if len(skills) > 0:
						query = 'SELECT id, name, exposure, soft_or_hard, reference, icon, category FROM Skills WHERE '
						for i in range(len(skills)):
							if i != len(skills) - 1:
								query += 'id="' + skills[i] + '" OR '
							else:
								query += 'id="' + skills[i] + '";'
						result = self.dbm.execute(query)
						if result != None:
							result = self.dbm.cur.fetchall()
							skills_list = []
							for i in range(len(result)):
								s = {
										'id': result[i][0],
										'name': result[i][1],
										'exposure': result[i][2],
										'soft_or_hard': result[i][3],
										'reference': result[i][4],
										'icon': result[i][5],
										'category': result[i][6]
									}
								skills_list.append(s)
							edu['skills'] = skills_list
						else:
							edu['skills'] = None

				edu_rows.append(edu)
		edu_rows = edu_rows[-3:]
		return edu_rows[::-1]

	def home_contact_query(self):
		query = 'SELECT * FROM Contact;'
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			if (len(result) > 0):
				contact_row = result[len(result) - 1]

				query = 'SELECT id, name, uri FROM Addresses WHERE id="' + contact_row[2] + '";'
				result = self.dbm.execute(query)
				if result != None:
					result = self.dbm.cur.fetchall()
					if (len(result) > 0):
						address_row = result[0]

						return {
								'id': contact_row[0],
								'name': contact_row[1],
								'address': {
									'id': address_row[0],
									'name': address_row[1],
									'uri': address_row[2]
								},
								'phone1': contact_row[3],
								'phone2': contact_row[4],
								'email': contact_row[5],
								'objective': contact_row[7]
								}
		return {
				'id': None,
				'name': None,
				'address': {
					'id': None,
					'name': None,
					'uri': None
				},
				'phone1': None,
				'phone2': None,
				'email': None,
				'objective': None
				}

	def skills_skills_general_query(self):
		query = '''SELECT	id, name, exposure, soft_or_hard, reference, icon, category
				   FROM		Skills
				   ORDER BY	name ASC;'''

		skill_rows = []
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			for row in result:
				s = {
						'id': row[0],
						'name': row[1],
						'exposure': row[2],
						'soft_or_hard': row[3],
						'reference': row[4],
						'icon': row[5],
						'category': row[6]
					}
				skill_rows.append(s)

		return skill_rows

	def skills_skills_query(self, id):
		query = '''SELECT	id, name, exposure, soft_or_hard, reference, icon, category, desc, desc_long
				   FROM		Skills
				   WHERE	id="'''+id+'''";'''

		this_skill = {}
		this_skill['similar'] = []
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			for row in result:
				s = {
						'id': row[0],
						'name': row[1],
						'exposure': row[2],
						'soft_or_hard': row[3],
						'reference': row[4],
						'icon':	row[5],
						'category': row[6],
						'desc': row[7],
						'desc_long': row[8]
					}
				this_skill['this'] = s

		query = '''SELECT	id, name, exposure, soft_or_hard, reference, icon, category, desc, desc_long
				   FROM		Skills
				   WHERE	soft_or_hard='''+str(this_skill['this']['soft_or_hard'])+'''
							AND category="'''+this_skill['this']['category']+'''"
							AND id!="'''+this_skill['this']['id']+'''";'''

		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			for row in result:
				s = {
						'id': row[0],
						'name': row[1],
						'exposure': row[2],
						'soft_or_hard': row[3],
						'reference': row[4],
						'icon':	row[5],
						'category': row[6],
						'desc': row[7],
						'desc_long': row[8]
					}
				this_skill['similar'].append(s)
		random.shuffle(this_skill['similar'])

		query1 = '''SELECT Jobs.id, Jobs.title, Orgs.id, Orgs.name, Orgs.logo, Jobs.skill_ids
					FROM Jobs, Orgs
					WHERE Jobs.org_id = Orgs.id;'''
		query2 = '''SELECT Education.id, Education.degree, Orgs.id, Orgs.name, Orgs.logo, Education.skill_ids
					FROM Education, Orgs
					WHERE Education.org = Orgs.id;'''

		appears_in = [[], []]
		result = self.dbm.execute(query1)
		if result != None:
			result = self.dbm.cur.fetchall()
			if len(result) > 0:
				for row1 in result:
					skilllist = row1[5]
					skills = skilllist.split(',')
					if id in skills:
						this = { 'id': row1[0], 'title': row1[1], 'org': { 'id': row1[2], 'name': row1[3], 'logo': row1[4] } }
						appears_in[0].append(this)
		result = self.dbm.execute(query2)
		if result != None:
			result = self.dbm.cur.fetchall()
			if len(result) > 0:
				for row2 in result:
					skilllist = row2[5]
					skills = skilllist.split(',')
					if id in skills:
						this = {'id': row2[0], 'degree': row2[1], 'org': { 'id': row2[2], 'name': row2[3], 'logo': row2[4] } }
						appears_in[1].append(this)

		this_skill['appears_in'] = appears_in
		this_skill['similar'] = this_skill['similar'][-6:]
		return this_skill

	def skills_for_add_query(self):
		query = "SELECT id, name FROM Skills;"
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			all_skills = []
			if len(result) > 0:
				for row in result:
					s = {
						'id': row[0],
						'name': row[1],
					}
					all_skills.append(s)
				return all_skills
			else:
				return []
		else:
			return []

	def orgs_for_add_query(self):
		query = "SELECT id, name FROM Orgs;"
		result = self.dbm.execute(query)
		if result != None:
			result = self.dbm.cur.fetchall()
			all_orgs = []
			if len(result) > 0:
				for row in result:
					o = {
						'id': row[0],
						'name': row[1]
					}
					all_orgs.append(o)
				return all_orgs
			else:
				return []
		else:
			return []

	"""
		HTML Conversion Methods
	"""

	def home_home_htmlify(self, contact_dict, edus_dict, jobs_dict, session):
		html = ""
		if not session['mobile']:
			html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;">
					<h1 style="position:absolute;left:50%;top:25%;color:white;font-size:55px;">'''+contact_dict['name']+'''</h1>

					<div style="position:absolute;left:50%;top:55%;z-index:2;">
						<img src="/static/Addr.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="'''+contact_dict['address']['uri']+'''" style="color:white;">'''+contact_dict['address']['name']+'''</a>
						</h4>
					</div>

					<div style="position:absolute;left:50%;top:67.5%;z-index:2;">
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;padding-left:5px;position:relative;top:5px;">
						<a href="'''+self.telelink(contact_dict['phone1'])+'''" style="color:white;">'''+self.teleformat(contact_dict['phone1'])+'''</a></h4>
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;position:relative;left:50px;" />
						<h4 style="display:inline;padding-left:5px;position:relative;left:50px;top:5px;">
						<a href="'''+self.telelink(contact_dict['phone2'])+'''" style="color:white;">'''+self.teleformat(contact_dict['phone2'])+'''</a></h4>
					</div>

					<div style="position:absolute;left:50%;top:80%;z-index:2;">
						<img src="/static/Mail.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="mailto:'''+contact_dict['email']+'''" style="color:white;">'''+contact_dict['email']+'''</a>
						</h4>
					</div>

					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;"/>

				</div>
				<br>'''
			html +='''	<div class="row" style="overflow:hidden;">
					<div class="col-sm-5" style="padding-left:40px;">
						<h2 class="mb-4">Objective</h2>
							<div class="card w-75">
								<div class="card-body">
									'''+contact_dict['objective']+'''
								</div>
							</div>
						<br>
						<div class="row" style="width:75%;">
							<div class="col">
								<h2 class="mb-4">Education</h2>
							</div>
							<div class="col">'''
			if session.get('auth_key') != self.auth_keys['Readers']:
				html +=	'''<a href="javascript:void(0)" data-toggle="modal" data-target="#addEduModal"><button style="position:relative;width:50px;margin-left:auto;margin-right:0;" type="button" class="btn btn-success btn-lg btn-block">+</button></a>'''
			html +=					'''</div>
						</div>
								'''
			for edu in edus_dict:
				html += self.home_edu_htmlify(edu, False)
			html+=			'''
					<span style="display:inline-block;border-left:1px solid #ccc;height:100%;position:relative;top:-100%;left:90%;"></span>
					</div>

					<div class="col-sm-7">
						<div class="row" style="width:75%;">
							<div class="col">
								<h2 class="mb-4">Experience</h2>
							</div>
							<div class="col">'''
			if session.get('auth_key') != self.auth_keys['Readers']:
				html +=	'''<a href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal"><button type="button" style="position:relative;width:50px;margin-left:auto;margin-right:0;" class="btn btn-success btn-lg btn-block">+</button></a>'''
			html +=					'''</div>
								</div>'''
			for job in jobs_dict:
				html += self.home_job_htmlify(job, False)

			html +=		'''</div>
						</div>
					</body>
				</html>'''

		else:
			html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;">
					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;"/>
				</div>
				<div class="row" style="overflow:hidden;">
					<div class="col-sm-12">
						<div class="card">
							<div class="card-header">
								<h4>Contact Information</h4>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<h6>'''+contact_dict['name']+'''</h6>
									</li>
									<li class="list-group-item">
										<h6>Phone</h6>
										<div class="col-sm-6" style="display:inline;">
											<a href="'''+self.telelink(contact_dict['phone1'])+'''">'''+self.teleformat(contact_dict['phone1'])+'''</a>
										</div>
										<div class="col-sm-6" style="display:inline;">
											<a href="'''+self.telelink(contact_dict['phone2'])+'''">'''+self.teleformat(contact_dict['phone2'])+'''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6>Email</h6>
										<div class="col-sm-12">
											<a href="mailto:'''+contact_dict['email']+'''">'''+contact_dict['email']+'''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6>Address</h6>
										<div class="col-sm-12">
											<a href="'''+contact_dict['address']['uri']+'''">'''+contact_dict['address']['name']+'''</a>
										</div>
										<div class="col-sm-12">
												<iframe
													width="325"
													height="200"
													frameborder="0" style="border:0"
													referrerpolicy="no-referrer-when-downgrade"
													src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q='''+contact_dict['address']['name']+'''"
													allowfullscreen>
												</iframe>
										</div>
									</li>
								</ul>
							</div>
						</div>'''
			html +='''
							<div class="card">
								<div class="card-header">
									<h4 style="padding-left:20px;">Objective</h4>
								</div>
								<div class="card-body">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
										'''+contact_dict['objective']+'''
										</li>
									</ul>
								</div>
							</div>
					<div class="card w-100">
						<div class="card-header">
							<div style="position:relative; width:100%; height:100%; margin-bottom:35px;">
								<div style="position:absolute;left:0%;width:85%; height:100%;">
									<h4 style="padding-left:20px; height:100%;">Experience</h4>
								</div>
								<div style="position:absolute;left:85%;width:15%;top:-7.5px;">
										'''
			if session.get('auth_key') != self.auth_keys['Readers']:
				html +=	'''			<a href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal"><button type="button" class="btn btn-success btn-lg btn-block">+</button></a>'''
			html += '''			</div>
							</div>
						</div>
					</div>'''


			for job in jobs_dict:
				html += self.home_job_htmlify(job, True)
			html += '''<div class="card w-100">
							<div class="card-header">
								<div style="position:relative; width:100%; height:100%; margin-bottom:35px;">
									<div style="position:absolute;left:0%;width:85%; height:100%;">
										<h4 style="padding-left:20px; height:100%;">Education</h4>
									</div>
								<div style="position:absolute;left:85%;width:15%;top:-7.5px;">
										'''
			if session.get('auth_key') != self.auth_keys['Readers']:
				html +=	'''			<a href="javascript:void(0)"><button type="button" class="btn btn-success btn-lg btn-block">+</button></a>'''
			html += '''			</div>
							</div>
						</div>
					</div>'''


			for edu in edus_dict:
				html += self.home_edu_htmlify(edu, True)
			html+=			'''
					<span style="display:inline-block;border-left:1px solid #ccc;height:100%;position:relative;top:-100%;left:90%;"></span>
					</body>
				</html>'''

		return html


	def home_job_htmlify(self, job, mobile):
		src = "data:image/png;base64,"
		src += job['org']['logo'].decode('utf-8')
		date_start = datetime.datetime.strptime(job['date_start'], '%m/%d/%Y')

		if (job['present'] == 1):
			date_stop = 'Present'
		else:
			date_stop = datetime.datetime.strptime(job['date_stop'], '%m/%d/%Y')

		date_start_str = date_start.strftime('%b %Y')
		if job['present'] != 1:
			date_stop_str = date_stop.strftime('%b %Y')
		else:
			date_stop_str = 'Present'

		if not mobile:
			html = '''
				<div class="card w-75">
					<div class="card-header">
						<div class="row">
							<div class="col-1">
								<img width="30" height="30" src="''' + src + '''" />
							</div>
							<div class="col-6">
								<a href="/orgs/'''+str(job['org']['id'])+'''" style="color:black;">
								<h6 style="margin-top:5px;">''' + str(job['org']['name']) + '''</h6>
								</a>
							</div>
						</div>
					</div>
					<div class="card-body">
						<ul class="list-group list-group-flush">
							<li class="list-group-item">
								<div class="row">
									<div class="col-7">
										<a href="/jobs/'''+job['id']+'''" style="color:black">
											<h5 class="card-title">''' + str(job['title']) + '''</h5>
										</a>
									</div>
									<div class="col-5" style="text-align:right;">
										<i style="margin-top:5px;">''' + date_start_str + ''' - ''' + date_stop_str + '''</i>
									</div>
								</div>

								<p class="card-text">''' + str(job['desc_short']) + '''</p>
								<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
									<a href="/jobs/''' + str(job['id']) + '''">''' + str(job['id']) + '''</a>
								</div>
							</li>
							<li class="list-group-item">
								<h6 style="margin-top:5px;">Skills</h6>
								<div class="row" style="margin-top:10px;display:inline;">
						'''
			if job['skills'] != None:
				for skill in job['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=			'''
								</div>
							</li>
						</ul>
					</div>


				</div>
			<br>'''
		else:
			html = '''
				<div class="card w-100">
					<div class="card-header">
						<div class="row">
							<div class="col-1">
								<img width="30" height="30" src="''' + src + '''" />
							</div>
							<div class="col-11">
								<a href="/orgs/'''+str(job['org']['id'])+'''" style="color:black;">
								<h6 style="margin-top:5px;"><u>''' + str(job['org']['name']) + '''</u></h6>
								</a>
							</div>
						</div>
					</div>
					<div class="card-body">
						<ul class="list-group list-group-flush">
							<li class="list-group-item">
								<div class="row">
									<div class="col-7">
										<a href="/jobs/'''+job['id']+'''" style="color:black">
											<h5 class="card-title"><u>''' + str(job['title']) + '''</u></h5>
										</a>
									</div>
									<div class="col-5" style="text-align:right;">
										<i style="margin-top:5px;">''' + date_start_str + ''' - ''' + date_stop_str + '''</i>
									</div>
								</div>

								<p class="card-text">''' + str(job['desc_short']) + '''</p>
								<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
									<a href="/jobs/''' + str(job['id']) + '''">''' + str(job['id']) + '''</a>
								</div>
							</li>
							<li class="list-group-item">
								<h6 style="margin-top:5px;">Skills</h6>
								<div class="row" style="margin-top:10px;display:inline;">
						'''
			if job['skills'] != None:
				for skill in job['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=			'''
								</div>
							</li>
						</ul>
					</div>


				</div>
			'''

		return html

	def home_edu_htmlify(self, edu, mobile):
		src = "data:image/png;base64,"
		src += edu['org']['logo'].decode('utf-8')

		date_stop = datetime.datetime.strptime(edu['date_end'], '%m/%d/%Y')
		date_stop_str = date_stop.strftime('%b %Y')
		if not mobile:
			html = '''
				<div class="card w-75">
					<div class="card-header">
						<div class="row">
							<div class="col-1">
								<img width="30" height="30" src="''' + src + '''" />
							</div>
							<div class="col-6">
								<a href="/orgs/'''+str(edu['org']['id'])+'''" style="color:black;">
								<h6 style="margin-top:5px;">''' + str(edu['org']['name']) + '''</h6>
								</a>
							</div>
						</div>
					</div>
					<div class="card-body">
						<ul class="list-group list-group-flush">
							<li class="list-group-item">
								<div class="row">
									<div class="col-7">
										<a href="/edus/'''+str(edu['id'])+'''" style="color:black;">
										<h5 class="card-title">''' + str(edu['degree']) + '''</h5></a>
									</div>
									<div class="col-5" style="text-align:right;">
										<i style="margin-top:5px;">''' + date_stop_str + '''</i>
									</div>
								</div>

								<p class="card-text">''' + str(edu['desc_short']) + '''</p>
								<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
									<a href="/edus/''' + str(edu['id']) + '''">''' + str(edu['id']) + '''</a>
								</div>
							</li>
							<li class="list-group-item">
								<h6 style="margin-top:5px;">Skills</h6>
								<div class="row" style="margin-top:10px;display:inline;">
						'''
			if edu['skills'] != None:
				for skill in edu['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=			'''
								</div>
							</li>
						</ul>
					</div>
				</div>
			<br>'''
		else:
			html = '''
				<div class="card w-100">
					<div class="card-header">
						<div class="row">
							<div class="col-1">
								<img width="30" height="30" src="''' + src + '''" />
							</div>
							<div class="col-11">
								<a href="/orgs/'''+str(edu['org']['id'])+'''" style="color:black;">
								<h6 style="margin-top:5px;"><u>''' + str(edu['org']['name']) + '''</u></h6>
								</a>
							</div>
						</div>
					</div>
					<div class="card-body">
						<ul class="list-group list-group-flush">
							<li class="list-group-item">
								<div class="row">
									<div class="col-7">
										<a href="/edus/'''+str(edu['id'])+'''" style="color:black;">
										<h5 class="card-title"><u>''' + str(edu['degree']) + '''</u></h5></a>
									</div>
									<div class="col-5" style="text-align:right;">
										<i style="margin-top:5px;">''' + date_stop_str + '''</i>
									</div>
								</div>

								<p class="card-text">''' + str(edu['desc_short']) + '''</p>
								<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
									<a href="/edus/''' + str(edu['id']) + '''">''' + str(edu['id']) + '''</a>
								</div>
							</li>
							<li class="list-group-item">
								<h6 style="margin-top:5px;">Skills</h6>
								<div class="row" style="margin-top:10px;display:inline;">
						'''
			if edu['skills'] != None:
				for skill in edu['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=			'''
								</div>
							</li>
						</ul>
					</div>
				</div>'''

		return html

	def jobs_jobs_htmlify(self, jobs, mobile):
		if not mobile:
			html = self.org_htmlify(jobs['this']['org'], jobs['next']['org'], jobs['last']['org'], 'jobs', jobs['next']['id'], jobs['last']['id'], mobile)
			html += '''		<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
								<div class="card-header">
									<div class="row">
										<div class="col-sm-7">
											<h4 style="vertical-align:middle;">'''+jobs['this']['title']+'''</h4>
										</div>
										<div class="col-sm-5" style="text-align:right;">
											<i style="vertical-align:middle;">
									'''
			if jobs['this']['date_stop'] != None:
				html += self.datereformat(jobs['this']['date_start'])+''' - '''+self.datereformat(jobs['this']['date_stop'])+'''</i>'''
			else:
				html += self.datereformat(jobs['this']['date_start'])+''' - Present</i>'''
			html +=			'''</div></div></div>
								<div class="card-body" style="z-index:0;">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
											<h6>Abstract</h6>
											'''+jobs['this']['desc_short']+'''
											<br><br>
											<h6>Description</h6>
											'''+jobs['this']['desc_long']+'''
											<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
												<a href="/jobs/''' + str(jobs['this']['id']) + '''">''' + str(jobs['this']['id']) + '''</a>
											</div>
										</li>
										<li class="list-group-item">
											<h6 style="margin-top:5px;">Skills</h6>
											<div class="row" style="margin-top:10px;display:inline;">'''
			if jobs['this']['skills'] != None:
				for skill in jobs['this']['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=						'''</li>
									</ul>
								</div>
							</div>
						</div>
					</div>

			'''
		else:
			html = self.org_htmlify(jobs['this']['org'], jobs['next']['org'], jobs['last']['org'], 'jobs', jobs['next']['id'], jobs['last']['id'], mobile)
			html += '''		<div class="card">
								<div class="card-body">
									<div class="row">
										<div class="col-sm-12">
											<div style="position:relative;width:50%;left:0%;display:inline;">
												<a href="/jobs/'''+jobs['last']['id']+'''" style="text-align:left;">< Last Job</a>
											</div>
											<div style="position:relative;width:50%;left:50%;display:inline;">
												<a href="/jobs/'''+jobs['next']['id']+'''" style="text-align:right;position:relative;width:50%;">Next Job ></a>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="card">
								<div class="card-header">
									<div class="row">
										<div class="col-sm-7">
											<h4 style="vertical-align:middle;">'''+jobs['this']['title']+'''</h4>
										</div>
										<div class="col-sm-5" style="text-align:right;">
											<i style="vertical-align:middle;">
									'''
			if jobs['this']['date_stop'] != None:
				html += self.datereformat(jobs['this']['date_start'])+''' - '''+self.datereformat(jobs['this']['date_stop'])+'''</i>'''
			else:
				html += self.datereformat(jobs['this']['date_start'])+''' - Present</i>'''
			html +=			'''</div></div></div>
								<div class="card-body" style="z-index:0;">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
											<h6>Abstract</h6>
											'''+jobs['this']['desc_short']+'''
											<br><br>
											<h6>Description</h6>
											'''+jobs['this']['desc_long']+'''
											<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
												<a href="/jobs/''' + str(jobs['this']['id']) + '''">''' + str(jobs['this']['id']) + '''</a>
											</div>
										</li>
										<li class="list-group-item">
											<h6 style="margin-top:5px;">Skills</h6>
											<div class="row" style="margin-top:10px;display:inline;">'''
			if jobs['this']['skills'] != None:
				for skill in jobs['this']['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=						'''</li>
									</ul>
								</div>
							</div>
						</div>
					</div>

			'''

		return html

	def edus_edus_htmlify(self, edus, mobile):
		if not mobile:
			html = self.org_htmlify(edus['this']['org'], edus['next']['org'], edus['last']['org'], 'edus', edus['next']['id'], edus['last']['id'], mobile)
			html += '''
							<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
								<div class="card-header">
									<div class="row">
										<div class="col-sm-7">
											<h4 style="vertical-align:middle;">'''+edus['this']['degree']+'''</h4>
										</div>
										<div class="col-sm-5" style="text-align:right;">
											<i style="vertical-align:middle;">
									'''

			html += self.datereformat(edus['this']['date_stop'])+'''</i>'''
			html +=		'''</div></div></div>
								<div class="card-body" style="z-index:0;">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
											<h6>Abstract</h6>
											'''+edus['this']['desc_short']+'''
											<br><br>
											<h6>Description</h6>
											'''+edus['this']['desc_long']+'''
											<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
												<a href="/edus/''' + str(edus['this']['id']) + '''">''' + str(edus['this']['id']) + '''</a>
											</div>
										</li>
										<li class="list-group-item">
											<h6 style="margin-top:5px;">Skills</h6>
											<div class="row" style="margin-top:10px;display:inline;">'''
			if edus['this']['skills'] != None:
				for skill in edus['this']['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=						'''</li>
									</ul>
								</div>
							</div>
						</div>
					</div>

			'''
		else:
			html = self.org_htmlify(edus['this']['org'], edus['next']['org'], edus['last']['org'], 'edus', edus['next']['id'], edus['last']['id'], mobile)
			html += '''		<div class="card">
								<div class="card-body">
									<div class="row">
										<div class="col-sm-12">
											<div style="position:relative;width:50%;left:0%;display:inline;">
												<a href="/edus/'''+edus['last']['id']+'''" style="text-align:left;">< Last Edu</a>
											</div>
											<div style="position:relative;width:50%;left:50%;display:inline;">
												<a href="/edus/'''+edus['next']['id']+'''" style="text-align:right;position:relative;width:50%;">Next Edu ></a>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="card">
								<div class="card-header">
									<div class="row">
										<div class="col-sm-7">
											<h4 style="vertical-align:middle;">'''+edus['this']['degree']+'''</h4>
										</div>
										<div class="col-sm-5" style="text-align:right;">
											<i style="vertical-align:middle;">
									'''

			html += self.datereformat(edus['this']['date_stop'])+'''</i>'''
			html +=		'''</div></div></div>
								<div class="card-body" style="z-index:0;">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
											<h6>Abstract</h6>
											'''+edus['this']['desc_short']+'''
											<br><br>
											<h6>Description</h6>
											'''+edus['this']['desc_long']+'''
											<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
												<a href="/edus/''' + str(edus['this']['id']) + '''">''' + str(edus['this']['id']) + '''</a>
											</div>
										</li>
										<li class="list-group-item">
											<h6 style="margin-top:5px;">Skills</h6>
											<div class="row" style="margin-top:10px;display:inline;">'''
			if edus['this']['skills'] != None:
				for skill in edus['this']['skills']:
					html += '<a href="/skills/'+skill['id']+'" style="padding-left:10px;"><span class="badge badge-pill badge-dark">'+skill['name']+'</span></a>'
			html +=						'''</li>
									</ul>
								</div>
							</div>
						</div>
					</div>

			'''

		return html

	def org_htmlify(self, org, next, last, t, next_id, last_id, mobile):
		logo = "data:image/png;base64,"
		logo += org['logo'].decode('utf-8')
		head = "data:image/png;base64,"
		head += org['header'].decode('utf-8')

		if not mobile:
			html = '''<div class="jumbotron">
						<img src="'''+head+'''" style="position:relative;width:70%;left:15%;z-index:0;max-height:25%;"/>
						'''
			if t == 'orgs':
				html += '''
						<a href="/orgs/'''+next['id']+'''">
							<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
						</a>
						<a href="/orgs/'''+last['id']+'''">
							<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
						</a>
						'''
			elif t == 'jobs':
				html += '''
						<a href="/jobs/'''+next_id+'''">
							<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
						</a>
						<a href="/jobs/'''+last_id+'''">
							<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
						</a>
						'''
			elif t == 'edus':
				html += '''
						<a href="/edus/'''+next_id+'''">
							<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
						</a>
						<a href="/edus/'''+last_id+'''">
							<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
						</a>
						'''

			html += ''' <br>
						<div style="position:relative;width:100%;z-index=1;">


							<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
								<div class="card-header">
									<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
										<img src="'''+logo+'''" width="45" height="45"/>
									</div>
									<a href="/orgs/'''+org['id']+'''" style="color:black;">
										<h4 style="display:inline;padding-left:10px;vertical-align:middle;">'''+org['name']+'''</h4>
									</a>
								</div>
								<div class="card-body" style="z-index:0;">
									<div class="row">
										<div class="col-sm-6">
											<h6>Description:</h6>
											'''+org['desc']+'''
										</div>
										<div class="col-sm-2">
											<h6>Information:</h6>
											'''+self.addresslines(org['address']['name'])+'''
											<a href="'''+self.telelink(org['phone'])+'''">'''+self.teleformat(org['phone'])+'''
											<br>
											<a href="'''+org['website']+'''" target="_blank">Website</a>
										</div>
										<div class="col-sm-4">
											<iframe
												width="290"
												height="200"
												frameborder="0" style="border:0"
												referrerpolicy="no-referrer-when-downgrade"
												src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q='''+org['address']['name']+'''"
												allowfullscreen>
											</iframe>
										</div>
									</div>
									<div style="position:relative;left:71%;width:25%;font-size:8px;text-align:right;padding-top:10px;">
										<a href="/orgs/''' + str(org['id']) + '''">''' + str(org['id']) + '''</a>
									</div>
								</div>
							</div>
							<br>'''
		else:
			html = '''<div class="jumbotron">
						<img src="'''+head+'''" style="position:relative;width:100%;left:0%;z-index:0;"/>
						'''

			html += '''
						<div style="position:relative;width:100%;z-index=1;">
							<div class="card">
								<div class="card-header">
									<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
										<img src="'''+logo+'''" width="45" height="45"/>
									</div>
									<a href="/orgs/'''+org['id']+'''" style="color:black;"><u>
										<h4 style="display:inline;padding-left:10px;vertical-align:middle;">'''+org['name']+'''</u></h4>
									</a>
								</div>
								<div class="card-body" style="z-index:0;">
									<div class="row">
										<div class="col-sm-8">
											<h6>Description:</h6>
											'''+org['desc']+'''<br><br>
										</div>
										<div class="col-sm-4">
												<h6>Information:</h6>
												'''+self.addresslines(org['address']['name'])+'''
												<a href="'''+self.telelink(org['phone'])+'''">'''+self.teleformat(org['phone'])+'''
												<br>
												<a href="'''+org['website']+'''" target="_blank">Website</a>
										</div>
										<div class="col-sm-4">
											<iframe
												width="350"
												height="200"
												frameborder="0" style="border:0"
												referrerpolicy="no-referrer-when-downgrade"
												src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q='''+org['address']['name']+'''"
												allowfullscreen>
											</iframe>
										</div>
									</div>
									<div style="position:relative;left:71%;width:25%;font-size:8px;text-align:right;padding-top:10px;">
										<a href="/orgs/''' + str(org['id']) + '''">''' + str(org['id']) + '''</a>
									</div>
								</div>
							</div>
							'''
		return html

	def skills_general_htmlify(self, all_skills, mobile):
		if not mobile:
			html = '''
					<div class="jumbotron">
						<div class="row">
							<div class="col-sm-6 mx-auto">
								<h1 style="text-align:center;">Skills</h1>
							</div>
						</div>
						<br>
						<div class="row">
							<div class="col-sm-10 mx-auto">
								<div class="card w-100">
									<div class="card-header">
										<h4>Technical Skills</h4>
									</div>
									<div class="card-body">
										<div class="row">'''
			for s in all_skills:
				if s['soft_or_hard'] == 1:
					src = "data:image/png;base64,"
					src += s['icon'].decode('utf-8')

					html += '''<div class="col-sm-2">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''

			html += '''					</div>
									</div>
								</div>
							</div>
						</div>
						<br>
						<div class="row">
							<div class="col-sm-10 mx-auto">
								<div class="card w-100">
									<div class="card-header">
										<h4>Soft Skills</h4>
									</div>
									<div class="card-body">
										<div class="row">'''
			for s in all_skills:
				if s['soft_or_hard'] == 0:
					src = "data:image/png;base64,"
					src += s['icon'].decode('utf-8')

					html += '''<div class="col-sm-2">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''

			html += '''					</div>
									</div>
								</div>
							</div>
						</div>
					</div>
			'''
		else:
			html = '''
					<div class="jumbotron">
						<div class="row">
							<div class="col-sm-6 mx-auto">
								<h1 style="text-align:center;">Skills</h1>
							</div>
						</div>
						<br>
						<div class="row">
							<div class="col-sm-10 mx-auto">
								<div class="card w-100">
									<div class="card-header">
										<h4>Technical Skills</h4>
									</div>
									<div class="card-body">
										<div class="row">'''
			for s in all_skills:
				if s['soft_or_hard'] == 1:
					src = "data:image/png;base64,"
					src += s['icon'].decode('utf-8')

					html += '''<div class="col-sm-4">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''

			html += '''					</div>
									</div>
								</div>
							</div>
						</div>
						<br>
						<div class="row">
							<div class="col-sm-10 mx-auto">
								<div class="card w-100">
									<div class="card-header">
										<h4>Soft Skills</h4>
									</div>
									<div class="card-body">
										<div class="row">'''
			for s in all_skills:
				if s['soft_or_hard'] == 0:
					src = "data:image/png;base64,"
					src += s['icon'].decode('utf-8')

					html += '''<div class="col-sm-4">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''

			html += '''					</div>
									</div>
								</div>
							</div>
						</div>
					</div>
			'''

		return html

	def skills_skills_htmlify(self, skill, mobile):
		if not mobile:
			src = "data:image/png;base64,"
			src += skill['this']['icon'].decode('utf-8')

			html = '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-8 mx-auto">
									<div class="card w-100">
										<div class="card-header" >
											<img src="'''+src+'''" width="40" height="40" style="display:inline;"/>
											<h4 style="display:inline;padding-left:15px;vertical-align:middle;">'''+skill['this']['name']+'''</h4>
										</div>
										<div class="card-body">
											<ul class="list-group list-group-flush">
												<li class="list-group-item">
													<div class="row">
														<h5>Details</h5>
													</div><br>
													<div class="row">
														<div class="col-sm-6">
															<h6>Comments</h6>
														</div>
														<div class="col-sm-6">
															<h6>Exposure</h6>
														</div>
													</div>
													<div class="row">
														<div class="col-sm-8">
															'''+skill['this']['desc_long']+'''
														</div>
														<div class="col-sm-4">
															<div class="progress">
																<div class="progress-bar" role="progressbar" aria-valuenow="'''+str(skill['this']['exposure'] * 10)+'''" aria-valuemin="0" aria-valuemax="100" style="width: '''+str(skill['this']['exposure'] * 10)+'''%;"></div>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Meta</h5>
													</div>
													<div class="row">
														<div class="col-sm-6">
															<h6>Description</h6>
														</div>
														<div class="col-sm-4">
															<h6>Information</h6>
														</div>
													</div>
													<div class="row">
														<div class="col-sm-6">
															'''+skill['this']['desc']+'''
														</div>
														<div class="col-sm-4">
															<div>
																Technical Skill: '''
			if skill['this']['soft_or_hard'] == 1:
				html += "<b>True</b>"
			else:
				html += "<b>False</b>"
			html +=										'''<br>
																Category: <b>'''+skill['this']['category']+'''</b><br>

																Reference: <a href="'''+skill['this']['reference']+'''" target="_blank">Website</a><br>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Similar</h5>
													</div>
													<div class="row">'''
			for s in skill['similar']:
				src = "data:image/png;base64,"
				src += s['icon'].decode('utf-8')
				html += '''<div class="col-sm-2">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''
			html += 							'''</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Exposed In</h5>
													</div>'''
			if (len(skill['appears_in'][0]) == 0 and len(skill['appears_in'][1]) == 0):
				html += '<div class="row"><i>No appearances in education or work experiences</i></div>'
			else:
				if len(skill['appears_in'][0]) > 0:
					html += '<div class="row"><div class="col-sm-12"><h6>Work Experiences</h6></div></div><div class="row">'
					for s in skill['appears_in'][0]:
						img = "data:image/png;base64," + s['org']['logo'].decode('utf-8')
						html += '''
										<div class="col-sm-6">
											<span style="display:inline;">
												<a href="/jobs/'''+s['id']+'''">
													<img src="'''+img+'''" width="25" height="25" />
													'''+s['org']['name']+''' -
													'''+s['title']+'''
												</a>
											</span>
										</div>
									'''
					html += '</div>'
				if len(skill['appears_in'][1]) > 0:
					html += '<div class="row"><div class="col-sm-12"><h6>Education</h6></div></div><div class="row">'
					for s in skill['appears_in'][1]:
						img = "data:image/png;base64," + s['org']['logo'].decode('utf-8')
						html += '''
										<div class="col-sm-6">
											<span style="display:inline;">
												<a href="/edus/'''+s['id']+'''">
													<img src="'''+img+'''" width="25" height="25" />
													'''+s['org']['name']+''' -
													'''+s['degree']+'''
												</a>
											</span>
										</div>
									'''
					html += '</div>'
			html += '''
												</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</div>
					'''
		else:
			src = "data:image/png;base64,"
			src += skill['this']['icon'].decode('utf-8')

			html = '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-8 mx-auto">
									<div class="card w-100">
										<div class="card-header" >
											<img src="'''+src+'''" width="40" height="40" style="display:inline;"/>
											<h4 style="display:inline;padding-left:15px;vertical-align:middle;">'''+skill['this']['name']+'''</h4>
										</div>
										<div class="card-body">
											<ul class="list-group list-group-flush">
												<li class="list-group-item">
													<div class="row">
														<h5>Details</h5>
													</div><br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Comments</h6>
														</div>
														<div class="col-sm-8">
															'''+skill['this']['desc_long']+'''
														</div>
													</div>
													<br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Exposure</h6>
														</div>
														<div class="col-sm-8">
															<div class="progress">
																<div class="progress-bar" role="progressbar" aria-valuenow="'''+str(skill['this']['exposure'] * 10)+'''" aria-valuemin="0" aria-valuemax="100" style="width: '''+str(skill['this']['exposure'] * 10)+'''%;"></div>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Meta</h5>
													</div>
													<div class="row">
														<div class="col-sm-4">
															<h6>Description</h6>
														</div>
														<div class="col-sm-8">
															'''+skill['this']['desc']+'''
														</div>
													</div>
													<br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Information</h6>
														</div>
														<div class="col-sm-8">
															<div>
																Technical Skill: '''
			if skill['this']['soft_or_hard'] == 1:
				html += "<b>True</b>"
			else:
				html += "<b>False</b>"
			html +=										'''<br>
																Category: <b>'''+skill['this']['category']+'''</b><br>

																Reference: <a href="'''+skill['this']['reference']+'''" target="_blank">Website</a><br>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Similar</h5>
													</div>
													<div class="row">'''
			for s in skill['similar']:
				src = "data:image/png;base64,"
				src += s['icon'].decode('utf-8')
				html += '''<div class="col-sm-6">
									<a href="/skills/'''+s['id']+'''">
										<span style="display:inline;">
											<img src="'''+src+'''" width="25" height="25" />
											<span class="badge badge-pill badge-dark">'''+s['name']+'''</span>
										</span>
									</a>
								</div>
							'''
			html += 							'''</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Exposed In</h5>
													</div>'''
			if (len(skill['appears_in'][0]) == 0 and len(skill['appears_in'][1]) == 0):
				html += '<div class="row"><i>No appearances in education or work experiences</i></div>'
			else:
				if len(skill['appears_in'][0]) > 0:
					html += '<div class="row"><div class="col-sm-12"><h6>Work Experiences</h6></div></div><div class="row">'
					for s in skill['appears_in'][0]:
						img = "data:image/png;base64," + s['org']['logo'].decode('utf-8')
						html += '''
										<div class="col-sm-6">
											<span style="display:inline;">
												<a href="/jobs/'''+s['id']+'''">
													<img src="'''+img+'''" width="25" height="25" />
													'''+s['org']['name']+''' -
													'''+s['title']+'''
												</a>
											</span>
										</div>
									'''
					html += '</div>'
				if len(skill['appears_in'][1]) > 0:
					html += '<div class="row"><div class="col-sm-12"><h6>Education</h6></div></div><div class="row">'
					for s in skill['appears_in'][1]:
						img = "data:image/png;base64," + s['org']['logo'].decode('utf-8')
						html += '''
										<div class="col-sm-6">
											<span style="display:inline;">
												<a href="/edus/'''+s['id']+'''">
													<img src="'''+img+'''" width="25" height="25" />
													'''+s['org']['name']+''' -
													'''+s['degree']+'''
												</a>
											</span>
										</div>
									'''
					html += '</div>'
			html += '''
												</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</div>
					'''
		return html

	def render_header(self, name, user, page, redirect, s):
		if not s['mobile']:
			html = 	'''
						<nav class="navbar navbar-expand navbar-dark bg-dark">
							<div style="padding-left:10px;">
								<a class="navbar-brand" href="/">
									<img src="/static/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
									<span style='position:relative;left:5px;'>'''+name+'''</span>
								</a>
							</div>
							<div class="collapse navbar-collapse">
								<ul class="navbar-nav mr-auto">'''
			if page == '/':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/">One-Pager
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/">One-Pager</a>
										</li>'''
			if page == '/jobs':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/jobs">Jobs
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/jobs">Jobs</a>
										</li>'''
			if page == '/edus':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/edus">Education
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/edus">Education</a>
										</li>'''
			if page == '/skills':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/skills">Skills
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/skills">Skills</a>
										</li>'''
			if page == '/orgs':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/orgs">Organizations
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/orgs">Organizations</a>
										</li>'''
			if page == '/about':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/about">About
											<span class="sr-only">(current)</span></a>
										</li>'''
			else:
				html += 			'''<li class="nav-item">
											<a class="nav-link" href="/about">About</a>
										</li>'''

			html += '''
								</ul>
								<div style="position:absolute;width:15%;left:84%;">
									<ul class="navbar-nav mr-auto">
										<li class="nav-item dropdown">
											<a class="nav-link dropdown-toggle" href="#" id="dropdown03" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Welcome, ''' + user + '''</a>
											<div class="dropdown-menu", aria-labelledby="dropdown03">
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#loginModal">Login</a>'''
			if s['auth_key'] == self.auth_keys['Contributors'] or s['auth_key'] == self.auth_keys['Owners']:
				html +=						'''<a class="dropdown-item" href="/logout?r='''+redirect.replace('/','_')+'''">Logout</a>'''
			html += '''
											</div>
										</li>
									</ul>
								</div>
							</div>
						</nav>
					'''
		else:
			html = 	'''
						<div class="w3-sidebar w3-bar-block" style="display:none" id="sidebar">
						  <button onclick="sidebar_close()">Close &times;</button>
						  <a href="#" class="w3-bar-item w3-button">Link 1</a>
						  <a href="#" class="w3-bar-item w3-button">Link 2</a>
						  <a href="#" class="w3-bar-item w3-button">Link 3</a>
						</div>

						<nav class="navbar navbar-expand navbar-dark bg-dark">

							<div style="padding-left:10px;">
								<div class="row">

									<img src="/static/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">'''
			if page == '/':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">Home</a>'''
			elif page == '/jobs':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">Jobs</a>'''
			elif page == '/edus':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">Education</a>'''
			elif page == '/skills':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">Skills</a>'''
			elif page == '/orgs':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">Organizations</a>'''
			elif page == '/about':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;">About</a>'''

			html += '''				<div class="dropdown-menu", aria-labelledby="dropdown04">
									'''
			if page == '/':
				html += '''				<a class="dropdown-item" href="/" style="background-color:#add8e6">Home</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/">Home</a>'''
			if page == '/jobs':
				html += '''				<a class="dropdown-item" href="/jobs" style="background-color:#add8e6">Jobs</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/jobs">Jobs</a>'''
			if page == '/edus':
				html += '''				<a class="dropdown-item" href="/edus" style="background-color:#add8e6">Education</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/edus">Education</a>'''
			if page == '/skills':
				html += '''				<a class="dropdown-item" href="/skills" style="background-color:#add8e6">Skills</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/skills">Skills</a>'''
			if page == '/orgs':
				html += '''				<a class="dropdown-item" href="/orgs" style="background-color:#add8e6">Organizations</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/orgs">Organizations</a>'''
			if page == '/about':
				html += '''				<a class="dropdown-item" href="/about" style="background-color:#add8e6">About</a>'''
			else:
				html += '''				<a class="dropdown-item" href="/about">About</a>'''


			html += '''
									</div>
									<div style="position:absolute;width:35%;left:62%;">
										<ul class="navbar-nav mr-auto" style="width:100%;">
											<li class="nav-item dropdown" style="width:100%;">
												<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown03" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">Welcome, ''' + user + '''</a>
												<div class="dropdown-menu", aria-labelledby="dropdown03">
													<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#loginModal">Login</a>'''
			if s['auth_key'] == self.auth_keys['Contributors'] or s['auth_key'] == self.auth_keys['Owners']:
				html +=						'''<a class="dropdown-item" href="/logout?r='''+redirect.replace('/','_')+'''">Logout</a>'''
			html += '''
												</div>
											</li>
										</ul>
									</div>
								</div>
							</div>
						</nav>
					'''

		return html

	def render_html_head(self, redirect, mobile):
		now = datetime.datetime.now()
		if not mobile:
			html = '''
				<html style="margin:0; max-width:100vw; overflow-x:hidden;">
					<head>
						<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
						<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
						<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
						<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
						<script src="/static/js/lib.js"></script>
						<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
						<link rel="stylesheet" href="/static/css/lib.css">
					</head>
					<body style="margin:0; max-width:100vw; overflow-x:hidden;">
						<div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="loginModalLabel" aria-hidden="true" style="position:fixed; top:20%; width:20%; left:40%;">
						  <div class="modal-dialog" role="document">
						    <div class="modal-content">
						      <div class="modal-header">
						        <h5 class="modal-title" id="loginModalLabel">Login</h5>

						        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
						          <span aria-hidden="true">&times;</span>
						        </button>
						      </div>
							  <form action='/login' method='post'>
							      <div class="modal-body">
								  			<a href="#" style="padding-left:25px;color:black" data-toggle="tooltip" title="Go ahead and log in as a member to make changes to content (don't worry, the content can be reset)">What's this?</a><br><br>
										<div class="row">
											<div class="col-sm-10 mx-auto">
												<input type="text" name="username" id="username" value="member"></input><br><br>
											</div>
										</div>
										<div class="row">
											<div class="col-sm-10 mx-auto">
												<input type="password" name="password" id="password" value="member"></input>
											</div>
										</div>
										<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
										<div class="row">
											<div class="col-sm-10 mx-auto">
												<input type="submit" value="Submit" style="display:none">
											</div>
										</div>
							      </div>
							      <div class="modal-footer">
							        <input type="submit" class="btn btn-primary" value="Submit"></button>
							      </div>
							   </form>
						    </div>
						  </div>
						</div>

						<div class="modal fade" id="addJobModal" tabindex="-1" role="dialog" aria-labelledby="addJobModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%;" >
						  <div class="modal-dialog" role="document">
							<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
							  <div class="modal-header">
								<h5 class="modal-title" id="addJobModal">New Work Experience</h5>

								<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
								  <span aria-hidden="true">&times;</span>
								</button>
							  </div>
							  <form action='/create/job' method='post' id="create_job">
								  <div class="modal-body">
										<div class="row">
											<div class="col-sm-6 mx-auto">
												<label for="title">Title</label><br>
												<input id="title" type="text" name="title" placeholder="Job title"></input><br><br>
											</div>
											<div class="col-sm-6 mx-auto">
												<label for="present">Present Job</label><br>
												<input id="present" type="checkbox" name="present" ></input><br><br>
											</div>
										</div>
										<div class="row">
											<div class="col-sm-6">
												<label for="date_start">Start Date</label><br>
												<input id="date_start" type="date" name="date_start" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
											</div>
											<div class="col-sm-6">
												<label for="date_stop">Stop Date</label><br>
												<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
											</div>
										</div>

										<div class="row">
											<div class="col-sm-6 mx-auto">
												<label for="desc_short">Short Description</label><br>
												<textarea name="desc_short" form="create_job" placeholder="Short description of job." style="width:95%;height:100px;"></textarea>
											</div>
											<div class="col-sm-6 mx-auto">
												<label for="desc_long">Long Description</label><br>
												<textarea name="desc_long" form="create_job" placeholder="Long description of job." style="width:95%;height:100px;"></textarea>
											</div>
										</div><br>
										<div class="row">
											<div class="col-sm-6 mx-auto">
												<label for="skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label><br>'''
			all_skills = self.skills_for_add_query()
			html += '''								<select style="min-width:80%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="'''+s['id']+'''">'''+s['name']+'''</option>'''
			html+= '''								</select>
												</div>


													<div class="col-sm-6 mx-auto">
														<label for="org_select">Select Organization</label><br>'''
			all_orgs = self.orgs_for_add_query()
			html += '''									<select style="min-width:80%;" size="6" id="org_selector" name="org_selector">'''
			for o in all_orgs:
				html += '''									<option value="'''+o['id']+'''">'''+o['name']+'''</option>'''
			html += '''									</select>
													</div>
											</div>
											<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
									  </div>
									  <div class="modal-footer">
										<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
										  <span aria-hidden="true">Cancel</span>
										</button>
										<input type="submit" class="btn btn-primary" value="Save & Exit"></button>
									  </div>
								   </form>
								</div>
							  </div>
							</div>


							<div class="modal fade" id="addEduModal" tabindex="-1" role="dialog" aria-labelledby="addJobModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%;" >
							  <div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
								  <div class="modal-header">
									<h5 class="modal-title" id="addJobModal">New Education</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/create/edu' method='post' id="create_edu">
									  <div class="modal-body">
											<div class="row">
												<div class="col-sm-4 mx-auto">
													<label for="title">Degree</label><br>
													<input id="title" type="text" name="degree" placeholder="Degree"></input>
												</div>
												<div class="col-sm-4">
													<label for="title">GPA</label><br>
													<input id="title" type="text" name="gpa" placeholder="GPA"></input>
												</div>
												<div class="col-sm-4">
													<label for="date_stop">Graduation Date</label><br>
													<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''"></input>
												</div>
											</div><br>

											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="desc_short">Short Description</label><br>
													<textarea name="desc_short" form="create_edu" placeholder="Short description of education." style="width:95%;height:100px;"></textarea>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="desc_long">Long Description</label><br>
													<textarea name="desc_long" form="create_edu" placeholder="Long description of education." style="width:95%;height:100px;"></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label><br>'''
			all_skills = self.skills_for_add_query()
			html += '''								<select style="min-width:80%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="'''+s['id']+'''">'''+s['name']+'''</option>'''
			html+= '''								</select>
												</div>


													<div class="col-sm-6 mx-auto">
														<label for="org_select">Select Organization</label><br>'''
			all_orgs = self.orgs_for_add_query()
			html += '''									<select style="min-width:80%;" size="6" id="org_selector" name="org_selector">'''
			for o in all_orgs:
				html += '''									<option value="'''+o['id']+'''">'''+o['name']+'''</option>'''
			html += '''									</select>
														</div>
												</div>
												<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
												<div class="row">
													<div class="col-sm-10 mx-auto">
														<input type="submit" value="Submit" style="display:none">
													</div>
												</div>
										  </div>
										  <div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Exit"></button>
										  </div>
									   </form>
									</div>
								  </div>
								</div>
					'''
		else:
			html = '''
					<html style="margin:0; max-width:100vw; overflow-x:hidden;">
						<head>
							<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
							<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
							<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
							<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
							<script src="/static/js/lib.js"></script>
							<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
						</head>
						<body style="margin:0; max-width:100vw; overflow-x:hidden;">
							<div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelledby="loginModalLabel" aria-hidden="true" style="position:fixed; top:20%; width:80%; left:10%;">
							  <div class="modal-dialog" role="document">
							    <div class="modal-content">
							      <div class="modal-header">
							        <h5 class="modal-title" id="loginModalLabel">Login</h5>

							        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          <span aria-hidden="true">&times;</span>
							        </button>
							      </div>
								  <form action='/login' method='post'>
								      <div class="modal-body">
									  			<p>Go ahead and log in as a member to make changes to content (don't worry, the content can be reset).</p>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="text" name="username" id="username" value="member"></input><br><br>
												</div>
											</div>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="password" name="password" id="password" value="member"></input>
												</div>
											</div>
											<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
								      </div>
								      <div class="modal-footer">
								        <input type="submit" class="btn btn-primary" value="Submit"></button>
								      </div>
								   </form>
							    </div>
							  </div>
							</div>


							<div class="modal fade" id="addJobModal" tabindex="-1" role="dialog" aria-labelledby="addJobModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;">
							  <div class="modal-dialog" role="document">
							    <div class="modal-content">
							      <div class="modal-header">
							        <h5 class="modal-title" id="addJobModal">New Work Experience</h5>

							        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          <span aria-hidden="true">&times;</span>
							        </button>
							      </div>
								  <form action='/create/job' method='post' id="create_job">
								      <div class="modal-body">
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="title">Title</label><br>
													<input id="title" type="text" name="title" placeholder="Job title"></input><br><br>
												</div>
											</div>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="present">Present Job</label><br>
													<input id="present" type="checkbox" name="present" ></input><br><br>
												</div>
											</div>
											<div class="row">
												<div class="col-sm-6">
													<label for="date_start">Start Date</label><br>
													<input id="date_start" type="date" name="date_start" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
												</div>
												<div class="col-sm-6">
													<label for="date_stop">Stop Date</label><br>
													<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
												</div>
											</div>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="desc_short">Short Description</label><br>
													<textarea name="desc_short" form="create_job" placeholder="Short description of job."></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="desc_long">Long Description</label><br>
													<textarea name="desc_long" form="create_job" placeholder="Long description of job."></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="skill_selector">Select Skills</label><br>'''
			all_skills = self.skills_for_add_query()
			html += '''								<select "style=width:100%;" size="'''+str(len(all_skills))+'''" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="'''+s['id']+'''">'''+s['name']+'''</option>'''
			html+= '''								</select>
												</div>
											</div><br>
											<div class="row">
													<div class="col-sm-12 mx-auto">
														<label for="org_select">Select Organization</label><br>'''
			all_orgs = self.orgs_for_add_query()
			html += '''									<select "style=width:100%;" size="'''+str(len(all_orgs))+'''" id="org_selector" name="org_selector">'''
			for o in all_orgs:
				html += '''									<option value="'''+o['id']+'''">'''+o['name']+'''</option>'''
			html += '''									</select>
													</div>
											</div>
											<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
								      </div>
								      <div class="modal-footer">
									  	<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
								          <span aria-hidden="true">Cancel</span>
								        </button>
								        <input type="submit" class="btn btn-primary" value="Save & Exit"></button>
								      </div>
								   </form>
							    </div>
							  </div>
							</div>
						'''
		return html

	def render_about(self, session):
		if not session['mobile']:
			html = '''<div class="jumbotron">
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card">
										<div class="card-header">
											<h2>About</h2>
										</div>
										<div class="card-body">
											<div class="row">
												<div class="col-sm-2">
													<img src="/static/logo.png" width="100" height="100" style="position:relative;left:25px;"/>
												</div>
												<div class="col-sm-9">
														This is a site I have developed myself with the intention of gaining some further
														exposure to several frameworks and technologies, showcase my technical proficiencies,
														and digitize my resume in a palatable manner. Namely, I am looking to start gaining exposure to Jenkins through this project in running a pipeline with a local development environment, an external production server, and a central code repository.<br><br>

														The intention is to make the site fully interactable using psuedo-MVC methodologies and to allow for CRUD operations to be performed on my resume data within the site itself, both by myself and by visitors to the site, with the idea that visitor changes
														can be reverted. It is then the intent to extend this into a full RESTful API.<br><br>

														The site is run on a Flask server with Python and connected to a sqlite storage backend. The front end is served in HTML via Flask and is mostly hard-coded into the Python backend - it uses the Bootstrap CSS library for the majority of styling.<br><br>

														You can access the source for this site <a href="https://github.com/P00ters/resume" target="_blank">here</a>.
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card">
										<div class="card-header">
											<h5>Site Development Roadmap</h5>
										</div>
										<div class="card-body">
											<b>Note:</b> This site is still presently under development, but is in a suitable state to act as a digital copy of my resume.<br><br>
											<div class="row" style="padding-left:15px;">
												<p style="text-decoration:line-through;">Develop models for housing resume data in SQL.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p style="text-decoration:line-through;">Develop method for insertion of pre-existing resume data into data store.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p style="text-decoration:line-through;">Develop view controllers for the main resume data areas (single page resume, jobs, education, skills, organizations).</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Complete population of pre-existing resume data into data store for any missing data.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<p style="text-decoration:line-through;">Add all hard skills.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<p style="text-decoration:line-through;">Add all soft skills.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<p>Add skill commentary.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<p>Add long descriptions to education and work experience.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Circle back on implementation of custom 404 pages and error handling on queries on non-existant data.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p style="text-decoration:line-through;">Extend compatibility by implementing independent view controllers for mobile platforms.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Implement Jenkins pipelines for new feature additions once base functions are established.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Implement controllers for data integrity - allow for reversion to actual resume data when present state is altered by a guest.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Extend the application into a full RESTful API to GET any resume data via JSON.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Extend the application into a full RESTful API to perform any of the other CRUD operations on the resume data.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					'''
		else:
			html = '''<div class="jumbotron">
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card">
										<div class="card-header">
											<h2>About</h2>
										</div>
										<div class="card-body">
											<div class="row">
												<div class="col-sm-3">
													<img src="/static/logo.png" width="100" height="100" style="position:relative;left:25px;"/>
												</div>
												<div class="col-sm-9">
														This is a site I have developed myself with the intention of gaining some further
														exposure to several frameworks and technologies, showcase my technical proficiencies,
														and digitize my resume in a palatable manner. Namely, I am looking to start gaining exposure to Jenkins through this project in running a pipeline with a local development environment, an external production server, and a central code repository.<br><br>

														The intention is to make the site fully interactable using psuedo-MVC methodologies and to allow for CRUD operations to be performed on my resume data within the site itself, both by myself and by visitors to the site, with the idea that visitor changes
														can be reverted. It is then the intent to extend this into a full RESTful API.<br><br>

														The site is run on a Flask server with Python and connected to a sqlite storage backend. The front end is served in HTML via Flask and is mostly hard-coded into the Python backend - it uses the Bootstrap CSS library for the majority of styling.<br><br>

														You can access the source for this site <a href="https://github.com/P00ters/resume" target="_blank">here</a>.
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card">
										<div class="card-header">
											<h5>Site Development Roadmap</h5>
										</div>
										<div class="card-body">
											<b>Note:</b> This site is still presently under development, but is in a suitable state to act as a digital copy of my resume.<br><br>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Develop models for housing resume data in SQL.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Develop method for insertion of pre-existing resume data into data store.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Develop view controllers for the main resume data areas (single page resume, jobs, education, skills, organizations).</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Complete population of pre-existing resume data into data store for any missing data.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Add all hard skills.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Add all soft skills.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
												<div class="col-sm-8">
													<p>Add skill commentary.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Add long descriptions to education and work experience.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Circle back on implementation of custom 404 pages and error handling on queries on non-existant data.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Extend compatibility by implementing independent view controllers for mobile platforms.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
												<div class="col-sm-8">
													<p>Implement Jenkins pipelines for new feature additions once base functions are established.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-warning">Up Next</span>
												</div>
												<div class="col-sm-8">
													<p>Implement controllers for data integrity - allow for reversion to actual resume data when present state is altered by a guest.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
												<div class="col-sm-8">
													<p>Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
												<div class="col-sm-8">
													<p>Extend the application into a full RESTful API to GET any resume data via JSON.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-danger">Pending</span>
												</div>
												<div class="col-sm-8">
													<p>Extend the application into a full RESTful API to perform any of the other CRUD operations on the resume data.</p>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					'''

		return html

	"""
		Helper Conversion Methods
	"""

	def telelink (self, phone):
		return "tel:+1" + phone

	def teleformat (self, phone):
		return '(' + phone[:3] + ') ' + phone[3:6] + '-' + phone[6:10]

	def addresslines (self, address):
		a = address.split(',')
		c = ""
		for b in a:
			c += b + '<br>'
		return c

	def datereformat (self, date):
		d = datetime.datetime.strptime(date, '%m/%d/%Y')
		return d.strftime('%b %Y')
