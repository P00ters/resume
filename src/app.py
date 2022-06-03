import os
import base64
import binascii
import codecs
import hashlib
import sqlite3
import uuid
import datetime

from flask import Flask, session, render_template, request, redirect
from dbm import DBM

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"

app = Flask("myResume", static_url_path='/static')
app.secret_key = os.urandom(24).hex()
dbm = DBM('../dat/db.sqlite')

def get_keys():
	query = '''SELECT * FROM Groups;'''
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		keys = {}
		for row in result:
			keys[row[1]] = row[2]
		return keys				
	else:
		exit('Unable to load authorizations table.')

auth_keys = get_keys()

def get_sesh_key(gid):
	if gid == None:
		return None
	query = 'SELECT auth_key FROM Groups WHERE id="'+gid+'";'
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if (len(result) > 0):
			return result[0][0]
		else:
			return None
	else:
		return None

@app.route('/')
def authenticate():
	if (session.get('username') == None):
		session['username'] = 'guest'
		session['name'] = 'Guest'
		
		query = 'SELECT id, group_id FROM Accounts WHERE username="guest";'
		result = dbm.execute(query)
		if result != None:
			result = dbm.cur.fetchall()
			if (len(result) > 0):
				session['uid'] = result[0][0]
				session['gid'] = result[0][1]
			else:
				session['uid'] = None
				session['gid'] = None
		else:
			session['uid'] = None
			session['gid'] = None
		
	session['auth_key'] = get_sesh_key(session['gid'])
	return redirect('/home')
		
@app.route('/home')
def home():
	if session.get('username') == None:
		return redirect('/')

	contact_dict = home_contact_query()
	jobs_dict = home_jobs_query()
	edus_dict = home_edu_query()
	
	html = render_html_head('/home')
	html += render_header(contact_dict['name'], session['name'], '/', '/home')
	html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;">
					<h1 style="position:absolute;left:50%;top:30%;color:white;font-size:55px;">'''+contact_dict['name']+'''</h1>
					
					<div style="position:absolute;left:50%;top:55%;z-index:2;">
						<img src="/static/Addr.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="'''+contact_dict['address']['uri']+'''" style="color:white;">'''+contact_dict['address']['name']+'''</a>
						</h4>
					</div>
					
					<div style="position:absolute;left:50%;top:67.5%;z-index:2;">
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;padding-left:5px;position:relative;top:5px;">
						<a href="'''+telelink(contact_dict['phone1'])+'''" style="color:white;">'''+teleformat(contact_dict['phone1'])+'''</a></h4>
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;position:relative;left:50px;" />
						<h4 style="display:inline;padding-left:5px;position:relative;left:50px;top:5px;">
						<a href="'''+telelink(contact_dict['phone2'])+'''" style="color:white;">'''+teleformat(contact_dict['phone2'])+'''</a></h4>
					</div>
					
					<div style="position:absolute;left:50%;top:80%;z-index:2;">
						<img src="/static/Mail.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="mailto:'''+contact_dict['email']+'''" style="color:white;">'''+contact_dict['email']+'''</a>
						</h4>
					</div>
						
					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;"/>
					
				</div>
				<br>

				<div class="row" style="overflow:hidden;">
					<div class="col-sm-5" style="padding-left:40px;">
						<h2 class="mb-4">Objective</h2>
							<div class="card w-75">
								<div class="card-body">
									'''+contact_dict['objective']+'''
								</div>
							</div>
						<br>
						<h2 class="mb-4">Education</h2>'''
	for edu in edus_dict:
		html += home_edu_htmlify(edu)
	html+=			'''
					<span style="display:inline-block;border-left:1px solid #ccc;height:100%;position:relative;top:-100%;left:90%;"></span>
					</div>
					
					<div class="col-sm-7">
						<div class="row">
							<div class="col-sm-8">
								<h2 class="mb-4">Work Experience</h2>
							</div>
							<div class="col-sm-1">'''
	if session.get('name') != 'Guest':
		html +=				'''<button type="button" class="btn btn-secondary btn-lg btn-block">+</button>'''
	html +=					'''</div>
						</div>'''
	for job in jobs_dict:
		html += home_job_htmlify(job)
				
	html +=		'''</div>
				</div>
			</body>
		</html>'''
	return html

@app.route('/jobs/<string:job_id>')
def job_by_id(job_id):
	this_job = jobs_jobs_query(job_id)
	contact_dict = home_contact_query()

	html = render_html_head('/jobs/'+job_id)
	html += render_header(contact_dict['name'], session['name'], '/jobs', '/jobs/' + job_id)
	
	html += jobs_jobs_htmlify(this_job)
	html += "</body></html>"
	return html

@app.route('/edus/<string:edu_id>')
def edu_by_id(edu_id):
	this_edu = edus_edus_query(edu_id)
	contact_dict = home_contact_query()
	
	html = render_html_head('/edus/'+edu_id)
	html += render_header(contact_dict['name'], session['name'], '/edus', '/edus/' + edu_id)
	
	html += edus_edus_htmlify(this_edu)
	html += "</body></html>"
	return html

@app.route('/jobs')
def jobs_general():
	return jobs_jobs_general_query()

@app.route('/edus')
def edus_general():
	return edus_edus_general_query()

@app.route('/about')
def about():
	contact_dict = home_contact_query()

	html = render_html_head('/about')
	html += render_header(contact_dict['name'], session['name'], '/about', '/about')
	html += str(session['auth_key'])
	html += str(auth_keys)
	html += '''
			</body>
		</html>'''
	
	return html

@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	raw = request.form['password']
	r = request.form['redirect']
	
	if username != session.get('username'):
		query = '''SELECT 	Accounts.id, Accounts.username, Accounts.password, 
							Accounts.salt, Accounts.name, Accounts.group_id, Groups.auth_key
					FROM	Accounts, Groups
					WHERE	Accounts.group_id = Groups.id AND Accounts.username="'''+username+'''";'''
		result = dbm.execute(query)
		if result != None:
			result = dbm.cur.fetchall()
			if len(result) > 0:
				row = result[0]
				data = { 'a_id': row[0], 'username': row[1], 'password': row[2], 'salt': row[3], 'name': row[4], 'g_id': row[5], 'auth_key': row[6] }
				
				from_raw = hashlib.sha512((raw+ data['salt']).encode('utf-8')).hexdigest()
				if from_raw == data['password']:
					session['username'] = data['username']
					session['name'] = data['name']
					session['uid'] = data['a_id']
					session['gid'] = data['g_id']
					session['auth_key'] = data['auth_key']
		
	return redirect(r)

@app.route('/logout', methods=['GET'])
def logout():
	r = request.args.get('r')
	r = r.replace('_', '/')

	session['username'] = 'guest'
	session['name'] = 'Guest'
	
	query = 'SELECT id, group_id FROM Accounts WHERE username="guest";'
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if (len(result) > 0):
			session['uid'] = result[0][0]
			session['gid'] = result[0][1]
		else:
			session['uid'] = None
			session['gid'] = None
	else:
		session['uid'] = None
		session['gid'] = None
		
	session['auth_key'] = get_sesh_key(session['gid'])
	return redirect(r)

def edus_edus_query(id):
	query = '''SELECT 	Education.id, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.desc, 
						Orgs.website, Orgs.logo, Orgs.image_head, Education.degree, Education.gpa,
						Education.skill_ids, Education.date_end, Education.desc_short, Education.desc_long
				FROM	Education, Orgs, Addresses
				WHERE	Education.org = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	edu_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
				result = dbm.execute(query)
				if result != None:
					result = dbm.cur.fetchall()
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

