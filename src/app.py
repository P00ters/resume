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
	html += cr.render_go_between('job', form_data, session)


	return html

@app.route('/create/edu', methods=['POST'])
def create_edu():
	skills = ""
	d = list(request.form.lists())
	for s in d:
		if s[0] == 'skill_selector':
			for a in s[1]:
				skills += str(a) + ','
	id = dbm.genid()
	form_data = {
		'id': id,
		'degree': request.form['degree'],
		'gpa': request.form['gpa'],
		'date_end': request.form['date_stop'],
		'desc_short': request.form['desc_short'],
		'desc_long': request.form['desc_long'],
		'org_id': request.form['org_selector'],
		'skill_ids': skills[:len(skills)-1]
	}
	
	html = ''
	html += cr.render_html_head('/edu', session['mobile'])
	html += cr.render_header(session['name'], '/create/edu', '/create/edu/' + id, session)
	html += cr.render_go_between('edu', form_data, session)

	return html

if __name__ == '__main__':
	app.run(host='127.0.0.1',port='80',debug=True)
