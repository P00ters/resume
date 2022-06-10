import base64
import datetime
import json
import hashlib
import os
import sqlite3
import sys
from urllib.parse import urlencode
import uuid

sys.path.append("models/")

from accounts import Account
from addresses import Address
from contacts import Contact
from educations import Education
from groups import Group
from jobs import Job
from orgs import Org
from skills import Skill

class Populate:
	def __init__(self, dbm):
		self.dbm = dbm
		
	def population(self):
		with open('../dat/def/init.json', 'r') as infile:
			j = json.load(infile)
		
		self.groups = []
		for i in range(len(j['Groups'])):
			g = Group(self.dbm.genid(), j['Groups'][i]['name'], self.dbm.genid())
			g.create(self.dbm)
			self.groups.append(g)
					
		self.accounts = []
		for i in range(len(j['Accounts'])):
			this = j['Accounts'][i]
			salt = uuid.uuid4().hex
			pw = hashlib.sha512((this['password'] + salt).encode('utf-8')).hexdigest()
			a = Account(self.dbm.genid(), this['username'], pw, salt, this['name'], self.groups[this['group']])
			a.create(self.dbm)
			self.accounts.append(a)

	def custom_population(self):
		with open('../dat/def/mydata.json', 'r') as infile:
			j = json.load(infile)
	
		addresses = []
		for i in range(len(j['Addresses'])):
			this = j['Addresses'][i]
			param = [("q", this['name'])]
			uri = "https://www.google.com/search?" + urlencode(param)
			a = Address(self.dbm.genid(), this['name'], uri, self.accounts[0], self.accounts[0])
			a.create(self.dbm)
			addresses.append(a)
		
		skills = []
		for i in range(len(j['Skills'])):
			this = j['Skills'][i]
			icon = self.dbm.imgtobin(this['icon'])
			s = Skill(self.dbm.genid(), this['name'], this['exposure'], this['soft_or_hard'], this['reference'], icon, this['category'], this['desc_short'], this['desc_long'], self.accounts[0], self.accounts[0])
			s.create(self.dbm)
			skills.append(s)
					
		orgs = []
		for i in range(len(j['Orgs'])):
			this = j['Orgs'][i]
			logo = self.dbm.imgtobin(this['logo'])
			image_head = self.dbm.imgtobin(this['image_head'])
			o = Org(self.dbm.genid(), this['name'], addresses[this['address']], this['phone'], this['desc_short'], this['website'], logo, image_head, self.accounts[0], self.accounts[0])
			o.create(self.dbm)
			orgs.append(o)
			
		jobs = []
		for i in range(len(j['Jobs'])):
			this = j['Jobs'][i]
			skill_ids = ""
			skill_splits = this['skill_ids'].split(',')
			for k in range(len(skill_splits)):
				if k != len(skill_splits) - 1:
					skill_ids += skills[int(skill_splits[k])].id + ','
				else:
					skill_ids += skills[int(skill_splits[k])].id
			
			jj = Job(self.dbm.genid(), this['title'], this['present'], this['date_start'], this['date_stop'], this['desc_short'], this['desc_long'], skill_ids, orgs[this['org']], self.accounts[0], self.accounts[0])
			jj.create(self.dbm)
			jobs.append(jj)
			
			
		contacts = []
		for i in range(len(j['Contact'])):
			this = j['Contact'][i]
			c = Contact(self.dbm.genid(), this['name'], addresses[this['address']], this['phone1'], this['phone2'], this['email'], this['objective'], self.accounts[0], self.accounts[0])
			c.create(self.dbm)
			contacts.append(c)
		
		
		educations = []
		for i in range(len(j['Education'])):
			this = j['Education'][i]
			skill_ids = ""
			skill_splits = this['skill_ids'].split(',')
			for k in range(len(skill_splits)):
				if k != len(skill_splits) - 1:
					skill_ids += skills[int(skill_splits[k])].id + ','
				else:
					skill_ids += skills[int(skill_splits[k])].id
					
			e = Education(self.dbm.genid(), orgs[this['org']], this['degree'], this['gpa'], skill_ids, this['date_stop'], this['desc_short'], this['desc_long'], self.accounts[0], self.accounts[0])
			e.create(self.dbm)
			educations.append(e)
		