def edus_edus_general_query():
	query = '''SELECT 	Education.id, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.desc, 
						Orgs.website, Orgs.logo, Orgs.image_head, Education.degree, Education.gpa,
						Education.skill_ids, Education.date_end, Education.desc_short, Education.desc_long
				FROM	Education, Orgs, Addresses
				WHERE	Education.org = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	edu_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
				result = dbm.execute(query)
				if result != None:
					result = dbm.cur.fetchall()
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
	return edu_by_id(edu_rows[0]['id'])

def jobs_jobs_general_query():
	query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, 
						Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo
				FROM Jobs, Orgs, Addresses
				WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	job_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
				result = dbm.execute(query)
				if result != None:
					result = dbm.cur.fetchall()
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
	return job_by_id(job_rows[0]['id'])

def home_contact_query():
	query = 'SELECT * FROM Contact;'
	result = dbm.execute(query)
	if result != None:
		result = dbm.cur.fetchall()
		if (len(result) > 0):
			contact_row = result[len(result) - 1]
			
			query = 'SELECT id, name, uri FROM Addresses WHERE id="' + contact_row[2] + '";'
			result = dbm.execute(query)
			if result != None:
				result = dbm.cur.fetchall()
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

def home_edu_query():
	query = '''SELECT	Education.id, Education.degree, Education.gpa, Education.skill_ids, Education.date_end, Education.desc_short, 
						Education.desc_long, Orgs.id, Orgs.name, Orgs.phone, Orgs.website, Orgs.logo, Addresses.id, Addresses.name, 
						Addresses.uri
				FROM	Education, Orgs, Addresses
				WHERE   Education.org = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	edu_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
							query += 'id="' + skills[i] + '" '
						else:
							query += 'id="' + skills[i] + '";'
					result = dbm.execute(query)
					if result != None:
						result = dbm.cur.fetchall()
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

