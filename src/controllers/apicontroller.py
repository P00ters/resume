import sys
sys.path.append('../')
sys.path.append('../models')


from accounts import Account, NoneAccount, retrieve_all_accounts, retrieve_accounts_fcustom
from jobs import Job, retrieve_all_jobs, retrieve_jobs, retrieve_jobs_fcustom, NoneJob
from orgs import Org, retrieve_all_orgs, retrieve_orgs, retrieve_orgs_fcustom, NoneOrg
from groups import Group, retrieve_all_groups, retrieve_groups_fcustom, NoneGroup
from educations import Education, retrieve_all_educations, retrieve_educations, retrieve_educations_fcustom
from skills import Skill, retrieve_all_skills, retrieve_skills_fcustom
from addresses import NoneAddress, Address, retrieve_all_addresses, retrieve_addresses, retrieve_addresses_fcustom
from contacts import Contact, retrieve_all_contacts, retrieve_contacts_fcustom
from dbm import DBM

import json

class APIController:
	def __init__ (self, dbm):
		self.dbm = dbm

	def parse(self, method, model, args, comparator):
		if method.lower() == 'get':
			if model.lower() == 'addresses':
				return self.get_address(method, model, args, comparator)

			elif model.lower() == 'orgs':
				return self.get_orgs(method, model, args, comparator)

			elif model.lower() == 'jobs':
				return self.get_jobs(method, model, args, comparator)

			elif model.lower() == 'edus':
				return self.get_edus(method, model, args, comparator)

			elif model.lower() == 'skills':
				return self.get_skills(method, model, args, comparator)

			else:
				return self.get_error(method, model, args, 'Invalid model.')
		else:
			return self.get_error(method, model, args, 'Invalid method.')

	def get_address	(self, method, model, args, comparator):
		aid = args.get('id')
		aname = args.get('name')
		auri = args.get('uri')

		result = 	{
						'response': {
							'code': 200,
							'message': 'OK',
							'method': method,
							'model': model,
							'args': str(args)
						},
						'addresses': []
					}

		if aid == None and aname == None and auri == None:
			all_addresses = retrieve_all_addresses(self.dbm)
			for a in all_addresses:
				result['addresses'].append(a.dict())
		else:
			query = "SELECT * FROM Addresses WHERE "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if auri != None:
				if comparator == "=":
					query += "Addresses.uri" + comparator + "'" + auri + "';"
				else:
					query += "Addresses.uri" + comparator + "'%" + auri + "%';"

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			print(query)
			addresses = retrieve_addresses_fcustom(self.dbm, query)
			for a in addresses:
				result['addresses'].append(a.dict())

		return json.dumps(result, indent=2)

	def get_orgs (self, method, model, args, comparator):
		oid = args.get('id')
		oname = args.get('name')
		aid = args.get('aid')
		aname = args.get('aname')
		phone = args.get('phone')
		desc_short = args.get('desc_short')
		website = args.get('website')

		result = {
					'response': {
						'code': 200,
						'message': 'OK',
						'method': method,
						'model': model,
						'args': str(args)
					},
					'orgs': []
				}

		if oid == None and oname == None and aid == None and aname == None and phone == None and desc_short == None and website == None:
			all_orgs = retrieve_all_orgs(self.dbm)
			for o in all_orgs:
				result['orgs'].append(o.dict())
		else:
			query = "SELECT Orgs.id, Orgs.name, Orgs.address, Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by, Orgs.modified_by, Addresses.id, Addresses.name FROM Orgs, Addresses WHERE Orgs.address=Addresses.id AND "

			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname  + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname  + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if phone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + phone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + phone + "%' AND "
			if desc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + desc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + desc_short + "%' AND "
			if website != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + website + "';"
				else:
					query += "Orgs.website" + comparator + "'%" + website + "%';"

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			print(query)

			orgs = retrieve_orgs_fcustom(self.dbm, query)
			for o in orgs:
				result['orgs'].append(o.dict())

		return json.dumps(result, indent=2)

	def get_jobs (self, method, model, args, comparator):
		jid = args.get('id')
		jtitle = args.get('title')
		jpresent = args.get('present')
		jdate_start = args.get('date_start')
		jdate_stop = args.get('date_stop')
		jdesc_short = args.get('desc_short')
		jdesc_long = args.get('desc_long')
		jskill_ids = args.get('skill_ids')
		oid = args.get('oid')
		oname = args.get('oname')
		aid = args.get('aid')
		aname = args.get('aname')
		ophone = args.get('ophone')
		odesc_short = args.get('odesc_short')
		owebsite = args.get('owebsite')

		result = 	{
						'response': {
							'code': 200,
							'message': 'OK',
							'method': method,
							'model': model,
							'args': str(args)
						},
						'jobs': []
					}

		if jid == None and jtitle == None and jpresent == None and jdate_start == None and jdate_stop == None and jdesc_short == None and jdesc_long == None and jskill_ids == None and oid == None and oname == None and aid == None and aname == None and ophone == None and odesc_short == None and owebsite == None:
			all_jobs = retrieve_all_jobs(self.dbm)
			for j in all_jobs:
				result['jobs'].append(j.dict())
		else:
			query = "SELECT Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Jobs.org, Jobs.created_by, Jobs.modified_by, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Orgs.phone, Orgs.desc_short, Orgs.website FROM Jobs, Orgs, Addresses WHERE Jobs.org = Orgs.id AND Orgs.address = Addresses.id AND "

			if jid != None:
				if comparator == "=":
					query += "Jobs.id" + comparator + "'" + jid + "' AND "
				else:
					query += "Jobs.id" + comparator + "'%" + jid + "%' AND "
			if jtitle != None:
				if comparator == "=":
					query += "Jobs.title" + comparator + "'" + jtitle + "' AND "
				else:
					query += "Jobs.title" + comparator + "'%" + jtitle + "%' AND "
			if jpresent != None:
				if comparator == "=":
					query += "Jobs.present" + comparator + "'" + jpresent + "' AND "
				else:
					query += "Jobs.present" + comparator + "'%" + jpresent + "%' AND "
			if jdate_start != None:
				if comparator == "=":
					query += "Jobs.date_start" + comparator + "'" + jdate_start + "' AND "
				else:
					query += "Jobs.date_start" + comparator + "'%" + jdate_start + "%' AND "
			if jdate_stop != None:
				if comparator == "=":
					query += "Jobs.date_stop" + comparator + "'" + jdate_stop + "' AND "
				else:
					query += "Jobs.date_stop" + comparator + "'%" + jdate_stop + "%' AND "
			if jdesc_short != None:
				if comparator == "=":
					query += "Jobs.desc_short" + comparator + "'" + jdesc_short + "' AND "
				else:
					query += "Jobs.desc_short" + comparator + "'%" + jdesc_short + "%' AND "
			if jdesc_long != None:
				if comparator == "=":
					query += "Jobs.desc_long" + comparator + "'" + jdesc_long + "' AND "
				else:
					query += "Jobs.desc_long" + comparator + "'%" + jdesc_long + "%' AND "
			if jskill_ids != None:
				if comparator == "=":
					query += "Jobs.skill_ids" + comparator + "'" + jskill_ids + "' AND "
				else:
					query += "Jobs.skill_ids" + comparator + "'%" + jskill_ids + "%' AND "
			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname  + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname  + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if ophone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + ophone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + ophone + "%' AND "
			if odesc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + odesc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + odesc_short + "%' AND "
			if owebsite != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + owebsite + "';"
				else:
					query += "Orgs.website" + comparator + "'%" + owebsite + "%';"
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			jobs = retrieve_jobs_fcustom(self.dbm, query)
			for j in jobs:
				result['jobs'].append(j.dict())

		return json.dumps(result, indent=2)

	def get_edus (self, method, model, args, comparator):
		eid = args.get('id')
		edegree = args.get('degree')
		egpa = args.get('gpa')
		edate_stop = args.get('date_stop')
		edesc_short = args.get('desc_short')
		edesc_long = args.get('desc_long')
		eskill_ids = args.get('skill_ids')
		oid = args.get('oid')
		oname = args.get('oname')
		aid = args.get('aid')
		aname = args.get('aname')
		ophone = args.get('ophone')
		odesc_short = args.get('odesc_short')
		owebsite = args.get('owebsite')

		result = 	{
						'response': {
							'code': 200,
							'message': 'OK',
							'method': method,
							'model': model,
							'args': str(args)
						},
						'edus': []
					}

		if eid == None and edegree == None and edate_stop == None and edesc_short == None and edesc_long == None and eskill_ids == None and oid == None and oname == None and aid == None and aname == None and ophone == None and odesc_short == None and owebsite == None:
			all_edus = retrieve_all_educations(self.dbm)
			for e in all_edus:
				result['edus'].append(e.dict())
		else:
			query = "SELECT Education.id, Education.degree, Education.gpa, Education.skill_ids, Education.date_stop, Education.desc_short, Education.desc_long, Education.org, Education.created_by, Education.modified_by, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Orgs.phone, Orgs.desc_short, Orgs.website FROM Education, Orgs, Addresses WHERE Education.org = Orgs.id AND Orgs.address = Addresses.id AND "
			if eid != None:
				if comparator == "=":
					query += "Education.id" + comparator + "'" + eid + "' AND "
				else:
					query += "Education.id" + comparator + "'%" + eid + "%' AND "
			if edegree != None:
				if comparator == "=":
					query += "Education.degree" + comparator + "'" + edegree + "' AND "
				else:
					query += "Education.degree" + comparator + "'%" + edegree + "%' AND "
			if egpa != None:
				if comparator == "=":
					query += "Education.gpa" + comparator + "'" + egpa + "' AND "
				else:
					query += "Education.gpa" + comparator + "'%" + egpa + "%' AND "
			if edate_stop != None:
				if comparator == "=":
					query += "Education.date_stop" + comparator + "'" + edate_stop + "' AND "
				else:
					query += "Education.date_stop" + comparator + "'%" + edate_stop + "%' AND "
			if edesc_short != None:
				if comparator == "=":
					query += "Education.desc_short" + comparator + "'" + edesc_short + "' AND "
				else:
					query += "Education.desc_short" + comparator + "'%" + edesc_short + "%' AND "
			if edesc_long != None:
				if comparator == "=":
					query += "Education.desc_long" + comparator + "'" + edesc_long + "' AND "
				else:
					query += "Education.desc_long" + comparator + "'%" + edesc_long + "%' AND "
			if eskill_ids != None:
				if comparator == "=":
					query += "Education.skill_ids" + comparator + "'" + eskill_ids + "' AND "
				else:
					query += "Education.skill_ids" + comparator + "'%" + eskill_ids + "%' AND "
			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname + "%' AND "
			if ophone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + ophone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + ophone + "%' AND "
			if odesc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + odesc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + odesc_short + "%' AND "
			if owebsite != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + owebsite + "' AND "
				else:
					query += "Orgs.website" + comparator + "'%" + owebsite + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			edus = retrieve_educations_fcustom(self.dbm, query)
			for e in edus:
				result['edus'].append(e.dict())

		return json.dumps(result, indent=2)

	def get_skills (self, method, model, args, comparator):
		sid = args.get('id')
		sname = args.get('name')
		sexposure = args.get('exposure')
		ssoh = args.get('technical_skill')
		sreference = args.get('reference')
		scategory = args.get('category')
		sdesc_short = args.get('desc_short')
		sdesc_long = args.get('desc_long')

		result = 	{
						'response': {
							'code': 200,
							'message': 'OK',
							'method': method,
							'model': model,
							'args': str(args)
						},
						'skills': []
					}

		if sid == None and sname == None and sexposure == None and ssoh == None and sreference == None and scategory == None and sdesc_short == None and sdesc_long == None:
			ss = retrieve_all_skills(self.dbm)
			for s in ss:
				result['skills'].append(s.dict())
		else:
			query = "SELECT Skills.id, Skills.name, Skills.exposure, Skills.soft_or_hard, Skills.reference, Skills.icon, Skills.category, Skills.desc_short, Skills.desc_long, Skills.created_by, Skills.modified_by FROM Skills WHERE "

			if sid != None:
				if comparator == "=":
					query += "Skills.id" + comparator + "'" + sid + "' AND "
				else:
					query += "Skills.id" + comparator + "'%" + sid + "%' AND "
			if sname != None:
				if comparator == "=":
					query += "Skills.name" + comparator + "'" + sname + "' AND "
				else:
					query += "Skills.name" + comparator + "'%" + sname + "%' AND "
			if sexposure != None:
				if comparator == "=":
					query += "Skills.exposure" + comparator + "'" + sexposure + "' AND "
				else:
					query += "Skills.exposure" + comparator + "'%" + sexposure + "%' AND "
			if ssoh != None:
				if comparator == "=":
					query += "Skills.soft_or_hard" + comparator + "'" + ssoh + "' AND "
				else:
					query += "Skills.soft_or_hard" + comparator + "'%" + ssoh + "%' AND "
			if sreference != None:
				if comparator == "=":
					query += "Skills.reference" + comparator + "'" + sreference + "' AND "
				else:
					query += "Skills.reference" + comparator + "'%" + sreference + "%' AND "
			if scategory != None:
				if comparator == "=":
					query += "Skills.category" + comparator + "'" + scategory + "' AND "
				else:
					query += "Skills.category" + comparator + "'%" + scategory + "%' AND "
			if sdesc_short != None:
				if comparator == "=":
					query += "Skills.desc_short" + comparator + "'" + sdesc_short + "' AND "
				else:
					query += "Skills.desc_short" + comparator + "'%" + sdesc_short + "%' AND "
			if sdesc_long != None:
				if comparator == "=":
					query += "Skills.desc_long" + comparator + "'" + sdesc_long + "' AND "
				else:
					query += "Skills.desc_long" + comparator + "'%" + sdesc_long + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			ss = retrieve_skills_fcustom(self.dbm, query)
			for s in ss:
				result['skills'].append(s.dict())

		return json.dumps(result, indent=2)

	def get_error (self, method, model, args, message):

		error = {
					'response': {
						'code': 500,
						'message': message,
						'method': method,
						'model': model,
						'args': str(args)
					}
				}
		return json.dumps(error, indent=2)

	def v2 (self, method, model, args, message):
		if method.lower() == 'post':
			if model.lower() == 'auth':
				return self.post_auth(method, model, args, message)
			else:
				return self.get_error(method, model, args, 'Invalid model.'), 400
		elif method.lower() == 'get':
			dbm_reader = DBM(self.dbm.db_path, self.dbm.init)
			if model.lower() == 'addresses':
				return self.get_addresses_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'accounts':
				return self.get_accounts_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'groups':
				return self.get_groups_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'orgs':
				return self.get_orgs_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'edus':
				return self.get_edus_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'jobs':
				return self.get_jobs_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'skills':
				return self.get_skills_v2(dbm_reader, method, model, args, message)
			elif model.lower() == 'contacts':
				return self.get_contacts_v2(dbm_reader, method, model, args, message)
			else:
				return self.get_error(method, model, args, 'Invalid model.'), 400
		elif method.lower() == 'put':
			dbm_writer = DBM(self.dbm.db_path, self.dbm.init)
			if model.lower() == 'accounts':
				return self.put_accounts_v2(dbm_writer, method, model, args, message)
			elif model.lower() == 'addresses':
				return self.put_addresses_v2(dbm_writer, method, model, args, message)
			elif model.lower() == 'orgs':
				return self.put_orgs_v2(dbm_writer, method, model, args, message)
			elif model.lower() == 'jobs':
				return self.put_jobs_v2(dbm_writer, method, model, args, message)
			else:
				return self.get_error(method, model, args, 'Invalid model.'), 400
		else:
			return self.get_error(method, model, args, 'Invalid method.'), 400

	def get_contacts_v2 (self, db, method, model, args, comparator):
		cid = args.get('id')
		cname = args.get('name')
		cphone1 = args.get('phone1')
		cphone2 = args.get('phone2')
		cemail = args.get('email')
		cobjective = args.get('objective')
		ccreated_by = args.get('created_by')
		cmodified_by = args.get('modified_by')
		aid = args.get('aid')
		aname = args.get('aname')


		result = []
		if cid == None and cname == None and cphone1 == None and cphone2 == None and cemail == None and cobjective == None and ccreated_by == None and cmodified_by == None and aid == None and aname == None:
			contacts = retrieve_all_contacts(db)
			for c in contacts:
				result.append(c.dict())
		else:
			query = "SELECT Contact.id, Contact.name, Addresses.id, Contact.phone1, Contact.phone2, Contact.email, Contact.objective, Contact.created_by, Contact.modified_by FROM Contact, Addresses WHERE Contact.address = Addresses.id AND "

			if cid != None:
				if comparator == "=":
					query += "Contact.id" + comparator + "'" + cid + "' AND "
				else:
					query += "Contact.id" + comparator + "'%" + cid + "%' AND "
			if cname != None:
				if comparator == "=":
					query += "Contact.name" + comparator + "'" + cname + "' AND "
				else:
					query += "Contact.name" + comparator + "'%" + cname + "%' AND "
			if cphone1 != None:
				if comparator == "=":
					query += "Contact.phone1" + comparator + "'" + cphone1 + "' AND "
				else:
					query += "Contact.phone1" + comparator + "'%" + cphone1 + "%' AND "
			if cphone2 != None:
				if comparator == "=":
					query += "Contact.phone2" + comparator + "'" + cphone2 + "' AND "
				else:
					query += "Contact.phone2" + comparator + "'%" + cphone2 + "%' AND "
			if cemail != None:
				if comparator == "=":
					query += "Contact.email" + comparator + "'" + cemail + "' AND "
				else:
					query += "Contact.email" + comparator + "'%" + cemail + "%' AND "
			if cobjective != None:
				if comparator == "=":
					query += "Contact.objective" + comparator + "'" + cobjective + "' AND "
				else:
					query += "Contact.objective" + comparator + "'%" + cobjective + "%' AND "
			if ccreated_by != None:
				if comparator == "=":
					query += "Contact.created_by" + comparator + "'" + ccreated_by + "' AND "
				else:
					query += "Contact.created_by" + comparator + "'%" + ccreated_by + "%' AND "
			if cmodified_by != None:
				if comparator == "=":
					query += "Contact.modified_by" + comparator + "'" + cmodified_by + "' AND "
				else:
					query += "Contact.modified_by" + comparator + "'%" + cmodified_by + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			contacts = retrieve_contacts_fcustom(db, query)
			for c in contacts:
				result.append(c.dict())

		db.close()
		return result

	def get_skills_v2 (self, db, method, model, args, comparator):
		sid = args.get('id')
		sname = args.get('name')
		sexposure = args.get('exposure')
		ssoh = args.get('technical_skill')
		sreference = args.get('reference')
		scategory = args.get('category')
		sdesc_short = args.get('desc_short')
		sdesc_long = args.get('desc_long')

		result = []

		if sid == None and sname == None and sexposure == None and ssoh == None and sreference == None and scategory == None and sdesc_short == None and sdesc_long == None:
			ss = retrieve_all_skills(db)
			for s in ss:
				result.append(s.dict())
		else:
			query = "SELECT Skills.id, Skills.name, Skills.exposure, Skills.soft_or_hard, Skills.reference, Skills.icon, Skills.category, Skills.desc_short, Skills.desc_long, Skills.created_by, Skills.modified_by FROM Skills WHERE "

			if sid != None:
				if comparator == "=":
					query += "Skills.id" + comparator + "'" + sid + "' AND "
				else:
					query += "Skills.id" + comparator + "'%" + sid + "%' AND "
			if sname != None:
				if comparator == "=":
					query += "Skills.name" + comparator + "'" + sname + "' AND "
				else:
					query += "Skills.name" + comparator + "'%" + sname + "%' AND "
			if sexposure != None:
				if comparator == "=":
					query += "Skills.exposure" + comparator + "'" + sexposure + "' AND "
				else:
					query += "Skills.exposure" + comparator + "'%" + sexposure + "%' AND "
			if ssoh != None:
				if comparator == "=":
					query += "Skills.soft_or_hard" + comparator + "'" + ssoh + "' AND "
				else:
					query += "Skills.soft_or_hard" + comparator + "'%" + ssoh + "%' AND "
			if sreference != None:
				if comparator == "=":
					query += "Skills.reference" + comparator + "'" + sreference + "' AND "
				else:
					query += "Skills.reference" + comparator + "'%" + sreference + "%' AND "
			if scategory != None:
				if comparator == "=":
					query += "Skills.category" + comparator + "'" + scategory + "' AND "
				else:
					query += "Skills.category" + comparator + "'%" + scategory + "%' AND "
			if sdesc_short != None:
				if comparator == "=":
					query += "Skills.desc_short" + comparator + "'" + sdesc_short + "' AND "
				else:
					query += "Skills.desc_short" + comparator + "'%" + sdesc_short + "%' AND "
			if sdesc_long != None:
				if comparator == "=":
					query += "Skills.desc_long" + comparator + "'" + sdesc_long + "' AND "
				else:
					query += "Skills.desc_long" + comparator + "'%" + sdesc_long + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			ss = retrieve_skills_fcustom(db, query)
			for s in ss:
				result.append(s.dict())

		db.close()
		return result

	def get_jobs_v2 (self, db, method, model, args, comparator):
		jid = args.get('id')
		jtitle = args.get('title')
		jpresent = args.get('present')
		jdate_start = args.get('date_start')
		jdate_stop = args.get('date_stop')
		jdesc_short = args.get('desc_short')
		jdesc_long = args.get('desc_long')
		jskill_ids = args.get('skill_ids')
		oid = args.get('oid')
		oname = args.get('oname')
		aid = args.get('aid')
		aname = args.get('aname')
		ophone = args.get('ophone')
		odesc_short = args.get('odesc_short')
		owebsite = args.get('owebsite')

		result = []

		if jid == None and jtitle == None and jpresent == None and jdate_start == None and jdate_stop == None and jdesc_short == None and jdesc_long == None and jskill_ids == None and oid == None and oname == None and aid == None and aname == None and ophone == None and odesc_short == None and owebsite == None:
			all_jobs = retrieve_all_jobs(db)
			for j in all_jobs:
				result.append(j.dict())
		else:
			query = "SELECT Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Jobs.org, Jobs.created_by, Jobs.modified_by, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Orgs.phone, Orgs.desc_short, Orgs.website FROM Jobs, Orgs, Addresses WHERE Jobs.org = Orgs.id AND Orgs.address = Addresses.id AND "

			if jid != None:
				if comparator == "=":
					query += "Jobs.id" + comparator + "'" + jid + "' AND "
				else:
					query += "Jobs.id" + comparator + "'%" + jid + "%' AND "
			if jtitle != None:
				if comparator == "=":
					query += "Jobs.title" + comparator + "'" + jtitle + "' AND "
				else:
					query += "Jobs.title" + comparator + "'%" + jtitle + "%' AND "
			if jpresent != None:
				if comparator == "=":
					query += "Jobs.present" + comparator + "'" + jpresent + "' AND "
				else:
					query += "Jobs.present" + comparator + "'%" + jpresent + "%' AND "
			if jdate_start != None:
				if comparator == "=":
					query += "Jobs.date_start" + comparator + "'" + jdate_start + "' AND "
				else:
					query += "Jobs.date_start" + comparator + "'%" + jdate_start + "%' AND "
			if jdate_stop != None:
				if comparator == "=":
					query += "Jobs.date_stop" + comparator + "'" + jdate_stop + "' AND "
				else:
					query += "Jobs.date_stop" + comparator + "'%" + jdate_stop + "%' AND "
			if jdesc_short != None:
				if comparator == "=":
					query += "Jobs.desc_short" + comparator + "'" + jdesc_short + "' AND "
				else:
					query += "Jobs.desc_short" + comparator + "'%" + jdesc_short + "%' AND "
			if jdesc_long != None:
				if comparator == "=":
					query += "Jobs.desc_long" + comparator + "'" + jdesc_long + "' AND "
				else:
					query += "Jobs.desc_long" + comparator + "'%" + jdesc_long + "%' AND "
			if jskill_ids != None:
				if comparator == "=":
					query += "Jobs.skill_ids" + comparator + "'" + jskill_ids + "' AND "
				else:
					query += "Jobs.skill_ids" + comparator + "'%" + jskill_ids + "%' AND "
			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname  + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname  + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if ophone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + ophone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + ophone + "%' AND "
			if odesc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + odesc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + odesc_short + "%' AND "
			if owebsite != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + owebsite + "';"
				else:
					query += "Orgs.website" + comparator + "'%" + owebsite + "%';"
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			jobs = retrieve_jobs_fcustom(db, query)
			for j in jobs:
				result.append(j.dict())

		db.close()
		return result

	def get_edus_v2 (self, db, method, model, args, comparator):
		eid = args.get('id')
		edegree = args.get('degree')
		egpa = args.get('gpa')
		edate_stop = args.get('date_stop')
		edesc_short = args.get('desc_short')
		edesc_long = args.get('desc_long')
		eskill_ids = args.get('skill_ids')
		oid = args.get('oid')
		oname = args.get('oname')
		aid = args.get('aid')
		aname = args.get('aname')
		ophone = args.get('ophone')
		odesc_short = args.get('odesc_short')
		owebsite = args.get('owebsite')

		result = []

		if eid == None and edegree == None and edate_stop == None and edesc_short == None and edesc_long == None and eskill_ids == None and oid == None and oname == None and aid == None and aname == None and ophone == None and odesc_short == None and owebsite == None:
			all_edus = retrieve_all_educations(db)
			for e in all_edus:
				result.append(e.dict())
		else:
			query = "SELECT Education.id, Education.degree, Education.gpa, Education.skill_ids, Education.date_stop, Education.desc_short, Education.desc_long, Education.org, Education.created_by, Education.modified_by, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Orgs.phone, Orgs.desc_short, Orgs.website FROM Education, Orgs, Addresses WHERE Education.org = Orgs.id AND Orgs.address = Addresses.id AND "
			if eid != None:
				if comparator == "=":
					query += "Education.id" + comparator + "'" + eid + "' AND "
				else:
					query += "Education.id" + comparator + "'%" + eid + "%' AND "
			if edegree != None:
				if comparator == "=":
					query += "Education.degree" + comparator + "'" + edegree + "' AND "
				else:
					query += "Education.degree" + comparator + "'%" + edegree + "%' AND "
			if egpa != None:
				if comparator == "=":
					query += "Education.gpa" + comparator + "'" + egpa + "' AND "
				else:
					query += "Education.gpa" + comparator + "'%" + egpa + "%' AND "
			if edate_stop != None:
				if comparator == "=":
					query += "Education.date_stop" + comparator + "'" + edate_stop + "' AND "
				else:
					query += "Education.date_stop" + comparator + "'%" + edate_stop + "%' AND "
			if edesc_short != None:
				if comparator == "=":
					query += "Education.desc_short" + comparator + "'" + edesc_short + "' AND "
				else:
					query += "Education.desc_short" + comparator + "'%" + edesc_short + "%' AND "
			if edesc_long != None:
				if comparator == "=":
					query += "Education.desc_long" + comparator + "'" + edesc_long + "' AND "
				else:
					query += "Education.desc_long" + comparator + "'%" + edesc_long + "%' AND "
			if eskill_ids != None:
				if comparator == "=":
					query += "Education.skill_ids" + comparator + "'" + eskill_ids + "' AND "
				else:
					query += "Education.skill_ids" + comparator + "'%" + eskill_ids + "%' AND "
			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname + "%' AND "
			if ophone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + ophone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + ophone + "%' AND "
			if odesc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + odesc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + odesc_short + "%' AND "
			if owebsite != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + owebsite + "' AND "
				else:
					query += "Orgs.website" + comparator + "'%" + owebsite + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			edus = retrieve_educations_fcustom(db, query)
			for e in edus:
				result.append(e.dict())

		db.close()
		return result

	def get_addresses_v2 (self, db, method, model, args, comparator):
		aid = args.get('id')
		aname = args.get('name')
		auri = args.get('uri')

		result = []

		if aid == None and aname == None and auri == None:
			all_addresses = retrieve_all_addresses(db)
			for a in all_addresses:
				result.append(a.dict())
		else:
			query = "SELECT * FROM Addresses WHERE "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if auri != None:
				if comparator == "=":
					query += "Addresses.uri" + comparator + "'" + auri + "';"
				else:
					query += "Addresses.uri" + comparator + "'%" + auri + "%';"

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			print(query)
			addresses = retrieve_addresses_fcustom(db, query)
			for a in addresses:
				result.append(a.dict())

		db.close()
		return result

	def put_jobs_v2 (self, db, method, model, args, comparator):
		authorizer_g = NoneGroup()
		authorizer_u = NoneAccount()
		if not authorizer_g.retrieve(db, auth_key=args.get('signer')):
			return {'err', 'ag retrieve'}, 404
		else:
			if authorizer_g.name == 'Readers':
				return {'err': 'au level'}, 404
			else:
				if not authorizer_u.retrieve(db, group_id=authorizer_g.id):
					return {'err': 'au retrieve'}, 404
				else:
					id = args.get('id')
					j = NoneJob()
					if not j.retrieve(db, id=id):
						return {'err': 'a.retrieve'}, 404
					else:
						title = args.get('title')
						date_start = args.get('date_start')
						present = args.get('present')
						date_stop = args.get('date_stop')
						desc_short = args.get('desc_short')
						desc_long = args.get('desc_long')
						org = args.get('org')

						if title != None:
							j.title = title
						if date_start != None:
							j.date_start = date_start
						if present != None:
							j.present = present
						if date_stop != None:
							j.date_stop = date_stop
						if desc_short != None:
							j.desc_short = desc_short
						if desc_long != None:
							j.desc_long = desc_long
						if org != None:
							o = NoneOrg()
							if o.retrieve(db, id=org):
								j.org = o

						if title != None or date_start != None or present != None or date_stop != None or desc_short != None or desc_long != None:
							j.modified_by = authorizer_u

						j.update(db)

						if (authorizer_g.name == 'Owners'):
							db2 = DBM(self.db.dp_path + '.bak.sqlite', self.dbm.init)
							j.update(db2)

						return j.dict()


	def put_addresses_v2 (self, db, method, model, args, comparator):
		authorizer_g = NoneGroup()
		authorizer_u = NoneAccount()
		if not authorizer_g.retrieve(db, auth_key=args.get('signer')):
			return {'err', 'ag retrieve'}, 404
		else:
			if authorizer_g.name == 'Readers':
				return {'err': 'au level'}, 404
			else:
				if not authorizer_u.retrieve(db, group_id=authorizer_g.id):
					return {'err': 'au retrieve'}, 404
				else:
					id = args.get('id')
					a = NoneAddress()
					if not a.retrieve(db, id=id):
						return {'err': 'a.retrieve'}, 404
					else:
						name = args.get('name')
						uri = args.get('uri')

						if name != None:
							a.name = name
						if uri != None:
							a.uri = uri

						if name != None or uri != None:
							a.modified_by = authorizer_u

						a.update(db)

						if (authorizer_g.name == 'Owners'):
							db2 = DBM(self.dbm.db_path + '.bak.sqlite', self.dbm.init)
							a.update(db2)

						return a.dict()


	def get_accounts_v2 (self, db, method, model, args, comparator):
		aid = args.get('id')
		aname = args.get('name')
		ausername = args.get('username')
		gname = args.get('gname')
		gid = args.get('gid')

		result = []

		if aid == None and aname == None and ausername == None and gname == None and gid == None:
			all_accounts = retrieve_all_accounts(db)
			for a in all_accounts:
				result.append(a.dict())
		else:
			query = "SELECT Accounts.id, Accounts.username, Accounts.password, Accounts.salt, Accounts.name, Groups.id, Groups.name, Groups.auth_key FROM Accounts, Groups WHERE Accounts.group_id = Groups.id AND "

			if aid != None:
				if comparator == "=":
					query += "Accounts.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Accounts.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Accounts.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Accounts.name" + comparator + "'%" + aname + "%' AND "
			if ausername != None:
				if comparator == "=":
					query += "Accounts.username" + comparator + "'" + ausername + "' AND "
				else:
					query += "Accounts.username" + comparator + "'%" + ausername + "%' AND "
			if gname != None:
				if comparator == "=":
					query += "Groups.name" + comparator + "'" + gname + "' AND "
				else:
					query += "Groups.name" + comparator + "'%" + gname + "%' AND "
			if gid != None:
				if comparator == "=":
					query += "Groups.id" + comparator + "'" + gid + "' AND "
				else:
					query += "Groups.id" + comparator + "'%" + gid + "%' AND "

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			accounts = retrieve_accounts_fcustom(db, query)
			for a in accounts:
				result.append(a.dict())

		db.close()
		return result

	def put_accounts_v2 (self, db, method, model, args, comparator):
		authorizer_g = NoneGroup()
		authorizer_u = NoneAccount()
		if not authorizer_g.retrieve(db, auth_key=args.get('signer')):
			return {'err', 'ag retrieve'}, 404
		else:
			if authorizer_g.name == 'Readers':
				return {'err': 'au level'}, 404
			else:
				if not authorizer_u.retrieve(db, group_id=authorizer_g.id):
					return {'err': 'au retrieve'}, 404
				else:
					name = args.get('name')
					id = args.get('id')
					username = args.get('username')

					a = NoneAccount()
					if not a.retrieve(db, id=id):
						return {'err': 'a.retrieve'}, 404
					else:
						if name != None:
							a.name = name
						if username != None:
							a.username = username

						a.update(db)

						if (authorizer_g.name == 'Owners'):
							db2 = DBM(self.dbm.db_path + '.bak.sqlite', self.dbm.init)
							a.update(db2)

						return a.dict()

		return {}, 404

	def get_groups_v2 (self, db, method, model, args, comparator):
		gid = args.get('id')
		gname = args.get('name')
		gauth_key = args.get('auth_key')

		result = []

		if gid == None and gname == None and gauth_key == None:
			groups = retrieve_all_groups(db)
			for g in groups:
				result.append(g.dict())
		else:
			query = "SELECT * FROM Groups WHERE "
			if gid != None:
				if comparator == "=":
					query += "Groups.id" + comparator + "'" + gid + "' AND "
				else:
					query += "Groups.id" + comparator + "'%" + gid + "%' AND "
			if gname != None:
				if comparator == "=":
					query += "Groups.name" + comparator + "'" + gname + "' AND "
				else:
					query += "Groups.name" + comparator + "'%" + gname + "%' AND "
			if gauth_key != None:
				if comparator == "=":
					query += "Groups.auth_key" + comparator + "'" + gauth_key + "' AND "
				else:
					query += "Groups.auth_key" + comparator + "'%" + gauth_key + "%' AND "
			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			groups = retrieve_groups_fcustom(db, query)
			for g in groups:
				result.append(g.dict())

		db.close()
		return result

	def get_orgs_v2 (self, db, method, model, args, comparator):
		oid = args.get('id')
		oname = args.get('name')
		aid = args.get('aid')
		aname = args.get('aname')
		phone = args.get('phone')
		desc_short = args.get('desc_short')
		website = args.get('website')

		result = []

		if oid == None and oname == None and aid == None and aname == None and phone == None and desc_short == None and website == None:
			all_orgs = retrieve_all_orgs(db)
			for o in all_orgs:
				result.append(o.dict())
		else:
			query = "SELECT Orgs.id, Orgs.name, Orgs.address, Orgs.phone, Orgs.desc_short, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.created_by, Orgs.modified_by, Addresses.id, Addresses.name FROM Orgs, Addresses WHERE Orgs.address=Addresses.id AND "

			if oid != None:
				if comparator == "=":
					query += "Orgs.id" + comparator + "'" + oid + "' AND "
				else:
					query += "Orgs.id" + comparator + "'%" + oid + "%' AND "
			if oname != None:
				if comparator == "=":
					query += "Orgs.name" + comparator + "'" + oname  + "' AND "
				else:
					query += "Orgs.name" + comparator + "'%" + oname  + "%' AND "
			if aid != None:
				if comparator == "=":
					query += "Addresses.id" + comparator + "'" + aid + "' AND "
				else:
					query += "Addresses.id" + comparator + "'%" + aid + "%' AND "
			if aname != None:
				if comparator == "=":
					query += "Addresses.name" + comparator + "'" + aname + "' AND "
				else:
					query += "Addresses.name" + comparator + "'%" + aname + "%' AND "
			if phone != None:
				if comparator == "=":
					query += "Orgs.phone" + comparator + "'" + phone + "' AND "
				else:
					query += "Orgs.phone" + comparator + "'%" + phone + "%' AND "
			if desc_short != None:
				if comparator == "=":
					query += "Orgs.desc_short" + comparator + "'" + desc_short + "' AND "
				else:
					query += "Orgs.desc_short" + comparator + "'%" + desc_short + "%' AND "
			if website != None:
				if comparator == "=":
					query += "Orgs.website" + comparator + "'" + website + "';"
				else:
					query += "Orgs.website" + comparator + "'%" + website + "%';"

			if query[-4:] == 'AND ':
				query = query[:-4]
				query += ';'

			print(query)

			orgs = retrieve_orgs_fcustom(db, query)
			for o in orgs:
				result.append(o.dict())

		db.close()
		return result

	def put_orgs_v2 (self, db, method, model, args, comparator):
		authorizer_g = NoneGroup()
		authorizer_u = NoneAccount()
		if not authorizer_g.retrieve(db, auth_key=args.get('signer')):
			return {'err', 'ag retrieve'}, 404
		else:
			if authorizer_g.name == 'Readers':
				return {'err': 'au level'}, 404
			else:
				if not authorizer_u.retrieve(db, group_id=authorizer_g.id):
					return {'err': 'au retrieve'}, 404
				else:
					id = args.get('id')
					o = NoneOrg()
					if not o.retrieve(db, id=id):
						return {'err': 'o.retrieve'}, 404
					else:
						name = args.get('name')
						desc_short = args.get('desc_short')
						phone = args.get('phone')
						website = args.get('website')
						address = args.get('address')

						if name != None:
							o.name = name
						if desc_short != None:
							o.desc_short = desc_short
						if phone != None:
							o.phone = phone
						if website != None:
							o.website = website
						if address != None:
							a = NoneAddress()
							if a.retrieve(db, id=address):
								o.address = a


						if name != None or desc_short != None or phone != None or website != None:
							o.modified_by = authorizer_u

						o.update(db)

						if (authorizer_g.name == 'Owners'):
							db2 = DBM(self.dbm.db_path + '.bak.sqlite', self.dbm.init)
							o.update(db2)

						return o.dict()

	def post_auth(self, method, model, args, message):
		username = args['username']
		password = args['password']

		acct = NoneAccount()
		if acct.retrieve(self.dbm, username=username):
			if not acct.password_equals(password):
				acct.retrieve(self.dbm, group_name='Readers')
		else:
			acct.retrieve(self.dbm, group_name='Readers')

		result = 	{
						'account': {
							'name': acct.name,
							'username': acct.username,
							'id': acct.id,
							'permission': acct.group.name,
							'auth_key': acct.group.auth_key
						}
					}

		return result
