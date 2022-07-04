import os
import base64
import binascii
import codecs
import hashlib
import sqlite3
import uuid
import datetime
from urllib.parse import urlencode

from flask import Flask, session, render_template, request, redirect
from dbm import DBM
from crender import CRender

app = Flask("myResume", static_url_path='/static')
app.secret_key = os.urandom(24).hex()
dbm = DBM('../dat/db.sqlite', True)
cr = CRender(dbm)

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
	return redirect('/reauth?r=_home')

@app.route('/reauth', methods=['GET'])
def reauthenticate():
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
	app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
	session.permanent = True

	platform = request.user_agent
	print(request.user_agent)
	if 'iPhone' in str(platform) or 'Android' in str(platform):
		session['mobile'] = True
	else:
		session['mobile'] = False

	r = request.args.get('r')
	if r != None:
		r = r.replace('_', '/')
		return redirect(r)
	else:
		return redirect('/home')

@app.route('/home')
def home():
	if session.get('username') == None:
		return redirect('/reauth?r=_home')

	contact = cr.mc.home_contact_query()
	jobs = cr.mc.home_jobs_query()
	edus = cr.mc.home_edu_query()

	html = cr.render_html_head('/home', session['mobile'])
	html += cr.render_header(session['name'], '/', '/home', session)


	html += cr.home_home_htmlify(contact, edus, jobs, session)



	return html

