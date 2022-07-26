"""
	This module is the main flask module containing mostly routing directives for
	the application as well as a few pieces related to session and authentication
	control. Most of the functionality in the app for each of the routes is contained
	outside the scope of this module. The module can be called directly to start
	the flask app.

	Example:
		$ python app.py

	Attributes:
		app (Flask): Module level flask instance that all of the routes derive on.
		dbm (DBM): Main sqlite database connection manager instance that is passed
			to other modules that need to access data. Other modules may duplicate
			the database object when the purpose is for reading data that may be
			done asyncronously, such as with the api routes and functions.
		cr (CRender): Modules level rendering instance that contains much of the
			logic for laying out common html views for the app. Module contains all
			html rendering logic less the views wrapping individual model items.
"""

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
from flask_cors import CORS, cross_origin
from dbm import DBM
from crender import CRender
import json

from controllers.apicontroller import APIController

app = Flask("myResume", static_url_path='/static')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = os.urandom(24).hex()
dbm = DBM('../dat/db.sqlite', True)
api = APIController(dbm)
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
	"""Root route function for the app.

	The root route authenticates the user session if not done before redirecting
	to the /home route.
	"""
	return redirect('/reauth?r=_home')

@app.route('/reauth', methods=['GET'])
def reauthenticate():
	"""Main authenication route and functionality.

	Authenticates a user session as a guest session if not previously done and
	establishes session data. Redirects the route back to either home or a custom
	route as specified by with the argument 'r', with '/' being replaced by '_' for
	the value of the argument.

	Route Args:
		r: The route to redirect after performing the guest authentication if necessary.
			The '/' characters in the route should be replaced by '_' characters.
	"""
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
	"""Home page route and functionality.

	Constructs and returns the home page view using the CRender rendering functionality.
	"""
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
	"""Individual job view for a single instance of a job experience.

	Constructs and returns the html view for a single instance of a job experience
	based on the specified job id passed via the URL. If the specified job does
	not exist, an error page will be returned.

	Route Args:
		job_id: The id for the job to render and return the view for.
	"""
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
	"""Individual education view for a single instance of an education experience.

	Constructs and returns the html view for a single instance of an education experience
	based on the specified job id passed via the URL. If the specified education does
	not exist, an error page will be returned.

	Route Args:
		edu_id: The id for the education to render and return the view for.
	"""
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
	"""Individual organization view for a single instance of an organization.

	Constructs and returns the html view for a single instance of an organization
	based on the specified job id passed via the URL. If the specified organization does
	not exist, an error page will be returned.

	Route Args:
		org_id: The id for the organization to render and return the view for.
	"""
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
	"""Individual skill view for a single instance of a skill.

	Constructs and returns the html view for a single instance of a skill
	based on the specified job id passed via the URL. If the specified skill does
	not exist, an error page will be returned.

	Route Args:
		skill_id: The id for the skill to render and return the view for.
	"""
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
	"""General view for multiple jobs.

	Presently, this route just redirects back to the most recently entered individual
	job instance, instead of rendering its own multi-job view.
	"""
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
	"""General view for multiple edus.

	Presently, this route just redirects back to the most recently entered individual
	edu instance, instead of rendering its own multi-edu view.
	"""
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
	"""General view for multiple orgs.

	Presently, this route just redirects back to the most recently entered individual
	org instance, instead of rendering its own multi-org view.
	"""
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
	"""General view for multiple skills.

	Constructs and returns a view showing all skills contained in the database.
	Separates them into category across technical vs. soft skill.
	"""
	if session.get('username') == None:
		return redirect('/reauth?r=_skills')

	all_skills = cr.mc.skills_general_query()

	html = cr.render_html_head('/skills', session['mobile'])
	html += cr.render_header(session['name'], '/skills', '/skills', session)

	html += cr.skills_general_htmlify(all_skills, session['mobile'])

	return html

@app.route('/about')
def about():
	"""General view for an about page.

	Constructs and returns a view showing some about info for the app.
	"""
	if session.get('username') == None:
		return redirect('/reauth?r=_about')

	html = cr.render_html_head('/about', session['mobile'])
	html += cr.render_header(session['name'], '/about', '/about', session)
	html += cr.render_about(session)
	html += '''
			</body>
		</html>'''

	return html

@app.route('/<string:path>')
def unknown(path):
	return redirect('/err?resource=unknown')

@app.route('/err', methods=['GET'])
def err ():
	"""General view for an error page.

	Constructs and returns an error page, generally for use when a route that does
	not exist is attempted to be accessed. Return a custom result based on the model
	type attempting to be accessed when applicable.

	Route Args:
		resource: The resource that was attempted to be accessed when applicable.
	"""
	resource = request.args.get('resource')

	html = cr.render_html_head('/err?resource=' + resource, session['mobile'])
	html += cr.render_header(session['name'], '/err', '/err?resource=' + resource , session)
	html += cr.render_err(session, resource)
	return html