def jobs_jobs_query(id):
	query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, 
						Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo, Orgs.image_head, Orgs.desc
				FROM Jobs, Orgs, Addresses
				WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	job_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
				result = dbm.execute(query)
				if result != None:
					result = dbm.cur.fetchall()
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

def jobs_jobs_htmlify(jobs):
	logo = "data:image/png;base64,"
	logo += jobs['this']['org']['logo'].decode('utf-8')
	head = "data:image/png;base64,"
	head += jobs['this']['org']['header'].decode('utf-8')

	html = '''<div class="jumbotron">
				<img src="'''+head+'''" style="position:relative;width:70%;left:15%;z-index:0;max-height:25%;"/>
				<a href="/jobs/'''+jobs['next']['id']+'''">
					<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
				</a>
				<a href="/jobs/'''+jobs['last']['id']+'''">
					<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
				</a>
				<br>
				<div style="position:relative;width:100%;z-index=1;">
					
					
					<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
						<div class="card-header">
							<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
								<img src="'''+logo+'''" width="45" height="45"/>
							</div>
							<a href="/orgs/'''+jobs['this']['org']['id']+'''" style="color:black;">
								<h4 style="display:inline;padding-left:10px;vertical-align:middle;">'''+jobs['this']['org']['name']+'''</h4>
							</a>
						</div>
						<div class="card-body" style="z-index:0;">
							<div class="row">
								<div class="col-sm-6">
									<h6>Description:</h6>
									'''+jobs['this']['org']['desc']+'''
								</div>
								<div class="col-sm-2">
									<h6>Information:</h6>
									'''+addresslines(jobs['this']['org']['address']['name'])+'''
									<a href="'''+telelink(jobs['this']['org']['phone'])+'''">'''+teleformat(jobs['this']['org']['phone'])+'''
									<br>
									<a href="'''+jobs['this']['org']['website']+'''" target="_blank">Website</a>
								</div>
								<div class="col-sm-4">
									<iframe
										width="325"
										height="200" 
										frameborder="0" style="border:0" 
										referrerpolicy="no-referrer-when-downgrade"
										src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q='''+jobs['this']['org']['address']['name']+'''"
										allowfullscreen>
									</iframe>
								</div>
							</div>
							<div style="position:relative;left:71%;width:25%;font-size:8px;text-align:right;padding-top:10px;">
								<a href="/orgs/''' + str(jobs['this']['org']['id']) + '''">''' + str(jobs['this']['org']['id']) + '''</a>
							</div>
						</div>
					</div>
					<br>
					<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
						<div class="card-header">
							<div class="row">
								<div class="col-sm-7">
									<h4 style="vertical-align:middle;">'''+jobs['this']['title']+'''</h4>
								</div>
								<div class="col-sm-5" style="text-align:right;">
									<i style="vertical-align:middle;">
							'''
	if jobs['this']['date_stop'] != None:
		html += datereformat(jobs['this']['date_start'])+''' - '''+datereformat(jobs['this']['date_stop'])+'''</i>'''
	else:
		html += datereformat(jobs['this']['date_start'])+''' - Present</i>'''
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