@app.route('/jobs/<string:job_id>')
def job_by_id(job_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_jobs_' + job_id)

	this_job = cr.mc.jobs_byid_query(job_id)
	if len(this_job) == 0:
		return redirect('/err?resource=Job')
	contact = cr.mc.home_contact_query()

	html = cr.render_html_head('/jobs/'+job_id, session['mobile'])
	html += cr.render_header(session['name'], '/jobs', '/jobs/' + job_id, session)

	html += cr.jobs_jobs_htmlify(this_job, session['mobile'])
	html += "</body></html>"
	return html

@app.route('/edus/<string:edu_id>')
def edu_by_id(edu_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_edus_' + edu_id)

	this_edu = cr.mc.edus_byid_query(edu_id)
	if len(this_edu) == 0:
		return redirect('/err?resource=Education')
	contact = cr.mc.home_contact_query()

	html = cr.render_html_head('/edus/'+edu_id, session['mobile'])
	html += cr.render_header(session['name'], '/edus', '/edus/' + edu_id, session)

	html += cr.edus_edus_htmlify(this_edu, session['mobile'])
	html += "</body></html>"
	return html

@app.route('/orgs/<string:org_id>')
def org_by_id(org_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_orgs_' + org_id)

	orgs = cr.mc.orgs_byid_query(org_id)
	if len(orgs) == 0:
		return redirect('/err?resource=Organization')

	html = cr.render_html_head('/orgs/'+org_id, session['mobile'])
	html += cr.render_header(session['name'], '/orgs', '/orgs/' + org_id, session)
	print(str(orgs))
	html += cr.org_htmlify(orgs, session['mobile'])
	html += '''	</div>
			</div>
			</body></html>'''

	return html

@app.route('/skills/<string:skill_id>')
def skill_by_id(skill_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_skills_' + skill_id)

	this_skill = cr.mc.skills_byid_query(skill_id)
	if len(this_skill) == 0:
		return redirect('/err?resource=Skill')

	html = cr.render_html_head('/skills/'+skill_id, session['mobile'])
	html += cr.render_header(session['name'], '/skills', '/skills/' + skill_id, session)

	html += cr.skills_skills_htmlify(this_skill, session['mobile'])

	return html

@app.route('/jobs')
def jobs_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_jobs')

	jid = cr.mc.jobs_general_query()
	if jid == None:
		# return 404
		return redirect('/err?resource=Job')
	else:
		return redirect('/jobs/' + jid)

@app.route('/edus')
def edus_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_edus')

	eid = cr.mc.edus_general_query()
	if eid == None:
		# return 404
		return redirect('/err?resource=Education')
	else:
		return redirect('/edus/' + eid)

@app.route('/orgs')
def orgs_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_orgs')

	oid = cr.mc.orgs_general_query()
	if oid == None:
		# return 404
		return redirect('err?resource=Organization')
	else:
		return redirect('/orgs/' + oid)

@app.route('/skills')
def skills_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_skills')

	all_skills = cr.mc.skills_general_query()

	html = cr.render_html_head('/skills', session['mobile'])
	html += cr.render_header(session['name'], '/skills', '/skills', session)

	html += cr.skills_general_htmlify(all_skills, session['mobile'])

	return html

@app.route('/about')
def about():
	if session.get('username') == None:
		return redirect('/reauth?r=_about')

	html = cr.render_html_head('/about', session['mobile'])
	html += cr.render_header(session['name'], '/about', '/about', session)
	html += cr.render_about(session)
	html += '''
			</body>
		</html>'''

	return html

@app.route('/err', methods=['GET'])
def err ():
	resource = request.args.get('resource')

	html = cr.render_html_head('/err?resource=' + resource, session['mobile'])
	html += cr.render_header(session['name'], '/err', '/err?resource=' + resource , session)
	html += cr.render_err(session, resource)
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

	platform = request.user_agent
	if 'iPhone' in str(platform) or 'Android' in str(platform):
		session['mobile'] = True
	else:
		session['mobile'] = False

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

	platform = request.user_agent
	if 'iPhone' in str(platform) or 'Android' in str(platform):
		session['mobile'] = True
	else:
		session['mobile'] = False

	return redirect(r)

@app.route('/restore', methods=['GET'])
def restore ():
	r = request.args.get('r')
	if r == None:
		r = '_home'

	html = cr.render_html_head('/restore', session['mobile'])
	html += cr.render_header(session['name'], '/restore', '/restore', session)
	html += cr.render_restore(session, r)
	return html

@app.route('/create/job', methods=['POST'])
def create_job():
	skills = ""
	form_data = {}

	d = list(request.form.lists())
	for s in d:
		if s[0] == 'skill_selector':
			for a in s[1]:
				skills += str(a) + ','
	present = False
	if 'present' in request.form:
		present = True
	else:
		present = False

	if request.form['job_add_skills_i'] == "True":
		skills_to_add = []
		max_skill_no = int(request.form['job_max_skills'])

		for i in range(1, max_skill_no + 1):
			ele1 = 'j_s_name' + str(i)
			if ele1 in request.form:
				v1 = request.form[ele1]
				v2 = request.form['j_s_exposure' + str(i)]
				v3 = request.form['j_s_reference' + str(i)]
				v4 = request.form['j_s_category' + str(i)]
				v5 = request.form['j_s_desc_short' + str(i)]
				v6 = request.form['j_s_desc_long' + str(i)]
				if 'j_s_icon' + str(i) in request.form:
					if request.form['j_s_icon' + str(i)] == '':
						v7 = None
					else:
						v7 = bytes(request.form['j_s_icon' + str(i) + '_val'], 'utf-8')
				else:
					v7 = None
				if 'j_s_soft' + str(i) in request.form:
					v8 = 0
				else:
					v8 = 1

				nsid = dbm.genid()
				new_skill = {
								'id': nsid,
								'name': v1,
								'exposure': v2,
								'reference': v3,
								'category': v4,
								'desc_short': v5,
								'desc_long': v6,
								'icon': v7,
								'soft_or_hard': v8
							}
				skills_to_add.append(new_skill)
				skills += nsid + ','
		form_data['skills'] = skills_to_add



	id = dbm.genid()

	new_job = {
		'id': id,
		'title': request.form['title'],
		'present': present,
		'date_start': request.form['date_start'],
		'date_stop': request.form['date_stop'],
		'desc_short': request.form['desc_short'],
		'desc_long': request.form['desc_long'],
		'skill_ids': skills[:len(skills)-1],
	}


	if request.form['job_add_org_i'] == "True":
		oid = dbm.genid()
		new_job['org_id'] = oid
		new_org = 	{
						'id': oid,
						'name': request.form['j_o_name'],
						'phone': request.form['j_o_phone'],
						'website': request.form['j_o_website'],
						'desc_short': request.form['j_o_desc_short'],
					}
		if 'j_o_icon' in request.form:
			if request.form['j_o_icon'] == '':
				new_org['logo'] = None
			else:
				new_org['logo'] = bytes(request.form['j_o_icon_val'], 'utf-8')
		else:
			new_org['logo'] = None
		if 'j_o_header' in request.form:
			if request.form['j_o_header'] == '':
				new_org['image_head'] = None
			else:
				new_org['image_head'] = bytes(request.form['j_o_header_val'], 'utf-8')
		else:
			new_org['image_head'] = None

		if request.form['job_add_address_i'] == "True":
			aid = dbm.genid()
			new_org['address'] = aid
			param = [("q", request.form['j_o_new_address'])]
			uri = "https://www.google.com/search?" + urlencode(param)
			new_adr = 	{
							'id': aid,
							'name': request.form['j_o_new_address'],
							'uri': uri
						}
			form_data['address'] = new_adr
		else:
			new_org['address'] = request.form['j_o_address_selector']
		form_data['org'] = new_org
	else:
		new_job['org_id'] = request.form['org_selector']


	form_data['job'] = new_job



	html = ''
	html += cr.render_html_head('/job', session['mobile'])
	html += cr.render_header(session['name'], '/create/job', '/create/job/' + id, session)
	html += cr.render_go_between('add', 'job', form_data, session)


	return html

@app.route('/create/edu', methods=['POST'])
def create_edu():
	skills = ""
	form_data = {}
	print(str(request.form))

	d = list(request.form.lists())
	for s in d:
		if s[0] == 'skill_selector':
			for a in s[1]:
				skills += str(a) + ','

	if request.form['edu_add_skills_i'] == "True":
		skills_to_add = []
		max_skill_no = int(request.form['edu_max_skills'])

		for i in range(1, max_skill_no + 1):
			ele1 = 'e_s_name' + str(i)
			if ele1 in request.form:
				v1 = request.form[ele1]
				v2 = request.form['e_s_exposure' + str(i)]
				v3 = request.form['e_s_reference' + str(i)]
				v4 = request.form['e_s_category' + str(i)]
				v5 = request.form['e_s_desc_short' + str(i)]
				v6 = request.form['e_s_desc_long' + str(i)]
				if 'e_s_icon' + str(i) in request.form:
					if request.form['e_s_icon' + str(i)] == '':
						v7 = None
					else:
						v7 = bytes(request.form['e_s_icon' + str(i) + '_val'], 'utf-8')
				else:
					v7 = None
				if 'e_s_soft' + str(i) in request.form:
					v8 = 0
				else:
					v8 = 1

				nsid = dbm.genid()
				new_skill = {
								'id': nsid,
								'name': v1,
								'exposure': v2,
								'reference': v3,
								'category': v4,
								'desc_short': v5,
								'desc_long': v6,
								'icon': v7,
								'soft_or_hard': v8
							}
				skills_to_add.append(new_skill)
				skills += nsid + ','
		form_data['skills'] = skills_to_add



	id = dbm.genid()

	new_edu = {
		'id': id,
		'degree': request.form['degree'],
		'gpa': request.form['gpa'],
		'date_stop': request.form['date_stop'],
		'desc_short': request.form['desc_short'],
		'desc_long': request.form['desc_long'],
		'skill_ids': skills[:len(skills)-1],
	}


	if request.form['edu_add_org_i'] == "True":
		oid = dbm.genid()
		new_edu['org'] = oid
		new_org = 	{
						'id': oid,
						'name': request.form['e_o_name'],
						'phone': request.form['e_o_phone'],
						'website': request.form['e_o_website'],
						'desc_short': request.form['e_o_desc_short'],
					}
		if 'e_o_icon' in request.form:
			if request.form['e_o_icon'] == '':
				new_org['logo'] = None
			else:
				new_org['logo'] = bytes(request.form['e_o_icon_val'], 'utf-8')
		else:
			new_org['logo'] = None
		if 'e_o_header' in request.form:
			if request.form['e_o_header'] == '':
				new_org['image_head'] = None
			else:
				new_org['image_head'] = bytes(request.form['e_o_header_val'], 'utf-8')
		else:
			new_org['image_head'] = None

		if request.form['edu_add_address_i'] == "True":
			aid = dbm.genid()
			new_org['address'] = aid
			param = [("q", request.form['e_o_new_address'])]
			uri = "https://www.google.com/search?" + urlencode(param)
			new_adr = 	{
							'id': aid,
							'name': request.form['e_o_new_address'],
							'uri': uri
						}
			form_data['address'] = new_adr
		else:
			new_org['address'] = request.form['e_o_address_selector']
		form_data['org'] = new_org
	else:
		new_edu['org'] = request.form['edu_org_selector']


	form_data['edu'] = new_edu



	html = ''
	html += cr.render_html_head('/edu', session['mobile'])
	html += cr.render_header(session['name'], '/create/edu', '/create/edu/' + id, session)
	html += cr.render_go_between('add', 'edu', form_data, session)


	return html

@app.route('/create/org', methods=['POST'])
def create_org():
	if request.form['org_add_address_i'] == "True":
		aid = dbm.genid()
		aname = request.form['a_o_new_address']
		new_addr = True
	else:
		aid = request.form['a_o_address_selector']
		aname = None
		new_addr = False
		
	if request.form['a_o_icon'] != None and request.form['a_o_icon'] != "":
		logo = bytes(request.form['a_o_icon_val'], 'utf-8')
	else:
		logo = dbm.imgtobin('static/placeholder-logo.png')
		
	if request.form['a_o_header'] != None and request.form['a_o_header'] != "":
		image_head = bytes(request.form['a_o_header_val'], 'utf-8')
	else:
		image_head = dbm.imgtobin('static/placeholder-header.png')
		
	form_data =	{
					'id': dbm.genid(),
					'name': request.form['a_o_name'],
					'phone': request.form['a_o_phone'],
					'website': request.form['a_o_website'],
					'desc_short': request.form['a_o_desc_short'],
					'logo': logo,
					'image_head': image_head,
					'new_addr': new_addr,
					'aid': aid,
					'aname': aname
				}
				
	html = ''
	html += cr.render_html_head('/org', session['mobile'])
	html += cr.render_header(session['name'], '/create/org', '/create/org/' + form_data['id'], session)
	html += cr.render_go_between('add', 'org', form_data, session)
	
	return html

@app.route('/create/skill', methods=['POST'])
def create_skill():
	if request.form['s_a_icon'] != None and request.form['s_a_icon'] != "":
		logo = bytes(request.form['s_a_icon_val'], 'utf-8')
	else:
		logo = dbm.imgtobin('static/placeholder-logo.png')
	if request.form['s_a_soh'] == True:
		soh = False
	else:
		soh = True
	
	form_data = {
					'id': dbm.genid(),
					'name': request.form['s_a_name'],
					'exposure': request.form['s_a_exposure'],
					'soft_or_hard': soh,
					'reference': request.form['s_a_reference'],
					'icon': logo,
					'category': request.form['s_a_category'],
					'desc_short': request.form['s_a_desc_short'],
					'desc_long': request.form['s_a_desc_long']
				}
				
	html = ''
	html += cr.render_html_head('/skills', session['mobile'])
	html += cr.render_header(session['name'], '/create/skill', '/create/skill/' + form_data['id'], session)
	html += cr.render_go_between('add', 'skill', form_data, session)
	
	return html

@app.route('/update/edu', methods=['POST'])
def update_edu():
	skills = ""
	form_data = {}

	d = list(request.form.lists())
	for s in d:
		if s[0] == 'e_e_skill_selector':
			for a in s[1]:
				skills += str(a) + ','
	
	o = request.form['e_e_org_selector']
	
	form_data = {
					'id' : request.form['e_e_id'],
					'degree' : request.form['e_e_degree'],
					'gpa' : request.form['e_e_gpa'],
					'date_stop' : request.form['e_e_date_stop'],
					'desc_short' : request.form['e_e_desc_short'],
					'desc_long' : request.form['e_e_desc_long'],
					'org' : o,
					'skill_ids' : skills
				}
	
	html = ''
	html += cr.render_html_head('/edu', session['mobile'])
	html += cr.render_header(session['name'], '/update/edu', '/update/edu/' + form_data['id'], session)
	html += cr.render_go_between('update', 'edu', form_data, session)
	
	return html
	
@app.route('/update/job', methods=['POST'])
def update_job():
	skills = ""
	form_data = {}
	
	d = list(request.form.lists())
	for s in d:
		if s[0] == 'e_j_skill_selector':
			for a in s[1]:
				skills += str(a) + ','
	
	o = request.form['e_j_org_selector']
	
	if request.form['e_j_date_stop'] == "" or request.form['e_j_date_stop'] == None:
		date_stop = None
	else:
		date_stop = ['e_j_date_stop']
		
	if 'e_j_present' in request.form:
		present = 1
	else:
		present = 0
	
	form_data = {
					'id': request.form['e_j_id'],
					'title': request.form['e_j_title'],
					'present': present,
					'date_start': request.form['e_j_date_start'],
					'date_stop': date_stop,
					'desc_short': request.form['e_j_desc_short'],
					'desc_long': request.form['e_j_desc_long'],
					'org': o,
					'skill_ids': skills
				}
	
	html = ''
	html += cr.render_html_head('/job', session['mobile'])
	html += cr.render_header(session['name'], '/update/job', '/update/job' + form_data['id'], session)
	html += cr.render_go_between('update', 'job', form_data, session)
	
	return html

@app.route('/update/contact', methods=['POST'])
def update_contact():
	if request.form['contact_add_address_i'] == "True":
		new_address = True
	else:
		new_address = False
		
	if new_address:
		address = request.form['e_c_new_address']
	else:
		address = request.form['e_c_address_selector']
		
	form_data =	{
					'id': request.form['e_c_id'],
					'name': request.form['e_c_name'],
					'phone1': request.form['e_c_phone1'],
					'phone2': request.form['e_c_phone2'],
					'email': request.form['e_c_email'],
					'objective': request.form['e_c_objective'],
					'new_address': new_address,
					'address': address
				}
				
	html = ''
	html += cr.render_html_head('/contact', session['mobile'])
	html += cr.render_header(session['name'], '/update/contact', '/update/contact' + form_data['id'], session)
	html += cr.render_go_between('update', 'contact', form_data, session)
	
	return html

@app.route('/update/org', methods=['POST'])
def update_org():
	if request.form['org_edit_address_i'] == "True":
		aid = dbm.genid()
		aname = request.form['e_oo_new_address']
		new_addr = True
	else:
		aid = request.form['e_oo_address_selector']
		aname = None
		new_addr = False
		
	if request.form['e_oo_icon'] == "Current" or request.form['e_oo_icon'] == "":
		new_icon = False
		icon = None
	else:
		new_icon = True
		icon = bytes(request.form['e_oo_icon_val'], 'utf-8')
		
	if request.form['e_oo_header'] == "Current" or request.form['e_oo_header'] == "":
		new_header = False
		header = None
	else:
		new_header = True
		header = bytes(request.form['e_oo_header_val'], 'utf-8')
		
	
	form_data = {
					'id': request.form['e_oo_id'], 
					'name': request.form['e_oo_name'],
					'phone': request.form['e_oo_phone'],
					'desc_short': request.form['e_oo_desc_short'],
					'website': 	request.form['e_oo_website'],
					'new_logo': new_icon,
					'logo': icon,
					'new_image_head': new_header,
					'image_head': header,
					'new_address': new_addr,
					'aid': aid,
					'aname': aname,
				}
	
	html = ''
	html += cr.render_html_head('/orgs', session['mobile'])
	html += cr.render_header(session['name'], '/update/org', '/update/org' + form_data['id'], session)
	html += cr.render_go_between('update', 'org', form_data, session)
	
	return html

@app.route('/update/skill', methods=['POST'])
def update_skill():
	if request.form['s_e_icon_val'] == '':
		update_icon = False
		icon = None
	else:
		update_icon = True
		icon = bytes(request.form['s_e_icon_val'], 'utf-8')
		
	form_data = {
					'id': request.form['s_e_id'],
					'name': request.form['s_e_name'],
					'exposure': request.form['s_e_exposure'],
					'soft_or_hard': request.form['s_e_soh'],
					'reference': request.form['s_e_reference'],
					'update_icon': update_icon,
					'icon': icon,
					'category': request.form['s_e_category'],
					'desc_short': request.form['s_e_desc_short'],
					'desc_long': request.form['s_e_desc_long']
				}
				
	html = ''
	html += cr.render_html_head('/skills', session['mobile'])
	html += cr.render_header(session['name'], '/update/skill', '/update/skill/' + form_data['id'], session)
	html += cr.render_go_between('update', 'skill', form_data, session)
	
	return html

@app.route('/delete/edu', methods=['POST'])
def delete_edu():
	del_org = False
	del_addr = False
	l = list(request.form.lists())
	for item in l:
		if (item[0] == 'd_e_del_org'):
			if str(item[1][0]) == 'true':
				del_org = True
		if (item[0] == 'd_e_del_addr'):
			if str(item[1][0]) == 'true':
				del_addr = True
				
	eid = request.form['d_e_id']
	if del_org:
		oid = request.form['d_e_oid']
	else:
		oid = None
	if del_addr:
		aid = request.form['d_e_aid']
	else:
		aid = None
		
	form_data =	{
					'eid': eid,
					'del_org': del_org,
					'oid': oid,
					'del_addr': del_addr,
					'aid': aid
				}
	
	html = ''
	html += cr.render_html_head('/edu', session['mobile'])
	html += cr.render_header(session['name'], '/delete/edu', '/delete/edu' + form_data['eid'], session)
	html += cr.render_go_between('delete', 'edu', form_data, session)
	return html

@app.route('/delete/job', methods=['POST'])
def delete_job():
	del_org = False
	del_addr = False
	l = list(request.form.lists())
	for item in l:
		if (item[0] == 'd_j_del_org'):
			if str(item[1][0]) == 'true':
				del_org = True
		if (item[0] == 'd_j_del_addr'):
			if str(item[1][0]) == 'true':
				del_addr = True
				
	jid = request.form['d_j_id']
	if del_org:
		oid = request.form['d_j_oid']
	else:
		oid = None
	if del_addr:
		aid = request.form['d_j_aid']
	else:
		aid = None
		
	form_data =	{
					'jid': jid,
					'del_org': del_org,
					'oid': oid,
					'del_addr': del_addr,
					'aid': aid
				}
				
	html = ''
	html += cr.render_html_head('/job', session['mobile'])
	html += cr.render_header(session['name'], '/delete/job', '/delete/job' + form_data['jid'], session)
	html += cr.render_go_between('delete', 'job', form_data, session)
	return html

@app.route('/delete/org', methods=['POST'])
def delete_org():
	print(str(request.form))
	if 'd_o_numjobs' in request.form:
		num_org_jobadj = int(request.form['d_o_numjobs'])
	else:
		num_org_jobadj = 0
	if 'd_o_numedus' in request.form:
		num_org_eduadj = int(request.form['d_o_numedus'])
	else:
		num_org_eduadj = 0

	job_adj = []
	for i in range(num_org_jobadj):
		id = request.form['d_o_jid' + str(i)]
		new_org = request.form['d_o_j_selector' + str(i)]
		job_adj.append([id, new_org])
	
	edu_adj = []
	for i in range(num_org_eduadj):
		id = request.form['d_o_eid' + str(i)]
		new_org = request.form['d_o_e_selector' + str(i)]
		edu_adj.append([id, new_org])

	del_addr = False
	l = list(request.form.lists())
	for item in l:
		if (item[0] == 'd_j_del_addr'):
			if str(item[1][0]) == 'true':
				del_addr = True
				
	oid = request.form['d_o_id']
	if del_addr:
		aid = request.form['d_o_aid']
	else:
		aid = None
	
	form_data =	{
					'oid': oid,
					'del_addr': del_addr,
					'aid': aid,
					'num_jobs': num_org_jobadj,
					'job_adj': job_adj,
					'num_edus': num_org_eduadj,
					'edu_adj': edu_adj
				}
	
	html = ''
	html += cr.render_html_head('/org', session['mobile'])
	html += cr.render_header(session['name'], '/delete/org', '/delete/org' + form_data['oid'], session)
	html += cr.render_go_between('delete', 'org', form_data, session)
	return html

@app.route('/delete/skill', methods=['POST'])
def delete_skill():
	print(str(request.form))
	
	sid = request.form['s_d_id']
	
	if int(request.form['num_j']) > 0:
		del_jobs = True
		jobs = []
		for i in range(int(request.form['num_j'])):
			jobs.append(request.form['s_d_jid' + str(i)])
	else:
		del_jobs = False
		jobs = []
		
	if int(request.form['num_e']) > 0:
		del_edus = True
		edus = []
		for i in range(int(request.form['num_e'])):
			edus.append(request.form['s_d_eid' + str(i)])
	else:
		del_edus = False
		edus = []
		
	form_data = {
					"id": sid,
					"del_jobs": del_jobs,
					"jobs": jobs,
					"del_edus": del_edus,
					"edus": edus
				}
				
	html = ''
	html += cr.render_html_head('/skills', session['mobile'])
	html += cr.render_header(session['name'], '/delete/skill', '/delete/skill' + form_data['id'], session)
	html += cr.render_go_between('delete', 'skill', form_data, session)
	return html
		

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='80',debug=True)