@app.route('/login', methods=['POST'])
def login():
	"""Does authentication beyond the basic guest level authentication and session establishment.

	Performs authentication function when user attempts to authenticate beyond the basic
	guest authentication session that is established for them. Will redirect and return
	the prior page that was present before the authentication attempt occurred.

	POST Args:
		username: The username to authenticate with.
		raw: The raw password to authenticate with.
		r: The previous page/route where the authentication attempt occurred. Will return
			back to this route upon completing authentication.
	"""
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
	"""Wipes the present authentication session.

	Logs the user out of any authentication session and restablishes the session
	as a guest authentication session. Redirects back to previous route/page after.

	Route Args:
		r: The previous route/page to redirect back to after logout. Route value should
			have '/' characters replaced with '_' characters.
	"""
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
	"""Does a restore on site data.

	Restores site data to an admin created/modified only state, eliminating any
	changes made under the member/contributor account/group levels. Redirects back
	to the prior page after performing the operation.

	Route Args:
		r: The previous route/page to redirect back to after logout. Route value should
			have '/' characters replaced with '_' characters.
	"""
	r = request.args.get('r')
	if r == None:
		r = '_home'

	html = cr.render_html_head('/restore', session['mobile'])
	html += cr.render_header(session['name'], '/restore', '/restore', session)
	html += cr.render_restore(session, r)
	return html

@app.route('/create/job', methods=['POST'])
def create_job():
	"""Route for creating a new job within the app.

	Parses and creates a new job instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for creating a new edu within the app.

	Parses and creates a new edu instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for creating a new org within the app.

	Parses and creates a new org instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for creating a new skill within the app.

	Parses and creates a new skill instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for updating an edu within the app.

	Parses and updates an edu instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for updating a job within the app.

	Parses and updates a job instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for updating a contact within the app.

	Parses and updates a contact instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for updating an org within the app.

	Parses and updates an org instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for updating a skill within the app.

	Parses and updates a skill instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for deleting an edu within the app.

	Parses and deletes an edu instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for deleting a job within the app.

	Parses and deletes a job instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for deleting an org within the app.

	Parses and deletes an org instance and saves to the database from form
	data passed by site forms in the app.
	"""
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
	"""Route for deleting a skill within the app.

	Parses and deletes a skill instance and saves to the database from form
	data passed by site forms in the app.
	"""
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

@app.route('/api/<string:method>/<string:model>', methods=['GET'])
def api_get_handle(method, model):
	"""Route for handling api get requests.

	Old route for handling api get requests. To be deprecated in favor of
	the v2 api routing.
	"""
	return api.parse(method, model, request.args, "=")

@app.route('/api/get/search/<string:model>', methods=['GET'])
def api_search_handle(model):
	"""Route for handling api get requests.

	Old route for handling api get requests. To be deprecated in favor of
	the v2 api routing.
	"""
	return api.parse('get', model, request.args, " LIKE ")

@app.route('/api/v2/<string:method>/<string:model>', methods=['GET', 'POST', 'PUT'])
def api_v2_handle(method, model):
	"""Route for handling non-REST api requests and requests returning multiple instances.
	"""

	if request.method == 'POST':
		return api.v2(method, model, request.form, "=")
	elif request.method == 'PUT':
		if 'id' in request.args and 'auth_key' in request.args:
			return api.v2(method, model, request.form, "=")
		else:
			return {}, 404
	else:
		if method.lower() == 'get':
			item = api.v2(method, model, request.args, "=")
			if len(item) >= 1:
				return json.dumps(item)
			else:
				return {}, 404
		else:
			return api.v2(method, model, request.args, " LIKE ")

@app.route('/api/v2/get/<string:model>/<string:id>', methods=['GET'])
def api_v2_rget(model, id):
	"""Route for handling REST-adhering api GET requests.
	"""
	item = api.v2('get', model, {'id': id}, '=')
	if len(item) == 1:
		return item[0]
	else:
		return {}, 404

@app.route('/api/v2/put/<string:model>/<string:id>', methods=['PUT'])
def api_v2_rput(model, id):
	"""Route for handling REST-adhering api PUT requests.
	"""
	if 'signer' not in request.json:
		return {}, 400
	else:
		args = {}
		for key in request.json:
			args[key] = request.json[key]
		args['id'] = id
		return api.v2('put', model, args, '=')

if __name__ == '__main__':
	"""When called from CLI, start the flask app
	"""
	app.run(host='resume.tomesser.biz', port='80',debug=True)