def edus_edus_htmlify(edus):
	logo = "data:image/png;base64,"
	logo += edus['this']['org']['logo'].decode('utf-8')
	head = "data:image/png;base64,"
	head += edus['this']['org']['header'].decode('utf-8')

	html = '''<div class="jumbotron">
				<img src="'''+head+'''" style="position:relative;width:70%;left:15%;z-index:0;max-height:25%;"/>
				<a href="/edus/'''+edus['next']['id']+'''">
					<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
				</a>
				<a href="/edus/'''+edus['last']['id']+'''">
					<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
				</a>
				<br>
				<div style="position:relative;width:100%;z-index=1;">
					
					
					<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
						<div class="card-header">
							<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
								<img src="'''+logo+'''" width="45" height="45"/>
							</div>
							<a href="/orgs/'''+edus['this']['org']['id']+'''" style="color:black;">
								<h4 style="display:inline;padding-left:10px;vertical-align:middle;">'''+edus['this']['org']['name']+'''</h4>
							</a>
						</div>
						<div class="card-body" style="z-index:0;">
							<div class="row">
								<div class="col-sm-6">
									<h6>Description:</h6>
									'''+edus['this']['org']['desc']+'''
								</div>
								<div class="col-sm-2">
									<h6>Information:</h6>
									'''+addresslines(edus['this']['org']['address']['name'])+'''
									<a href="'''+telelink(edus['this']['org']['phone'])+'''">'''+teleformat(edus['this']['org']['phone'])+'''
									<br>
									<a href="'''+edus['this']['org']['website']+'''" target="_blank">Website</a>
								</div>
								<div class="col-sm-4">
									<iframe
										width="325"
										height="200" 
										frameborder="0" style="border:0" 
										referrerpolicy="no-referrer-when-downgrade"
										src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q='''+edus['this']['org']['address']['name']+'''"
										allowfullscreen>
									</iframe>
								</div>
							</div>
							<div style="position:relative;left:71%;width:25%;font-size:8px;text-align:right;padding-top:10px;">
								<a href="/orgs/''' + str(edus['this']['org']['id']) + '''">''' + str(edus['this']['org']['id']) + '''</a>
							</div>
						</div>
					</div>
					<br>
					<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
						<div class="card-header">
							<div class="row">
								<div class="col-sm-7">
									<h4 style="vertical-align:middle;">'''+edus['this']['degree']+'''</h4>
								</div>
								<div class="col-sm-5" style="text-align:right;">
									<i style="vertical-align:middle;">
							'''

	html += datereformat(edus['this']['date_stop'])+'''</i>'''
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

def home_jobs_query():
	query = '''SELECT 	Jobs.id, Jobs.title, Jobs.present, Jobs.date_start, Jobs.date_stop, 
						Jobs.desc_short, Jobs.desc_long, Jobs.skill_ids, Orgs.id, Orgs.name, Addresses.id, Addresses.name, Addresses.uri, Orgs.phone, Orgs.website, Orgs.logo
				FROM Jobs, Orgs, Addresses
				WHERE Jobs.org_id = Orgs.id AND Orgs.address = Addresses.id;'''
	
	result = dbm.execute(query)
	job_rows = []
	if result != None:
		result = dbm.cur.fetchall()
		
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
				result = dbm.execute(query)
				if result != None:
					result = dbm.cur.fetchall()
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
	return job_rows[::-1]

def home_edu_htmlify(edu):
	src = "data:image/png;base64,"
	src += edu['org']['logo'].decode('utf-8')
	
	date_stop = datetime.datetime.strptime(edu['date_end'], '%m/%d/%Y')
	date_stop_str = date_stop.strftime('%b %Y')
	
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
								<h5 class="card-title">''' + str(edu['degree']) + '''</h5>
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
	
	return html

def home_job_htmlify(job):
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
								<h5 class="card-title">''' + str(job['title']) + '''</h5>
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
	
	return html

def render_header(name, user, page, redirect):
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
									<a class="nav-link" href="/skilks">Skills
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
										<a class="dropdown-item" href="javascript:void(0)" onclick="show_login_form()">Login</a>'''
	if session['auth_key'] == auth_keys['Contributors'] or session['auth_key'] == auth_keys['Owners']:
		html +=						'''<a class="dropdown-item" href="/logout?r='''+redirect.replace('/','_')+'''">Logout</a>'''
	html += '''
									</div>
								</li>
							</ul>
						</div>
					</div>
				</nav>
			'''
	
	
	return html

def render_html_head(redirect):
	return '''
		<html>
			<head>
				<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
				<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
				<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
				<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
				<script src="/static/js/lib.js"></script>
				<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
			</head>
			<body>
			<div id="login_form" style="border-radius:10%;background-color:#343a40;position:absolute;width:10%;height:20%;left:80%;top:50px;z-index:-1;opacity:0;">
				<div class="row" style="position:relative;top:5px;">
					<div class="col-sm-6" style="text-align:left;">
						<a href="#" style="padding-left:20px;color:white" data-toggle="tooltip" title="Go ahead and log in as a member to make changes to content (don't worry, the content can be reset)">?</a>
					</div>
					<div class="col-sm-6" style="text-align:right;">
						<a style="color:white;padding-right:20px;" onclick="hide_login_form()" href="javascript:void(0)">close</a><br><br>
					</div>
				</div>
				<form action='/login' method='post'>
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
				</form>
			</div>
			'''

def telelink (phone):
	return "tel:+1" + phone

def teleformat (phone):
	return '(' + phone[:3] + ') ' + phone[3:6] + '-' + phone[6:10]

def addresslines (address):
	a = address.split(',')
	c = ""
	for b in a:
		c += b + '<br>'
	return c

def datereformat (date):
	d = datetime.datetime.strptime(date, '%m/%d/%Y')
	return d.strftime('%b %Y')

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='80',debug=True)