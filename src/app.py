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
from crender import CRender

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

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"

app = Flask("myResume", static_url_path='/static')
app.secret_key = os.urandom(24).hex()
dbm = DBM('../dat/db.sqlite')
auth_keys = get_keys()
cr = CRender(dbm, auth_keys)

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

	contact_dict = cr.home_contact_query()
	jobs_dict = cr.home_jobs_query()
	edus_dict = cr.home_edu_query()
	
	html = cr.render_html_head('/home')
	html += cr.render_header(contact_dict['name'], session['name'], '/', '/home', session)
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
						<a href="'''+cr.telelink(contact_dict['phone1'])+'''" style="color:white;">'''+cr.teleformat(contact_dict['phone1'])+'''</a></h4>
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;position:relative;left:50px;" />
						<h4 style="display:inline;padding-left:5px;position:relative;left:50px;top:5px;">
						<a href="'''+cr.telelink(contact_dict['phone2'])+'''" style="color:white;">'''+cr.teleformat(contact_dict['phone2'])+'''</a></h4>
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
		html += cr.home_edu_htmlify(edu)
	html+=			'''
					<span style="display:inline-block;border-left:1px solid #ccc;height:100%;position:relative;top:-100%;left:90%;"></span>
					</div>
					
					<div class="col-sm-7">
						<div class="row">
							<div class="col-sm-8">
								<h2 class="mb-4">Work Experience</h2>
							</div>
							<div class="col-sm-1">'''
	if session.get('auth_key') != cr.auth_keys['Readers']:
		html +=				'''<button type="button" class="btn btn-secondary btn-lg btn-block">+</button>'''
	html +=					'''</div>
						</div>'''
	for job in jobs_dict:
		html += cr.home_job_htmlify(job)
				
	html +=		'''</div>
				</div>
			</body>
		</html>'''
	return html

@app.route('/jobs/<string:job_id>')
def job_by_id(job_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_jobs_' + job_id)

	this_job = cr.jobs_jobs_query(job_id)
	contact_dict = cr.home_contact_query()

	html = cr.render_html_head('/jobs/'+job_id)
	html += cr.render_header(contact_dict['name'], session['name'], '/jobs', '/jobs/' + job_id, session)
	
	html += cr.jobs_jobs_htmlify(this_job)
	html += "</body></html>"
	return html

@app.route('/edus/<string:edu_id>')
def edu_by_id(edu_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_edus_' + edu_id)

	this_edu = cr.edus_edus_query(edu_id)
	contact_dict = cr.home_contact_query()
	
	html = cr.render_html_head('/edus/'+edu_id)
	html += cr.render_header(contact_dict['name'], session['name'], '/edus', '/edus/' + edu_id, session)
	
	html += cr.edus_edus_htmlify(this_edu)
	html += "</body></html>"
	return html

@app.route('/orgs/<string:org_id>')
def org_by_id(org_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_orgs_' + org_id)
		
	this_org = cr.orgs_orgs_query(org_id)
	contact_dict = cr.home_contact_query()
	
	html = cr.render_html_head('/orgs/'+org_id)
	html += cr.render_header(contact_dict['name'], session['name'], '/orgs', '/orgs/' + org_id, session)
	
	html += cr.org_htmlify(this_org['this'], this_org['next'], this_org['last'])
	html += '''	</div>
			</div>
			</body></html>'''
	
	return html

@app.route('/skills/<string:skill_id>')
def skill_by_id(skill_id):
	if session.get('username') == None:
		return redirect('/reauth?r=_skills_' + skill_id)
		
	this_skill = cr.skills_skills_query(skill_id)
	contact_dict = cr.home_contact_query()
	
	html = cr.render_html_head('/skills/'+skill_id)
	html += cr.render_header(contact_dict['name'], session['name'], '/skills', '/skills/' + skill_id, session)
	
	html += cr.skills_skills_htmlify(this_skill)
	
	return html

@app.route('/jobs')
def jobs_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_jobs')
	return redirect('/jobs/' + cr.jobs_jobs_general_query())

@app.route('/edus')
def edus_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_edus')
	return redirect('/edus/' + cr.edus_edus_general_query())

@app.route('/orgs')
def orgs_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_orgs')
	return redirect('/orgs/' + cr.orgs_orgs_general_query())

@app.route('/skills')
def skills_general():
	if session.get('username') == None:
		return redirect('/reauth?r=_skills')
		
	all_skills = cr.skills_skills_general_query()
	contact_dict = cr.home_contact_query()
	
	html = cr.render_html_head('/skills')
	html += cr.render_header(contact_dict['name'], session['name'], '/skills', '/skills', session)
	
	html += cr.skills_general_htmlify(all_skills)
	
	return html

@app.route('/about')
def about():
	if session.get('username') == None:
		return redirect('/reauth?r=_about')
	
	contact_dict = cr.home_contact_query()

	html = cr.render_html_head('/about')
	html += cr.render_header(contact_dict['name'], session['name'], '/about', '/about', session)
	html += cr.render_about(session)
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



if __name__ == '__main__':
	app.run(host='127.0.0.1',port='80',debug=True)