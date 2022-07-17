import os
import base64
import binascii
import codecs
import hashlib
import random
import sqlite3
import uuid
import datetime
import sys
from urllib.parse import urlencode

from flask import Flask, session, render_template, request, redirect

sys.path.append("models")
sys.path.append("views")
sys.path.append("controllers")

from mastercontroller import MasterController
from dbm import DBM
from accounts import NoneAccount
from addresses import retrieve_all_addresses, Address, NoneAddress
from contacts import NoneContact
from contactsrender import ContactRenderer
from jobsrender import JobRenderer
from jobs import Job, retrieve_all_jobs, jobs_date_sort, NoneJob, retrieve_jobs
from orgsrender import OrgRenderer
from orgs import Org, retrieve_all_orgs, NoneOrg, retrieve_orgs
from educations import Education, retrieve_all_educations, edus_date_sort, NoneEducation, retrieve_educations
from edusrender import EduRenderer
from skillsrender import SkillRenderer
from skills import retrieve_skills_custom, NoneSkill, Skill, retrieve_skills, retrieve_all_skills

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"
URL = 'http://resume.tomesser.biz'

class CRender:
	def __init__ (self, dbm):
		self.dbm = dbm
		self.mc = MasterController(dbm)
		self.contactrenderer = ContactRenderer(self.dbm)
		self.jobrenderer = JobRenderer(self.dbm)
		self.orgrenderer = OrgRenderer(self.dbm)
		self.edurenderer = EduRenderer(self.dbm)
		self.skillrenderer = SkillRenderer(self.dbm)



	"""
		HTML Conversion Methods
	"""

	def home_home_htmlify (self, contact, home_edus, home_jobs, session):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']

		html = ""
		html += self.contactrenderer.render_home_contact(contact, session['mobile'], auth)

		if not session['mobile']:
			html += '''
						<div class="row" style="width:75%;">
							<div class="col">
								<h2 class="mb-4">Education</h2>
							</div>
							<div class="col">'''
			if session.get('auth_key') != self.mc.auth_keys['Readers']:
				html +=	'''<a href="javascript:void(0)" data-toggle="modal" data-target="#addEduModal"><button style="position:relative;width:50px;margin-left:auto;margin-right:0;" type="button" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>'''
			html +=					'''</div>
						</div>
								'''
			for edu in home_edus:
				html += self.edurenderer.render_home_tile(edu, False, auth)
			html+=			'''
					<span style="display:inline-block;border-left:1px solid #ccc;height:100%;position:relative;top:-100%;left:90%;"></span>
					</div>

					<div class="col-sm-7">
						<div class="row" style="width:75%;">
							<div class="col">
								<h2 class="mb-4">Experience</h2>
							</div>
							<div class="col">'''
			if session.get('auth_key') != self.mc.auth_keys['Readers']:
				html +=	'''<a href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal"><button type="button" style="position:relative;width:50px;margin-left:auto;margin-right:0;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>'''
			html +=					'''</div>
								</div>'''
			for j in home_jobs:
				html += self.jobrenderer.render_home_tile(j, False, auth)

			html +=		'''</div>
						</div>
					</body>
				</html>'''

		else:
			html += '''	<div class="card w-100">
							<div class="card-header">
								<div class="row">
										<div class="col-8">
											<h4>Experience</h4>
										</div>
									<div class="col-4">
										'''
			if session.get('auth_key') != self.mc.auth_keys['Readers']:
					html +=	'''			<ul class="navbar-nav mr-auto" style="width:100%;">
											<li class="nav-item dropdown" style="width:100%;">
												<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown06" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">New</a>
												<div class="dropdown-menu", aria-labelledby="dropdown06">
													<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal">Job</a>
												</div>
											</li>
										</ul>
									'''
			html += '''				</div>
								</div>
							</div>
						</div>'''


			for j in home_jobs:
				html += self.jobrenderer.render_home_tile(j, True, auth)
			html += '''<div class="card w-100" style="width:100%;">
							<div class="card-header">
								<div class="row">
									<div class="col-8">
										<h4>Education</h4>
									</div>
								<div class="col-4">
										'''
			if session.get('auth_key') != self.mc.auth_keys['Readers']:
				html +=	'''			<ul class="navbar-nav mr-auto" style="width:100%;">
										<li class="nav-item dropdown" style="width:100%;">
											<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown05" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">New</a>
											<div class="dropdown-menu", aria-labelledby="dropdown05">
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addEduModal">Education</a>
											</div>
										</li>
									</ul>
									'''
			html += '''			</div>
							</div>
						</div>
					</div>'''


			for edu in home_edus:
				html += self.edurenderer.render_home_tile(edu, True, auth)
			html+=			'''

					</body>
				</html>'''

		return html

	def jobs_jobs_htmlify (self, jobs, mobile):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']
	
		html = self.orgrenderer.render_org_tile(mobile, auth, this_job=jobs[0], next_job=jobs[1], last_job=jobs[2])
		html += self.jobrenderer.render_job_page(jobs[0], jobs[1], jobs[2], mobile)

		return html

	def edus_edus_htmlify (self, edus, mobile):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']
	
		html = self.orgrenderer.render_org_tile(mobile, auth, this_edu=edus[0], next_edu=edus[1], last_edu=edus[2])
		html += self.edurenderer.render_edu_page(edus[0], edus[1], edus[2], mobile)

		return html

	def org_htmlify (self, orgs, mobile):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']
	
		return self.orgrenderer.render_org_tile(mobile, auth, this_org=orgs[0], next_org=orgs[1], last_org=orgs[2])

	def skills_general_htmlify (self, all_skills, mobile):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']
		return self.skillrenderer.render_skills_general(all_skills, mobile, auth)

	def skills_skills_htmlify (self, skill, mobile):
		auth = session.get('auth_key') != self.mc.auth_keys['Readers']
		html = self.skillrenderer.render_skills_page(skill[0], skill[1], skill[2], mobile, auth)
		return html

	def render_header (self, user, page, redirect, s):
		intact = self.dbm.is_intact()

		if not s['mobile']:
			html = 	'''
						<nav class="navbar navbar-expand navbar-dark bg-dark">
							<div style="padding-left:10px;">
								<a class="navbar-brand" href="/">
									<img src="/static/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
									<span style='position:relative;left:5px;'>Resume</span>
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
			if page == '/err':
				html += 			'''<li class="nav-item active">
											<a class="nav-link" href="/home">Error</a>
										</li>'''
			html += '''
								</ul>
								<div style="position:absolute;width:15%;left:84%;">
									<ul class="navbar-nav mr-auto">
										<li class="nav-item dropdown">
											<a class="nav-link dropdown-toggle" href="#" id="dropdown03" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Welcome, ''' + user + '''</a>
											<div class="dropdown-menu", aria-labelledby="dropdown03">
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#loginModal">Login</a>'''
			if s['auth_key'] == self.mc.auth_keys['Contributors'] or s['auth_key'] == self.mc.auth_keys['Owners']:
				html +=						'''<a class="dropdown-item" href="/logout?r='''+redirect.replace('/','_')+'''">Logout</a>'''
			html += '''
											</div>
										</li>
									</ul>
								</div>
							</div>
						</nav>
					'''
			if not intact:
				html += '''	<div class="alert alert-danger" role="alert" style="text-align:center;z-index:3;margin-bottom:-15px;">
								<b>Note:</b> The data in this site is not original data. Please click <a href="/restore?r=''' + redirect.replace('/','_') + '''">here</a> to restore resume data.
							</div>'''
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

									<img src="/static/logo.png" width="30" height="30" class="d-inline-block align-top" alt="" style="z-index:10;">'''
			if page == '/':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Home</a>'''
			elif page == '/jobs':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Jobs</a>'''
			elif page == '/edus':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Education</a>'''
			elif page == '/skills':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Skills</a>'''
			elif page == '/orgs':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Organizations</a>'''
			elif page == '/about':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">About</a>'''
			elif page == '/err':
				html += '''			<a class="nav-link dropdown-toggle" href="#" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="color:white;position:relative;top:-5px;z-index:10;">Error</a>'''

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
									<div style="position:absolute;margin-right:0;margin-left:auto;width:95%;margin-top:-5px;">
										<div style="margin-right:0;margin-left:auto;width:40%;">
											<ul class="navbar-nav mr-auto" style="width:100%;position:relative;">
												<li class="nav-item dropdown" style="width:100%;">
													<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown03" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">Welcome, ''' + user + '''</a>
													<div class="dropdown-menu", aria-labelledby="dropdown03">
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#loginModal">Login</a>'''
			if s['auth_key'] == self.mc.auth_keys['Contributors'] or s['auth_key'] == self.mc.auth_keys['Owners']:
				html +=									'''<a class="dropdown-item" href="/logout?r='''+redirect.replace('/','_')+'''">Logout</a>'''
			html += '''
													</div>
												</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</nav>
					'''
			if not intact:
				html += '''	<div class="alert alert-danger" role="alert" style="margin-bottom:-5px;">
								<div class="col-sm-8 mx-auto">
									<b>Note:</b> The data in this site is not original data. Please click <a href="/restore?r=''' + redirect.replace('/','_') + '''">here</a> to restore resume data.
								</div>
							</div>'''

		return html

	def render_html_head (self, redirect, mobile):
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
						<link rel="shortcut icon" href="static/favicon.ico">
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
												<input type="text" name="username" id="username" value="member" required></input><br><br>
											</div>
										</div>
										<div class="row">
											<div class="col-sm-10 mx-auto">
												<input type="password" name="password" id="password" value="member" required></input>
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

						<div class="modal fade" id="addJobModal" tabindex="-1" role="dialog" aria-labelledby="addJobModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
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
												<input id="title" type="text" name="title" placeholder="Job title" required></input><br><br>
											</div>
											<div class="col-sm-6 mx-auto">
												<label for="present">Present Job</label><br>
												<input id="present" type="checkbox" name="present"></input><br><br>
											</div>
										</div>
										<div class="row">
											<div class="col-sm-6">
												<label for="date_start">Start Date</label><br>
												<input id="date_start" type="date" name="date_start" value="'''+now.strftime("%Y-%m-%d")+'''" required></input><br><br>
											</div>
											<div class="col-sm-6">
												<label for="date_stop">Stop Date</label><br>
												<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
											</div>
										</div>

										<div class="row">
											<div class="col-sm-6 mx-auto">
												<label for="desc_short">Short Description</label><br>
												<textarea name="desc_short" form="create_job" placeholder="Short description of job." style="width:95%;height:100px;" required></textarea>
											</div>
											<div class="col-sm-6 mx-auto">
												<label for="desc_long">Long Description</label><br>
												<textarea name="desc_long" form="create_job" placeholder="Long description of job." style="width:95%;height:100px;" required></textarea>
											</div>
										</div><br>
										<div class="row">
											<div class="col-sm-6 mx-auto">
												<label for="skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label><br>'''
			all_skills = self.mc.skills_for_add_query()
			html += '''								<select style="min-width:95%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="''' + s.id + '''">'''+ s.name + '''</option>'''
			html+= '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" id="job_add_skill_button" onClick="job_add_skill(0, 0)">Add Skill</button>
												</div>


													<div class="col-sm-6 mx-auto">
														<label for="org_select">Select Organization</label><br>'''
			all_orgs = self.mc.orgs_for_add_query()
			html += '''									<select style="min-width:95%;" size="6" id="org_selector" name="org_selector" required>'''
			for o in all_orgs:
				html += '''									<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: job_add_org()">Add Organization</button>
													</div>
											</div>
											<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<input type="hidden" name="job_add_skills_i" id="job_add_skills_i" value="False"></input>
											<input type="hidden" name="job_max_skills" id="job_max_skills" value="0"></input>
											<input type="hidden" name="job_add_org_i" id="job_add_org_i" value="False"></input>
											<input type="hidden" name="job_add_address_i" id="job_add_address_i" value="False"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
											<hr>
											<div class="container" id="job_new_org_parent" style="visibility:hidden;height:0px;">
												<div class="row">
													<h6>Add New Organization</h6>
												</div>
												<hr>
												<div class="container" id="job_add_org_div">
													<div class="row">
														<button type="button" class="close", onClick="javascript: job_remove_org()" style="margin-left:auto;margin-right:0;">
															<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="j_o_name">Name</label><br>
															<input type="text" name="j_o_name" id="j_o_name" placeholder="Oragnization name"></input>
														</div>
														<div class="col-6">
															<label for="j_o_phone">Phone number</label><br>
															<input type="text" name="j_o_phone" id="j_o_phone" placeholder="555-555-5555"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="j_o_website">Website</label><br>
															<input type="text" name="j_o_website" id="j_o_website" placeholder="Website URL"></input>
														</div>
														<div class="col-6">
															<label for="j_o_desc_short">Description</label><br>
															<textarea name="j_o_desc_short" id="j_o_desc_short" form="create_job" placeholder="Description of organization" style="width:95%;height:100px;" ></textarea>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="j_o_icon">Icon Image</label>
															<input type="file" onChange="upload_img('j_o_icon')"  name="j_o_icon" id="j_o_icon" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="j_o_icon_val" id="j_o_icon_val"></input>
														</div>
														<div class="col-6">
															<label for="j_o_header">Header Image</label>
															<input type="file" onChange="upload_img('j_o_header')"  name="j_o_header" id="j_o_header" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="j_o_header_val" id="j_o_header_val" value=""></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="j_o_address_selector">Address</label>'''
			all_addresses = retrieve_all_addresses(self.dbm)
			html += '''										<select style="min-width:95%;max-width:95%;" size="4" id="j_o_address_selector" name="j_o_address_selector">'''
			for a in all_addresses:
				html += '''									<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''										</select>
															<br><br>
															<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: job_new_address()">Add Address</button>
														</div>
														<div class="col-6">
															<div id="job_new_address_div" style="visibility:hidden; height:0px; left:0px;">
																<button type="button" class="close", onClick="javascript: job_remove_address()" style="margin-left:auto;margin-right:0;">
																<span aria-hidden="true">&times;</span>
																</button>
																<br>
																<label for="j_o_new_address">New Address</label>
																<input type="text" name="j_o_new_address" id="j_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
															</div>
														</div>
													</div>
												</div>
											</div>
											<hr>
											<div class="container" id="job_new_skill_parent" style="visibility:hidden;height:0px;">
												<div class="row">
													<h6>Add New Skill(s)</h6>
												</div>
												<hr>
												<div class="container" id="job_add_skill_div">


												</div>
												<hr>
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


							<div class="modal fade" id="addEduModal" tabindex="-1" role="dialog" aria-labelledby="addEduModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
								  <div class="modal-header">
									<h5 class="modal-title" id="addEduModal">New Education</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/create/edu' method='post' id="create_edu">
									  <div class="modal-body">
											<div class="row">
												<div class="col-sm-4 mx-auto">
													<label for="title">Degree</label><br>
													<input id="title" type="text" name="degree" placeholder="Degree" required></input>
												</div>
												<div class="col-sm-4">
													<label for="title">GPA</label><br>
													<input id="title" type="text" name="gpa" placeholder="GPA" required></input>
												</div>
												<div class="col-sm-4">
													<label for="date_stop">Graduation Date</label><br>
													<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''" required></input>
												</div>
											</div><br>

											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="desc_short">Short Description</label><br>
													<textarea name="desc_short" form="create_edu" placeholder="Short description of education." style="width:95%;height:100px;" required></textarea>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="desc_long">Long Description</label><br>
													<textarea name="desc_long" form="create_edu" placeholder="Long description of education." style="width:95%;height:100px;" required></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label><br>'''
			all_skills = self.mc.skills_for_add_query()
			html += '''								<select style="min-width:95%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="''' + s.id + '''">''' + s.name + '''</option>'''
			html+= '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" id="edu_add_skill_button" onClick="edu_add_skill(0, 0)">Add Skill</button>
												</div>


													<div class="col-sm-6 mx-auto">
														<label for="edu_org_selector">Select Organization</label><br>'''
			all_orgs = self.mc.orgs_for_add_query()
			html += '''									<select style="min-width:95%;" size="6" id="edu_org_selector" name="edu_org_selector" required>'''
			for o in all_orgs:
				html += '''									<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: edu_add_org()">Add Organization</button>
														</div>
												</div>
												<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
												<div class="row">
													<div class="col-sm-10 mx-auto">
														<input type="submit" value="Submit" style="display:none">
													</div>
												</div>
												<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<input type="hidden" name="edu_add_skills_i" id="edu_add_skills_i" value="False"></input>
											<input type="hidden" name="edu_max_skills" id="edu_max_skills" value="0"></input>
											<input type="hidden" name="edu_add_org_i" id="edu_add_org_i" value="False"></input>
											<input type="hidden" name="edu_add_address_i" id="edu_add_address_i" value="False"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
											<hr>
											<div class="container" id="edu_new_org_parent" style="visibility:hidden;height:0px;">
												<div class="row">
													<h6>Add New Organization</h6>
												</div>
												<hr>
												<div class="container" id="edu_add_org_div">
													<div class="row">
														<button type="button" class="close", onClick="javascript: edu_remove_org()" style="margin-left:auto;margin-right:0;">
															<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="e_o_name">Name</label><br>
															<input type="text" name="e_o_name" id="e_o_name" placeholder="Oragnization name"></input>
														</div>
														<div class="col-6">
															<label for="e_o_phone">Phone number</label><br>
															<input type="text" name="e_o_phone" id="e_o_phone" placeholder="555-555-5555"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="e_o_website">Website</label><br>
															<input type="text" name="e_o_website" id="e_o_website" placeholder="Website URL"></input>
														</div>
														<div class="col-6">
															<label for="e_o_desc_short">Description</label><br>
															<textarea name="e_o_desc_short" id="e_o_desc_short" form="create_edu" placeholder="Description of organization" style="width:95%;height:100px;" ></textarea>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="e_o_icon">Icon Image</label>
															<input type="file" onChange="upload_img('e_o_icon')"  name="e_o_icon" id="e_o_icon" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="e_o_icon_val" id="e_o_icon_val"></input>
														</div>
														<div class="col-6">
															<label for="e_o_header">Header Image</label>
															<input type="file" onChange="upload_img('e_o_header')"  name="e_o_header" id="e_o_header" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="e_o_header_val" id="e_o_header_val" value=""></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-6">
															<label for="e_o_address_selector">Address</label>'''
			all_addresses = retrieve_all_addresses(self.dbm)
			html += '''										<select style="min-width:95%;max-width:95%;" size="4" id="e_o_address_selector" name="e_o_address_selector">'''
			for a in all_addresses:
				html += '''									<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''										</select>
															<br><br>
															<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: edu_new_address()">Add Address</button>
														</div>
														<div class="col-6">
															<div id="edu_new_address_div" style="visibility:hidden; height:0px; left:0px;">
																<button type="button" class="close", onClick="javascript: edu_remove_address()" style="margin-left:auto;margin-right:0;">
																<span aria-hidden="true">&times;</span>
																</button>
																<br>
																<label for="e_o_new_address">New Address</label>
																<input type="text" name="e_o_new_address" id="e_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
															</div>
														</div>
													</div>
												</div>
											</div>
												<hr>
												<div class="container" id="edu_new_skill_parent" style="visibility:hidden;height:0px;">
													<div class="row">
														<h6>Add New Skill(s)</h6>
													</div>
													<hr>
													<div class="container" id="edu_add_skill_div">


													</div>
													<hr>
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


							<div class="modal fade" id="editEduModal" tabindex="-1" role="dialog" aria-labelledby="editEduModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
								  <div class="modal-header">
									<h5 class="modal-title" id="editEduModal">Edit Education</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/update/edu' method='post' id="update_edu">
										<input type="hidden" id="e_e_id" name="e_e_id" value=""></input>
										<div class="container" id="edu_edit_div">
											<div class="row" style="padding-top:15px;">
												<div class="col-4">
													<label for="e_e_degree">Degree</label><br>
													<input id="e_e_degree" name="e_e_degree" type="text" value=""></input>
												</div>
												<div class="col-4">
													<label for="e_e_gpa">GPA</label><br>
													<input id="e_e_gpa" name="e_e_gpa" type="text" value=""></input>
												</div>
												<div class="col-4">
													<label for="e_e_date_stop">Graduation Date</label><br>
													<input id="e_e_date_stop" name="e_e_date_stop" type="date" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_e_desc_short">Short Description</label><br>
													<textarea name="e_e_desc_short" form="update_edu" id="e_e_desc_short" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
												<div class="col-6">
													<label for="e_e_desc_long">Long Description</label><br>
													<textarea name="e_e_desc_long" form="update_edu" id="e_e_desc_long" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_e_skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_e_skill_selector" name="e_e_skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option id="e_e_''' + s.id + '''" value="''' + s.id + '''">''' + s.name + '''</option>'''
			html+= '''								</select>
												</div>
												<div class="col-6">
													<label for="e_e_org_selector">Select Organization</label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_e_org_selector" name="e_e_org_selector">'''
			for o in all_orgs:
				html += '''								<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''								</select>
												</div>
											</div>
										</div>
										<br>
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

							<!-- Job Edit Popup -->
							<div class="modal fade" id="editJobModal" tabindex="-1" role="dialog" aria-labelledby="editJobModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
								  <div class="modal-header">
									<h5 class="modal-title" id="editJobModal">Edit Work Experience</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/update/job' method='post' id="update_job">
										<input type="hidden" id="e_j_id" name="e_j_id" value=""></input>
										<div class="container" id="edu_edit_div">
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_j_title">Title</label><br>
													<input id="e_j_title" name="e_j_title" type="text" value=""></input>
												</div>
												<div class="col-6">
													<label for="e_j_present">Present</label><br>
													<input id="e_j_present" name="e_j_present" type="checkbox" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_j_date_start">Start Date</label><br>
													<input id="e_j_date_start" name="e_j_date_start" type="date" value=""></input>
												</div>
												<div class="col-6">
													<label for="e_j_date_stop">Stop Date</label><br>
													<input id="e_j_date_stop" name="e_j_date_stop" type="date" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_j_desc_short">Short Description</label><br>
													<textarea name="e_j_desc_short" form="update_job" id="e_j_desc_short" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
												<div class="col-6">
													<label for="e_j_desc_long">Long Description</label><br>
													<textarea name="e_j_desc_long" form="update_job" id="e_j_desc_long" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_j_skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_j_skill_selector" name="e_j_skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option id="e_e_''' + s.id + '''" value="''' + s.id + '''">''' + s.name + '''</option>'''
			html+= '''								</select>
												</div>
												<div class="col-6">
													<label for="e_j_org_selector">Select Organization</label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_j_org_selector" name="e_j_org_selector">'''
			for o in all_orgs:
				html += '''								<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''								</select>
												</div>
											</div>
										</div>
										<br>
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
							
							<!-- Edu Delete Popup -->
							<div class="modal fade" id="delEduModal" tabindex="-1" role="dialog" aria-labelledby="delEduModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="delEduModal">Delete Education</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/edu' method='post' id="delete_edu">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the education entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-6">
													<label for="d_e_id">Education ID</label><br>
													<input type="text" id="d_e_id" name="d_e_id" value="" style="width:90%;" disabled required></input>
												</div>
												<div class="col-6">
													<label for="d_e_degree">Degree</label><br>
													<input type="text" id="d_e_degree" name="d_e_degree" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										<div class="container" id="d_e_dangle_org" >
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this education will leave the below organization dangling with no referenced activity:
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="d_e_oid">Organization ID</label><br>
													<input type="text" id="d_e_oid" name="d_e_oid" value="" style="width:90%;" disabled></input>
												</div>
												<div class="col-6">
													<label for="d_e_oname">Name</label><br>
													<input type="text" id="d_e_oname" name="d_e_oname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_e_del_org" style="padding-top:5px;">Do you want to delete this organization as well?</label>
													<select id="d_e_del_org" name="d_e_del_org" style="position:relative; left:10px;">
														<option id="d_e_del_org_n" name="d_e_del_org_n" value="false">No</option>
														<option id="d_e_del_org_y" name="d_e_del_org_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										<hr>
										</div>
										<div class="container" id="d_e_dangle_addr" style="visibility:hidden;display:none;">
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="d_e_aid">Address ID</label><br>
													<input type="text" id="d_e_aid" name="d_e_aid" value="" style="width:90%;" disabled></input>
												</div>
												<div class="col-6">
													<label for="d_e_aname">Name</label><br>
													<input type="text" id="d_e_aname" name="d_e_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_e_del_addr" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_e_del_addr" name="d_e_del_addr" style="position:relative; left:10px;">
														<option id="d_e_del_addr_n" name="d_e_del_addr_n" value="false">No</option>
														<option id="d_e_del_addr_y" name="d_e_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_edu_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Job Delete Popup -->
							<div class="modal fade" id="delJobModal" tabindex="-1" role="dialog" aria-labelledby="delJobModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="delJobModal">Delete Work Experience</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/job' method='post' id="delete_job">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the job entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-6">
													<label for="d_j_id">Job ID</label><br>
													<input type="text" id="d_j_id" name="d_j_id" value="" style="width:90%;" disabled required></input>
												</div>
												<div class="col-6">
													<label for="d_j_title">Title</label><br>
													<input type="text" id="d_j_title" name="d_j_title" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										<div class="container" id="d_j_dangle_org" >
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this job will leave the below organization dangling with no referenced activity:
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="d_j_oid">Organization ID</label><br>
													<input type="text" id="d_j_oid" name="d_j_oid" value="" style="width:90%;" disabled></input>
												</div>
												<div class="col-6">
													<label for="d_j_oname">Name</label><br>
													<input type="text" id="d_j_oname" name="d_j_oname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_j_del_org" style="padding-top:5px;">Do you want to delete this organization as well?</label>
													<select id="d_j_del_org" name="d_j_del_org" style="position:relative; left:10px;">
														<option id="d_j_del_org_n" name="d_j_del_org_n" value="false">No</option>
														<option id="d_j_del_org_y" name="d_j_del_org_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										<hr>
										</div>
										<div class="container" id="d_j_dangle_addr" style="visibility:hidden;display:none;">
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="d_j_aid">Address ID</label><br>
													<input type="text" id="d_j_aid" name="d_j_aid" value="" style="width:90%;" disabled></input>
												</div>
												<div class="col-6">
													<label for="d_j_aname">Name</label><br>
													<input type="text" id="d_j_aname" name="d_j_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_j_del_addr" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_j_del_addr" name="d_j_del_addr" style="position:relative; left:10px;">
														<option id="d_j_del_addr_n" name="d_j_del_addr_n" value="false">No</option>
														<option id="d_j_del_addr_y" name="d_j_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_job_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Contact Edit Popup -->
							<div class="modal fade" id="editContactModal" tabindex="-1" role="dialog" aria-labelledby="editContactModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="editContactModal">Edit Contact Information</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/contact' method='post' id="update_contact">
									<input type="hidden" id="e_c_id" name="e_c_id" value=""></input>
										<div class="container" style="position:relative;left:10px;">
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_c_name">Name</label><br>
													<input type="text" id="e_c_name" name="e_c_name" value="" required></input>
												</div>
												<div class="col-6">
													<label for="e_c_phone1">Phone A</label><br>
													<input type="text" id="e_c_phone1" name="e_c_phone1" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_c_email">Email</label><br>
													<input type="text" id="e_c_email" name="e_c_email" value="" required></input>
												</div>
												<div class="col-6">
													<label for="e_c_phone2">Phone B</label><br>
													<input type="text" id="e_c_phone2" name="e_c_phone2" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<input type="hidden" id="contact_add_address_i" name="contact_add_address_i" value="False"></input>
													<label for="e_c_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="e_c_address_selector" name="e_c_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: contact_new_address()">Add Address</button>
												</div>
												<div class="col-6">
													<label for="e_c_objective">Objective</label><br>
													<textarea name="e_c_objective" form="update_contact" id="e_c_objective" value="" style="width:95%; min-height:100px;" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<div id="contact_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: contact_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="e_c_new_address">New Address</label>
														<input type="text" name="e_c_new_address" id="e_c_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Add org Popup -->
							<div class="modal fade" id="addOrgModal" tabindex="-1" role="dialog" aria-labelledby="addOrgModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="addOrgModal">Add Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/create/org' method='post' id="create_org">
										<div class="container">
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="a_o_name">Name</label><br>
													<input type="text" id="a_o_name" name="a_o_name" placeholder="Organization Name" required></input>
												</div>
												<div class="col-6">
													<label for="a_o_phone">Phone Number</label><br>
													<input type="text" id="a_o_phone" name="a_o_phone" placeholder="5555555555" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="a_o_website">Website</label><br>
													<input type="text" id="a_o_website" name="a_o_website" placeholder="Website URL" required></input>
												</div>
												<div class="col-6">
													<label for="a_o_desc_short">Description</label><br>
													<textarea name="a_o_desc_short" form="create_org" id="a_o_desc_short" value="" style="width:95%; min-height:100px;" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="a_o_icon">Icon Image</label>
													<input type="file" onChange="upload_img('a_o_icon')"  name="a_o_icon" id="a_o_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="a_o_icon_val" id="a_o_icon_val"></input>
												</div>
												<div class="col-6">
													<label for="a_o_header">Header Image</label>
													<input type="file" onChange="upload_img('a_o_header')"  name="a_o_header" id="a_o_header" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="a_o_header_val" id="a_o_header_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<input type="hidden" id="org_add_address_i" name="org_add_address_i" value="False"></input>
													<label for="a_o_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="a_o_address_selector" name="a_o_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: org_new_address()">Add Address</button>
												</div>
												<div class="col-6">
													<div id="org_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: org_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="a_o_new_address">New Address</label>
														<input type="text" name="a_o_new_address" id="a_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Edit org Popup -->
							<div class="modal fade" id="editOrgModal" tabindex="-1" role="dialog" aria-labelledby="editOrgModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="editOrgModal">Edit Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/org' method='post' id="update_org">
										<input type="hidden" name="e_oo_id" id="e_oo_id" value=""></input>
										<div class="container">
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_oo_name">Name</label><br>
													<input type="text" id="e_oo_name" name="e_oo_name" placeholder="Organization Name" value="" required></input>
												</div>
												<div class="col-6">
													<label for="e_oo_phone">Phone Number</label><br>
													<input type="text" id="e_oo_phone" name="e_oo_phone" placeholder="5555555555" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_oo_website">Website</label><br>
													<input type="text" id="e_oo_website" name="e_oo_website" placeholder="Website URL" value="" required></input>
												</div>
												<div class="col-6">
													<label for="e_oo_desc_short">Description</label><br>
													<textarea name="e_oo_desc_short" form="update_org" id="e_oo_desc_short" value="" style="width:95%; min-height:100px;" value="" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="e_oo_icon">Icon Image</label>
													<input type="file" onChange="upload_img('e_oo_icon')"  name="e_oo_icon" id="e_oo_icon" accept="image/png, image/jpeg" value="Current"></input>
													<input type="hidden" name="e_oo_icon_val" id="e_oo_icon_val" value=""></input>
												</div>
												<div class="col-6">
													<label for="e_o_header">Header Image</label>
													<input type="file" onChange="upload_img('e_oo_header')"  name="e_oo_header" id="e_oo_header" accept="image/png, image/jpeg" value="Current"></input>
													<input type="hidden" name="e_oo_header_val" id="e_oo_header_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:5px;">
												<div class="col-6">
													<img id="e_oo_img1" height="40" src="" style="display:none;"/> 
												</div>
												<div class="col-6">
													<img id="e_oo_img2" height="40" src="" style="display:none;"/> 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<input type="hidden" id="org_edit_address_i" name="org_edit_address_i" value="False"></input>
													<label for="e_oo_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="e_oo_address_selector" name="e_oo_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: e_org_new_address()">Add Address</button>
												</div>
												<div class="col-6">
													<div id="e_org_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: e_org_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="e_oo_new_address">New Address</label>
														<input type="text" name="e_oo_new_address" id="e_oo_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Org Delete Popup -->
							<div class="modal fade" id="delOrgModal" tabindex="-1" role="dialog" aria-labelledby="delOrgModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="delOrgModal">Delete Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/org' method='post' id="delete_org">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the organization entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-6">
													<label for="d_o_id">Organiation ID</label><br>
													<input type="text" id="d_o_id" name="d_o_id" value="" style="width:90%;" disabled required></input>
												</div>
												<div class="col-6">
													<label for="d_o_name">Name</label><br>
													<input type="text" id="d_o_name" name="d_o_name" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										
										<div class="container" id="d_o_dangle_addr" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-6">
													<label for="d_o_aid">Address ID</label><br>
													<input type="text" id="d_o_aid" name="d_o_aid" value="" style="width:90%;" disabled></input>
												</div>
												<div class="col-6">
													<label for="d_o_aname">Name</label><br>
													<input type="text" id="d_o_aname" name="d_o_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_o_del_addr" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_o_del_addr" name="d_o_del_addr" style="position:relative; left:10px;">
														<option id="d_o_del_addr_n" name="d_o_del_addr_n" value="false">No</option>
														<option id="d_o_del_addr_y" name="d_o_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<div class="container" id="d_o_dangle_jobs" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below jobs with no referenced organization - please choose alternate organizations for each:
												</div>
												<hr style="width:90%;left:5%;">
											</div>
											<div class="container" id="d_o_dangle_jobs_list">
											
											</div>
										</div>
										<div class="container" id="d_o_dangle_edus" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below education with no referenced organization - please choose alternate organizations for each:
												</div>
												<hr style="width:90%;left:5%;">
											</div>
											<div class="container" id="d_o_dangle_edus_list">
												
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_org_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Skill Add Popup -->
							<div class="modal fade" id="addSkillModal" tabindex="-1" role="dialog" aria-labelledby="addSkillModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="addSkillModal">New Skill</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/create/skill' method='post' id="create_skill">
										<div class="modal-body">
											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="s_a_name">Skill Name</label><br>
													<input type="text" name="s_a_name" id="s_a_name" placeholder="Skill name" required></input>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="s_a_exposure">Skill Exposure</label><br>
													<select name="s_a_exposure" id="s_a_exposure" required>
														<option value="0">0</option>
														<option value="1">1</option>
														<option value="2">2</option>
														<option value="3">3</option>
														<option value="4">4</option>
														<option value="5">5</option>
														<option value="6">6</option>
														<option value="7">7</option>
														<option value="8">8</option>
														<option value="9">9</option>
														<option value="10">10</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto">
													<label for="s_a_soh">Soft Skill</label><br>
													<select name="s_a_soh" id="s_a_soh" required>
														<option value="True">True</option>
														<option value="False">False</option>
													</select>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="s_a_reference">Reference site</label><br>
													<input type="text" name="s_a_reference" id="s_a_reference" placeholder="https://reference.com"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto>
													<label for="s_a_icon">Icon Image</label><br>
													<input type="file" onChange="upload_img('s_a_icon')"  name="s_a_icon" id="s_a_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="s_a_icon_val" id="s_a_icon_val" value=""></input>
												</div>
												<div class="col-sm-6 mx-auto>
													<label for="s_a_category">Skill Category</label><br>
													<input type="text" id="s_a_category" name="s_a_category" placeholder="ex. Software"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto>
													<label for="s_a_desc_short">Description</label><br>
													<textarea name="s_a_desc_short" form="create_skill" id="s_a_desc_short" value="" style="width:95%; min-height:100px;" placeholder="A short description of what the skill is." value="" required></textarea>
												</div>
												<div class="col-sm-6 mx-auto>
													<label for="s_a_desc_long">Commentary</label><br>
													<textarea name="s_a_desc_long" form="create_skill" id="s_a_desc_long" value="" style="width:95%; min-height:100px;" placeholder="A short description on how you've used this skill." value="" required></textarea>
												</div>
											</div>
										</div>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Edit Skill Popup -->
							<div class="modal fade" id="editSkillModal" tabindex="-1" role="dialog" aria-labelledby="editSkillModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="editSkillModal">Edit Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/skill' method='post' id="update_skill">
										<input type="hidden" name="s_e_id" id="s_e_id" value=""></input>
										<div class="modal-body">
											<div class="row">
												<div class="col-sm-6 mx-auto">
													<label for="s_e_name">Skill Name</label><br>
													<input type="text" style="width:95%;" name="s_e_name" id="s_e_name" placeholder="Skill name" required></input>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="s_e_exposure">Skill Exposure</label><br>
													<select name="s_e_exposure" id="s_e_exposure" required>
														<option value="0">0</option>
														<option value="1">1</option>
														<option value="2">2</option>
														<option value="3">3</option>
														<option value="4">4</option>
														<option value="5">5</option>
														<option value="6">6</option>
														<option value="7">7</option>
														<option value="8">8</option>
														<option value="9">9</option>
														<option value="10">10</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto">
													<label for="s_e_soh">Soft Skill</label><br>
													<select name="s_e_soh" id="s_e_soh" required>
														<option value="True">True</option>
														<option value="False">False</option>
													</select>
												</div>
												<div class="col-sm-6 mx-auto">
													<label for="s_e_reference">Reference site</label><br>
													<input type="text" style="width:95%;"  name="s_e_reference" id="s_e_reference" placeholder="https://reference.com"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto>
													<label for="s_e_icon">Icon Image</label><br>
													<input type="file" onChange="upload_img('s_e_icon')"  name="s_e_icon" id="s_e_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="s_e_icon_val" id="s_e_icon_val" value=""></input>
												</div>
												<div class="col-sm-6 mx-auto>
													<label for="s_e_category">Skill Category</label><br>
													<input type="text" style="width:95%;"  id="s_e_category" name="s_e_category" placeholder="ex. Software"></input>
												</div>
											</div>
											<div class="row" style="padding-top:5px;">
												<div class="col-6">
													<img id="s_e_icon_img" height="40" src="" style="display:none;"/> 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-6 mx-auto>
													<label for="s_e_desc_short">Description</label><br>
													<textarea name="s_e_desc_short" form="update_skill" id="s_e_desc_short" value="" style="width:95%; min-height:100px;" placeholder="A short description of what the skill is." value="" required></textarea>
												</div>
												<div class="col-sm-6 mx-auto>
													<label for="s_e_desc_long">Commentary</label><br>
													<textarea name="s_e_desc_long" form="update_skill" id="s_e_desc_long" value="" style="width:95%; min-height:100px;" placeholder="A short description on how you've used this skill." value="" required></textarea>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Skill Delete Popup -->
							<div class="modal fade" id="delSkillModal" tabindex="-1" role="dialog" aria-labelledby="delSkillModal" aria-hidden="true" style="position:fixed; width:50%; left:25%; top:15%; height:75%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" style="position:absolute; width:150%; left:-25%;">
									<div class="modal-header">
										<h5 class="modal-title" id="delSkillModal">Delete Skill</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/skill' method='post' id="delete_skill">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the skill entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-6">
													<label for="s_d_id">Skill ID</label><br>
													<input type="text" id="s_d_id" name="s_d_id" value="" style="width:90%;" disabled required></input>
												</div>
												<div class="col-6">
													<label for="s_d_name">Name</label><br>
													<input type="text" id="s_d_name" name="s_d_name" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										
										<div class="container" id="s_d_job_dels" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this skill will remove it from the below work expereience(s): 
												</div>
											</div>
											<div class="container" id="s_d_jobs">
												
											</div>
										</div>
										<div class="container" id="s_d_edu_dels" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this skill will remove it from the below education expereience(s): 
												</div>
											</div>
											<div class="container" id="s_d_edus">
												
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_skill_enable()"></button>
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
													<input id="title" type="text" name="title" placeholder="Job title" required></input><br><br>
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
													<input id="date_start" type="date" name="date_start" value="'''+now.strftime("%Y-%m-%d")+'''" required></input><br><br>
												</div>
												<div class="col-sm-6">
													<label for="date_stop">Stop Date</label><br>
													<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''"></input><br><br>
												</div>
											</div>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="desc_short">Short Description</label><br>
													<textarea name="desc_short" form="create_job" placeholder="Short description of job." required></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="desc_long">Long Description</label><br>
													<textarea name="desc_long" form="create_job" placeholder="Long description of job." required></textarea>
												</div>
											</div><br>
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="skill_selector">Select Skills</label><br>'''
			all_skills = self.mc.skills_for_add_query()
			html += '''								<select "style=width:100%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="'''+s.id+'''">'''+s.name+'''</option>'''
			html+= '''								</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" id="job_add_skill_button" onClick="job_add_skill(0, 1)">Add Skill</button>
												</div>
											</div><br>
											<div class="row">
													<div class="col-sm-12 mx-auto">
														<label for="org_select">Select Organization</label><br>'''
			all_orgs = self.mc.orgs_for_add_query()
			html += '''									<select "style=width:100%;" size="6" id="org_selector" name="org_selector" required>'''
			for o in all_orgs:
				html += '''									<option value="'''+o.id+'''">'''+o.name+'''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: job_add_org()">Add Organization</button>
													</div>
											</div>
											<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<input type="hidden" name="job_add_skills_i" id="job_add_skills_i" value="False"></input>
											<input type="hidden" name="job_max_skills" id="job_max_skills" value="0"></input>
											<input type="hidden" name="job_add_org_i" id="job_add_org_i" value="False"></input>
											<input type="hidden" name="job_add_address_i" id="job_add_address_i" value="False"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
											<hr>
											<div class="container" id="job_new_org_parent" style="visibility:hidden;height:0px;">
												<div class="row">
													<h6>Add New Organization</h6>
												</div>
												<hr>
												<div class="container" id="job_add_org_div">
													<div class="row">
														<button type="button" class="close", onClick="javascript: job_remove_org()" style="margin-left:auto;margin-right:0;">
															<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_name">Name</label><br>
															<input type="text" name="j_o_name" id="j_o_name" placeholder="Oragnization name"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_phone">Phone number</label><br>
															<input type="text" name="j_o_phone" id="j_o_phone" placeholder="555-555-5555"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_website">Website</label><br>
															<input type="text" name="j_o_website" id="j_o_website" placeholder="Website URL"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_desc_short">Description</label><br>
															<textarea name="j_o_desc_short" id="j_o_desc_short" form="create_job" placeholder="Description of organization" style="width:95%;height:100px;" ></textarea>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_icon">Icon Image</label>
															<input type="file" onChange="upload_img('j_o_icon')"  name="j_o_icon" id="j_o_icon" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="j_o_icon_val" id="j_o_icon_val"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_header">Header Image</label>
															<input type="file" onChange="upload_img('j_o_header')"  name="j_o_header" id="j_o_header" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="j_o_header_val" id="j_o_header_val" value=""></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<label for="j_o_address_selector">Address</label>'''
			all_addresses = retrieve_all_addresses(self.dbm)
			html += '''										<select style="min-width:95%;max-width:95%;" size="4" id="j_o_address_selector" name="j_o_address_selector">'''
			for a in all_addresses:
				html += '''									<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''										</select>
															<br><br>
															<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: job_new_address()">Add Address</button>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-12">
															<div id="job_new_address_div" style="visibility:hidden; height:0px; left:0px;">
																<button type="button" class="close", onClick="javascript: job_remove_address()" style="margin-left:auto;margin-right:0;">
																<span aria-hidden="true">&times;</span>
																</button>
																<br>
																<label for="j_o_new_address">New Address</label>
																<input type="text" name="j_o_new_address" id="j_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
															</div>
														</div>
													</div>
												</div>
											</div>
											<hr>
	  									  	<div class="container" id="job_new_skill_parent" style="visibility:hidden;height:0px;">
	  										  <div class="row">
	  											  <h6>Add New Skill(s)</h6>
	  										  </div>
	  										  <hr>
	  										  <div class="container" id="job_add_skill_div">


	  										  </div>
	  										  <hr>
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


							<div class="modal fade" id="addEduModal" tabindex="-1" role="dialog" aria-labelledby="addEduModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content">
								  <div class="modal-header">
									<h5 class="modal-title" id="addEduModal">New Education</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/create/edu' method='post' id="create_edu">
									  <div class="modal-body">
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="title">Degree</label><br>
													<input id="title" type="text" name="degree" placeholder="Degree" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="title">GPA</label><br>
													<input id="title" type="text" name="gpa" placeholder="GPA" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="date_stop">Graduation Date</label><br>
													<input id="date_stop" type="date" name="date_stop" value="'''+now.strftime("%Y-%m-%d")+'''" required></input>
												</div>
											</div><br>

											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="desc_short">Short Description</label><br>
													<textarea name="desc_short" form="create_edu" placeholder="Short description of education." style="width:95%;height:100px;" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="desc_long">Long Description</label><br>
													<textarea name="desc_long" form="create_edu" placeholder="Long description of education." style="width:95%;height:100px;" required></textarea>
												</div>
											</div><br>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="skill_selector">Select Skills</label><br>'''
			all_skills = self.mc.skills_for_add_query()
			html += '''								<select style="min-width:95%;" size="6" id="skill_selector" name="skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option value="''' + s.id + '''">''' + s.name + '''</option>'''
			html+= '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" id="edu_add_skill_button" onClick="edu_add_skill(0, 0)">Add Skill</button>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
													<div class="col-sm-12 mx-auto">
														<label for="edu_org_selector">Select Organization</label><br>'''
			all_orgs = self.mc.orgs_for_add_query()
			html += '''									<select style="min-width:95%;" size="6" id="edu_org_selector" name="edu_org_selector" required>'''
			for o in all_orgs:
				html += '''									<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: edu_add_org()">Add Organization</button>
														</div>
												</div>
												<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
												<div class="row">
													<div class="col-sm-10 mx-auto">
														<input type="submit" value="Submit" style="display:none">
													</div>
												</div>
												<input type="hidden" name="redirect" id="redirect" value="'''+redirect+'''"></input>
											<input type="hidden" name="edu_add_skills_i" id="edu_add_skills_i" value="False"></input>
											<input type="hidden" name="edu_max_skills" id="edu_max_skills" value="0"></input>
											<input type="hidden" name="edu_add_org_i" id="edu_add_org_i" value="False"></input>
											<input type="hidden" name="edu_add_address_i" id="edu_add_address_i" value="False"></input>
											<div class="row">
												<div class="col-sm-10 mx-auto">
													<input type="submit" value="Submit" style="display:none">
												</div>
											</div>
											<hr>
											<div class="container" id="edu_new_org_parent" style="visibility:hidden;height:0px;">
												<div class="row">
													<h6>Add New Organization</h6>
												</div>
												<hr>
												<div class="container" id="edu_add_org_div">
													<div class="row">
														<button type="button" class="close", onClick="javascript: edu_remove_org()" style="margin-left:auto;margin-right:0;">
															<span aria-hidden="true">&times;</span>
														</button>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_name">Name</label><br>
															<input type="text" name="e_o_name" id="e_o_name" placeholder="Oragnization name"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_phone">Phone number</label><br>
															<input type="text" name="e_o_phone" id="e_o_phone" placeholder="555-555-5555"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_website">Website</label><br>
															<input type="text" name="e_o_website" id="e_o_website" placeholder="Website URL"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_desc_short">Description</label><br>
															<textarea name="e_o_desc_short" id="e_o_desc_short" form="create_edu" placeholder="Description of organization" style="width:95%;height:100px;" ></textarea>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_icon">Icon Image</label>
															<input type="file" onChange="upload_img('e_o_icon')"  name="e_o_icon" id="e_o_icon" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="e_o_icon_val" id="e_o_icon_val"></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_header">Header Image</label>
															<input type="file" onChange="upload_img('e_o_header')"  name="e_o_header" id="e_o_header" accept="image/png, image/jpeg"></input>
															<input type="hidden" name="e_o_header_val" id="e_o_header_val" value=""></input>
														</div>
													</div>
													<div class="row" style="padding-top:15px;">
														<div class="col-sm-12 mx-auto">
															<label for="e_o_address_selector">Address</label>'''
			all_addresses = retrieve_all_addresses(self.dbm)
			html += '''										<select style="min-width:95%;max-width:95%;" size="4" id="e_o_address_selector" name="e_o_address_selector">'''
			for a in all_addresses:
				html += '''									<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''										</select>
															<br><br>
															<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: edu_new_address()">Add Address</button>
														</div>
													</div>
													<div class="row">
														<div class="col-sm-12 mx-auto">
															<div id="edu_new_address_div" style="visibility:hidden; height:0px; left:0px;">
																<button type="button" class="close", onClick="javascript: edu_remove_address()" style="margin-left:auto;margin-right:0;">
																<span aria-hidden="true">&times;</span>
																</button>
																<br>
																<label for="e_o_new_address">New Address</label>
																<input type="text" name="e_o_new_address" id="e_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
															</div>
														</div>
													</div>
												</div>
											</div>
												<hr>
												<div class="container" id="edu_new_skill_parent" style="visibility:hidden;height:0px;">
													<div class="row">
														<h6>Add New Skill(s)</h6>
													</div>
													<hr>
													<div class="container" id="edu_add_skill_div">


													</div>
													<hr>
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
							<div class="modal fade" id="editEduModal" tabindex="-1" role="dialog" aria-labelledby="editEduModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content">
									 <div class="modal-header">
										<h5 class="modal-title" id="editEduModal">Edit Education</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									  </div>
									  <form action='/update/edu' method='post' id="update_edu">
											<input type="hidden" id="e_e_id" name="e_e_id" value=""></input>
											<div class="container" id="edu_edit_div">
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_degree">Degree</label><br>
														<input id="e_e_degree" name="e_e_degree" type="text" value=""></input>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_gpa">GPA</label><br>
														<input id="e_e_gpa" name="e_e_gpa" type="text" value=""></input>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_date_stop">Graduation Date</label><br>
														<input id="e_e_date_stop" name="e_e_date_stop" type="date" value=""></input>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_desc_short">Short Description</label><br>
														<textarea name="e_e_desc_short" form="update_edu" id="e_e_desc_short" value="" style="width:95%; min-height:100px;"></textarea>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_desc_long">Long Description</label><br>
														<textarea name="e_e_desc_long" form="update_edu" id="e_e_desc_long" value="" style="width:95%; min-height:100px;"></textarea>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_skill_selector">Select Skills</label>
														<select style="min-width:95%;max-width:95%;" size="6" id="e_e_skill_selector" name="e_e_skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option id="e_e_''' + s.id + '''" value="''' + s.id + '''">''' + s.name + '''	</option>'''
			html+= '''								</select>
													</div>
												</div>
												<div class="row" style="padding-top:15px;">
													<div class="col-12">
														<label for="e_e_org_selector">Select Organization</label>
														<select style="min-width:95%;max-width:95%;" size="6" id="e_e_org_selector" name="e_e_org_selector">'''
			for o in all_orgs:
				html += '''								<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''									</select>
													</div>
												</div>
											</div>
											<br>
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

							<!-- Job Edit Popup -->
							<div class="modal fade" id="editJobModal" tabindex="-1" role="dialog" aria-labelledby="editJobModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content">
									 <div class="modal-header">
										<h5 class="modal-title" id="editJobModal">Edit Work Experience</h5>

									<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
									  <span aria-hidden="true">&times;</span>
									</button>
								  </div>
								  <form action='/update/job' method='post' id="update_job">
										<input type="hidden" id="e_j_id" name="e_j_id" value=""></input>
										<div class="container" id="edu_edit_div">
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_title">Title</label><br>
													<input id="e_j_title" name="e_j_title" type="text" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_present">Present</label><br>
													<input id="e_j_present" name="e_j_present" type="checkbox" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_date_start">Start Date</label><br>
													<input id="e_j_date_start" name="e_j_date_start" type="date" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_date_stop">Stop Date</label><br>
													<input id="e_j_date_stop" name="e_j_date_stop" type="date" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_desc_short">Short Description</label><br>
													<textarea name="e_j_desc_short" form="update_job" id="e_j_desc_short" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_desc_long">Long Description</label><br>
													<textarea name="e_j_desc_long" form="update_job" id="e_j_desc_long" value="" style="width:95%; min-height:100px;"></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_j_skill_selector">Select Skills <i>(CTRL + Click for multiple)</i></label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_j_skill_selector" name="e_j_skill_selector" multiple>'''
			for s in all_skills:
				html +=	'''								<option id="e_e_''' + s.id + '''" value="''' + s.id + '''">''' + s.name + '''</option>'''
			html+= '''								</select>
												</div>
												<div class="col-12">
													<label for="e_j_org_selector">Select Organization</label>
													<select style="min-width:95%;max-width:95%;" size="6" id="e_j_org_selector" name="e_j_org_selector">'''
			for o in all_orgs:
				html += '''								<option value="''' + o.id + '''">''' + o.name + '''</option>'''
			html += '''								</select>
												</div>
											</div>
										</div>
										<br>
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
							
							<!-- Edu Delete Popup -->
							<div class="modal fade" id="delEduModal" tabindex="-1" role="dialog" aria-labelledby="delEduModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="delEduModal">Delete Education</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/edu' method='post' id="delete_edu">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the education entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-12">
													<label for="d_e_id">Education ID</label><br>
													<input type="text" id="d_e_id" name="d_e_id" value="" style="width:90%;" disabled required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_e_degree">Degree</label><br>
													<input type="text" id="d_e_degree" name="d_e_degree" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										<div class="container" id="d_e_dangle_org" >
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this education will leave the below organization dangling with no referenced activity:
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_e_oid">Organization ID</label><br>
													<input type="text" id="d_e_oid" name="d_e_oid" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_e_oname">Name</label><br>
													<input type="text" id="d_e_oname" name="d_e_oname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_e_del_org" style="padding-top:5px;">Do you want to delete this organization as well?</label>
													<select id="d_e_del_org" name="d_e_del_org" style="position:relative; left:10px;">
														<option id="d_e_del_org_n" name="d_e_del_org_n" value="false">No</option>
														<option id="d_e_del_org_y" name="d_e_del_org_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										<hr>
										</div>
										<div class="container" id="d_e_dangle_addr" style="visibility:hidden;display:none;">
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_e_aid">Address ID</label><br>
													<input type="text" id="d_e_aid" name="d_e_aid" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_e_aname">Name</label><br>
													<input type="text" id="d_e_aname" name="d_e_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_e_del_org" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_e_del_addr" name="d_e_del_addr" style="position:relative; left:10px;">
														<option id="d_e_del_addr_n" name="d_e_del_addr_n" value="false">No</option>
														<option id="d_e_del_addr_y" name="d_e_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_edu_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Job Delete Popup -->
							<div class="modal fade" id="delJobModal" tabindex="-1" role="dialog" aria-labelledby="delJobModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="delJobModal">Delete Work Experience</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/job' method='post' id="delete_job">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the job entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-12">
													<label for="d_j_id">Job ID</label><br>
													<input type="text" id="d_j_id" name="d_j_id" value="" style="width:90%;" disabled required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_j_title">Title</label><br>
													<input type="text" id="d_j_title" name="d_j_title" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										<div class="container" id="d_j_dangle_org" >
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this job will leave the below organization dangling with no referenced activity:
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_j_oid">Organization ID</label><br>
													<input type="text" id="d_j_oid" name="d_j_oid" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_j_oname">Name</label><br>
													<input type="text" id="d_j_oname" name="d_j_oname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_j_del_org" style="padding-top:5px;">Do you want to delete this organization as well?</label>
													<select id="d_j_del_org" name="d_j_del_org" style="position:relative; left:10px;">
														<option id="d_j_del_org_n" name="d_j_del_org_n" value="false">No</option>
														<option id="d_j_del_org_y" name="d_j_del_org_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										<hr>
										</div>
										<div class="container" id="d_j_dangle_addr" style="visibility:hidden;display:none;">
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_j_aid">Address ID</label><br>
													<input type="text" id="d_j_aid" name="d_j_aid" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_j_aname">Name</label><br>
													<input type="text" id="d_j_aname" name="d_j_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_j_del_addr" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_j_del_addr" name="d_j_del_addr" style="position:relative; left:10px;">
														<option id="d_j_del_addr_n" name="d_j_del_addr_n" value="false">No</option>
														<option id="d_j_del_addr_y" name="d_j_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_job_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Contact Edit Popup -->
							<div class="modal fade" id="editContactModal" tabindex="-1" role="dialog" aria-labelledby="editContactModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="editContactModal">Edit Contact Information</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/contact' method='post' id="update_contact">
									<input type="hidden" id="e_c_id" name="e_c_id" value=""></input>
										<div class="container" style="position:relative;left:10px;">
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_c_name">Name</label><br>
													<input type="text" id="e_c_name" name="e_c_name" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_c_phone1">Phone A</label><br>
													<input type="text" id="e_c_phone1" name="e_c_phone1" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_c_phone2">Phone B</label><br>
													<input type="text" id="e_c_phone2" name="e_c_phone2" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_c_email">Email</label><br>
													<input type="text" id="e_c_email" name="e_c_email" value="" required></input>
												</div>
											</div>
											
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_c_objective">Objective</label><br>
													<textarea name="e_c_objective" form="update_contact" id="e_c_objective" value="" style="width:95%; min-height:100px;" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<input type="hidden" id="contact_add_address_i" name="contact_add_address_i" value="False"></input>
													<label for="e_c_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="e_c_address_selector" name="e_c_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''									</select>
														<br><br>
														<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: contact_new_address()">Add Address</button>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<div id="contact_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: contact_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="e_c_new_address">New Address</label>
														<input type="text" name="e_c_new_address" id="e_c_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Add org Popup -->
							<div class="modal fade" id="addOrgModal" tabindex="-1" role="dialog" aria-labelledby="addOrgModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="addOrgModal">Add Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/create/org' method='post' id="create_org">
										<div class="container">
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_name">Name</label><br>
													<input type="text" id="a_o_name" name="a_o_name" placeholder="Organization Name" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_phone">Phone Number</label><br>
													<input type="text" id="a_o_phone" name="a_o_phone" placeholder="5555555555" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_website">Website</label><br>
													<input type="text" id="a_o_website" name="a_o_website" placeholder="Website URL" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_desc_short">Description</label><br>
													<textarea name="a_o_desc_short" form="create_org" id="a_o_desc_short" value="" style="width:95%; min-height:100px;" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_icon">Icon Image</label>
													<input type="file" onChange="upload_img('a_o_icon')"  name="a_o_icon" id="a_o_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="a_o_icon_val" id="a_o_icon_val"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="a_o_header">Header Image</label>
													<input type="file" onChange="upload_img('a_o_header')"  name="a_o_header" id="a_o_header" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="a_o_header_val" id="a_o_header_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<input type="hidden" id="org_add_address_i" name="org_add_address_i" value="False"></input>
													<label for="a_o_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="a_o_address_selector" name="a_o_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: org_new_address()">Add Address</button>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<div id="org_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: org_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="a_o_new_address">New Address</label>
														<input type="text" name="a_o_new_address" id="a_o_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Edit org Popup -->
							<div class="modal fade" id="editOrgModal" tabindex="-1" role="dialog" aria-labelledby="editOrgModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="editOrgModal">Edit Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/org' method='post' id="update_org">
										<input type="hidden" name="e_oo_id" id="e_oo_id" value=""></input>
										<div class="container">
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_oo_name">Name</label><br>
													<input type="text" id="e_oo_name" name="e_oo_name" placeholder="Organization Name" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_oo_phone">Phone Number</label><br>
													<input type="text" id="e_oo_phone" name="e_oo_phone" placeholder="5555555555" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_oo_website">Website</label><br>
													<input type="text" id="e_oo_website" name="e_oo_website" placeholder="Website URL" value="" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_oo_desc_short">Description</label><br>
													<textarea name="e_oo_desc_short" form="update_org" id="e_oo_desc_short" value="" style="width:95%; min-height:100px;" value="" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_oo_icon">Icon Image</label>
													<input type="file" onChange="upload_img('e_oo_icon')"  name="e_oo_icon" id="e_oo_icon" accept="image/png, image/jpeg" value="Current"></input>
													<input type="hidden" name="e_oo_icon_val" id="e_oo_icon_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:5px;">
												<div class="col-12">
													<img id="e_oo_img1" height="40" src="" style="display:none;"/> 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="e_o_header">Header Image</label>
													<input type="file" onChange="upload_img('e_oo_header')"  name="e_oo_header" id="e_oo_header" accept="image/png, image/jpeg" value="Current"></input>
													<input type="hidden" name="e_oo_header_val" id="e_oo_header_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<img id="e_oo_img2" height="40" src="" style="display:none;"/> 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<input type="hidden" id="org_edit_address_i" name="org_edit_address_i" value="False"></input>
													<label for="e_oo_address_selector">Address</label><br>
													<select style="min-width:95%;max-width:95%;" size="4" id="e_oo_address_selector" name="e_oo_address_selector" required>'''
			for a in all_addresses:
				html += '''								<option value="''' + a.id + '''">''' + a.name +'''</option>'''
			html += '''								</select>
													<br><br>
													<button type="button" class="btn btn-success btn-lg btn-block" style="width:80%;position:relative;left:7.5%;" onClick="javascript: e_org_new_address()">Add Address</button>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<div id="e_org_new_address_div" style="visibility:hidden; height:0px; left:0px;">
														<button type="button" class="close", onClick="javascript: e_org_remove_address()" style="margin-left:auto;margin-right:0;">
														<span aria-hidden="true">&times;</span>
														</button>
														<br>
														<label for="e_oo_new_address">New Address</label>
														<input type="text" name="e_oo_new_address" id="e_oo_new_address" placeholder="123 Street Ave, City, State 12345" style="width:95%;"></input>
													</div>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Org Delete Popup -->
							<div class="modal fade" id="delOrgModal" tabindex="-1" role="dialog" aria-labelledby="delOrgModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="delOrgModal">Delete Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/org' method='post' id="delete_org">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the organization entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-12">
													<label for="d_o_id">Organiation ID</label><br>
													<input type="text" id="d_o_id" name="d_o_id" value="" style="width:90%;" disabled required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_o_name">Name</label><br>
													<input type="text" id="d_o_name" name="d_o_name" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										
										<div class="container" id="d_o_dangle_addr" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below address dangling with no referenced organization: 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_o_aid">Address ID</label><br>
													<input type="text" id="d_o_aid" name="d_o_aid" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-12">
													<label for="d_o_aname">Name</label><br>
													<input type="text" id="d_o_aname" name="d_o_aname" value="" style="width:90%;" disabled></input>
												</div>
											</div>
											<div class="row" style="padding-top:25px;">
												<div class="col-12">
													<label for="d_o_del_addr" style="padding-top:5px;">Do you want to delete this address as well?</label>
													<select id="d_o_del_addr" name="d_o_del_addr" style="position:relative; left:10px;">
														<option id="d_o_del_addr_n" name="d_o_del_addr_n" value="false">No</option>
														<option id="d_o_del_addr_y" name="d_o_del_addr_y" value="true">Yes</option>
													</select>
												</div>
											</div>
										</div>
										<div class="container" id="d_o_dangle_jobs" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below jobs with no referenced organization - please choose alternate organizations for each:
												</div>
												<hr style="width:90%;left:5%;">
											</div>
											<div class="container" id="d_o_dangle_jobs_list">
											
											</div>
										</div>
										<div class="container" id="d_o_dangle_edus" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this organization will leave the below education with no referenced organization - please choose alternate organizations for each:
												</div>
												<hr style="width:90%;left:5%;">
											</div>
											<div class="container" id="d_o_dangle_edus_list">
											
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_org_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Skill Add Popup -->
							<div class="modal fade" id="addSkillModal" tabindex="-1" role="dialog" aria-labelledby="addSkillModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="addSkillModal">New Skill</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/create/skill' method='post' id="create_skill">
										<div class="modal-body">
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_name">Skill Name</label><br>
													<input type="text" name="s_a_name" id="s_a_name" style="width:95%;" placeholder="Skill name" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_exposure">Skill Exposure</label><br>
													<select name="s_a_exposure" id="s_a_exposure" required>
														<option value="0">0</option>
														<option value="1">1</option>
														<option value="2">2</option>
														<option value="3">3</option>
														<option value="4">4</option>
														<option value="5">5</option>
														<option value="6">6</option>
														<option value="7">7</option>
														<option value="8">8</option>
														<option value="9">9</option>
														<option value="10">10</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_soh">Soft Skill</label><br>
													<select name="s_a_soh" id="s_a_soh" required>
														<option value="True">True</option>
														<option value="False">False</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_reference">Reference site</label><br>
													<input type="text" name="s_a_reference" id="s_a_reference" style="width:95%;"  placeholder="https://reference.com"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_icon">Icon Image</label><br>
													<input type="file" onChange="upload_img('s_a_icon')"  name="s_a_icon" id="s_a_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="s_a_icon_val" id="s_a_icon_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_category">Skill Category</label><br>
													<input type="text" id="s_a_category" name="s_a_category" style="width:95%;" placeholder="ex. Software"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_desc_short">Description</label><br>
													<textarea name="s_a_desc_short" form="create_skill" id="s_a_desc_short" value="" style="width:95%; min-height:100px;" placeholder="A short description of what the skill is." value="" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_a_desc_long">Commentary</label><br>
													<textarea name="s_a_desc_long" form="create_skill" id="s_a_desc_long" value="" style="width:95%; min-height:100px;" placeholder="A short description on how you've used this skill." value="" required></textarea>
												</div>
											</div>
										</div>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Edit Skill Popup -->
							<div class="modal fade" id="editSkillModal" tabindex="-1" role="dialog" aria-labelledby="editSkillModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="editSkillModal">Edit Organization</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/update/skill' method='post' id="update_skill">
										<input type="hidden" name="s_e_id" id="s_e_id" value=""></input>
										<div class="modal-body">
											<div class="row">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_name">Skill Name</label><br>
													<input type="text" style="width:95%;" name="s_e_name" id="s_e_name" placeholder="Skill name" required></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_exposure">Skill Exposure</label><br>
													<select name="s_e_exposure" id="s_e_exposure" required>
														<option value="0">0</option>
														<option value="1">1</option>
														<option value="2">2</option>
														<option value="3">3</option>
														<option value="4">4</option>
														<option value="5">5</option>
														<option value="6">6</option>
														<option value="7">7</option>
														<option value="8">8</option>
														<option value="9">9</option>
														<option value="10">10</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_soh">Soft Skill</label><br>
													<select name="s_e_soh" id="s_e_soh" required>
														<option value="True">True</option>
														<option value="False">False</option>
													</select>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_reference">Reference site</label><br>
													<input type="text" style="width:95%;"  name="s_e_reference" id="s_e_reference" placeholder="https://reference.com"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_icon">Icon Image</label><br>
													<input type="file" onChange="upload_img('s_e_icon')"  name="s_e_icon" id="s_e_icon" accept="image/png, image/jpeg"></input>
													<input type="hidden" name="s_e_icon_val" id="s_e_icon_val" value=""></input>
												</div>
											</div>
											<div class="row" style="padding-top:5px;">
												<div class="col-sm-12 mx-auto">
													<img id="s_e_icon_img" height="40" src="" style="display:none;"/> 
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_category">Skill Category</label><br>
													<input type="text" style="width:95%;"  id="s_e_category" name="s_e_category" placeholder="ex. Software"></input>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_desc_short">Description</label><br>
													<textarea name="s_e_desc_short" form="update_skill" id="s_e_desc_short" value="" style="width:95%; min-height:100px;" placeholder="A short description of what the skill is." value="" required></textarea>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-12 mx-auto">
													<label for="s_e_desc_long">Commentary</label><br>
													<textarea name="s_e_desc_long" form="update_skill" id="s_e_desc_long" value="" style="width:95%; min-height:100px;" placeholder="A short description on how you've used this skill." value="" required></textarea>
												</div>
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-primary" value="Save & Close"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
							
							<!-- Skill Delete Popup -->
							<div class="modal fade" id="delSkillModal" tabindex="-1" role="dialog" aria-labelledby="delSkillModal" aria-hidden="true" style="position:fixed; top:5%; width:80%; left:10%; height:90%;" >
							<div class="modal-dialog" role="document">
								<div class="modal-content" >
									<div class="modal-header">
										<h5 class="modal-title" id="delSkillModal">Delete Skill</h5>

										<button type="button" class="close" data-dismiss="modal" data-toggle="modal" aria-label="Close">
										  <span aria-hidden="true">&times;</span>
										</button>
									</div>
									<form action='/delete/skill' method='post' id="delete_skill">	
										<div class="container">
											<div class="row">
												<div class="col-12 d-flex align-items-center" style="margin-top:20px;">
													<h6>Are you really sure you want to delete the skill entry with the below data?</h6>
												</div>
											</div>
											<hr>
											<div class="row">
												<div class="col-12">
													<label for="s_d_id">Skill ID</label><br>
													<input type="text" id="s_d_id" name="s_d_id" value="" style="width:90%;" disabled required></input>
												</div>
											</div>
											<div class="row">
												<div class="col-12" style="padding-top:15px;">
													<label for="s_d_name">Name</label><br>
													<input type="text" id="s_d_name" name="s_d_name" value="" style="width:90%;" disabled></input>
												</div>
											</div>
										</div>
										
										<div class="container" id="s_d_job_dels" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this skill will remove it from the below work expereience(s): 
												</div>
											</div>
											<div class="container" id="s_d_jobs">
												
											</div>
										</div>
										<div class="container" id="s_d_edu_dels" style="visibility:hidden;display:none;">
											<hr>
											<div class="row">
												<div class="col-12">
													Deleting this skill will remove it from the below education expereience(s): 
												</div>
											</div>
											<div class="container" id="s_d_edus">
												
											</div>
										</div>
										<br>
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">
											  <span aria-hidden="true">Cancel</span>
											</button>
											<input type="submit" class="btn btn-danger" value="Delete & Close" onClick="del_skill_enable()"></button>
										</div>
									</form>
								</div>
							</div>
							</div>
						'''
		return html

	def render_about (self, session):
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
														and digitize my resume in a palatable manner. <br><br>

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
							<div id="accordion">
								<div class="row">
									<div class="col-sm-10 mx-auto">
										<div class="card">
											<div class="card-header" id="headingOne">
											  <h5>
												<button class="btn" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne" style="padding-top:15px;"><h5>
												  Development Roadmap</h5>
												</button>
											  
											</div>
											 <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
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
															<span class="badge badge-pill badge-info">In Progress</span>
														</div>
													</div>
													<div class="row" style="padding-left:45px;">
														<p style="text-decoration:line-through;">Add long descriptions to education and work experience.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p style="text-decoration:line-through;">Circle back on implementation of custom 404 pages and error handling on queries on non-existant data.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p style="text-decoration:line-through;">Extend compatibility by implementing independent view controllers for mobile platforms.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p style="text-decoration:line-through;">Implement controllers for data integrity - allow for reversion to actual resume data when present state is altered by a guest.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p style="text-decoration:line-through;">Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p style="text-decoration:line-through;">Extend the application into a full RESTful API to GET any resume data via JSON.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-success">Completed</span>
														</div>
													</div>
													<div class="row" style="padding-left:45px;">
														<p>Add api documentation.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-info">In Progress</span>
														</div>
													</div>
													<div class="row" style="padding-left:15px;">
														<p>Extend the application into a full RESTful API to perform any of the other CRUD operations on the resume data.</p>
														<div style="padding-left:10px;position:relative;top:3px;">
															<span class="badge badge-pill badge-info">In Progress</span>
														</div>
													</div>
												</div>
											</div>
										</div>
										<div class="card">
											<div class="card-header" id="headingTwo">
											  <h5>
												<button class="btn" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo" style="padding-top:15px;"><h5>
												  API Use</h5>
												</button>
											  
											</div>
											 <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
												<div class="card-body">
													<div id="accordion2">
														<div class="card">
															<div class="card-header" id="h1">
															  <h5>
																<button class="btn" data-toggle="collapse" data-target="#c1" aria-expanded="true" aria-controls="c1" style="padding-top:15px;"><h6>
																  Strict Get</h6>
																</button>
															  
															</div>
														</div>
														<div class="card-body">
															<div id="c1" class="collapse" aria-labelledby="h1" data-parent="#accordion2">
																<div class="row">
																	<div class="col-1">
																		<b>Description</b>
																	</div>
																	<div class="col-5">
																		Used to get any set of resume data matching specified parameters on a strict equality basis. 
																	</div>
																	<div class="col-1">
																		<b>Endpoint</b>
																	</div>
																	<div class="col-5">
																		http://resume.tomesser.biz/api/get/<i>{model}</i>
																	</div>
																</div><hr><br>
																<div class="row">
																	<div class="col-3">
																		<b>Required Parameters</b>
																	</div>
																	<div class="col-5">
																	
																	</div>
																</div><br>
																<div class="row">
																	<div class="col-1">
																	</div>
																	<div class="col-11">
																		<div class="row">
																			<table class="table">
																			<thead>
																			<tr>
																			<th scope="col">Parameter</th>
																			<th scope="col">Description</th>
																			<th scope="col">Possible Values</th>
																			<th scope="col">Example</th>
																			</tr>
																			</thead>
																			<tbody>
																			<tr>
																			<td>model</td>
																			<td>Specifies which data model to query in the get request.</td>
																			<td><i>jobs, edus, orgs, addresses, skills</td>
																			<td><i>To retrieve all jobs with no specified filtering criteria</i>:<br><a target="_blank" href="/api/get/jobs">''' + URL + '''/api/get/jobs</a>
																			</tr>
																			</tbody>
																			</table>
																		</div>
																	</div>
																</div><hr><br>
																<div class="row">
																	<div class="col-3">
																		<b>Optional Paramters</b>
																	</div>
																</div><br>
																<div class="row">
																	<div class="col-1"></div>
																	<div class="col-11">
																		<div class="row">
																			<table class="table">
																			<thead>
																			<tr>
																			<th scope="col">Model Scope</th>
																			<th scope="col">Parameter</th>
																			<th scope="col">Description</th>
																			<th scope="col">Example</th>
																			</tr>
																			</thead>
																			<tbody>
																			<tr>
																			<th scope="row">All models</th>
																			<td>id</td>
																			<td>Specifies the id of the model object to retrieve in the request.</td>
																			<td><i>To query the jobs models for an instance with an id of "68922a46-d53b49d7-b22ce9b4-d0f7b5fe"</i>:<br><a target="_blank" href="/api/get/jobs?id=68922a46-d53b49d7-b22ce9b4-d0f7b5fe">''' + URL + '''/api/get/jobs?id=68922a46-d53b49d7-b22ce9b4-d0f7b5fe</a></td>
																			</tr>
																			<tr>
																			<th scope="row">addresses, skills, orgs</th>
																			<td>name</td>
																			<td>Specifies the name of the address, skill, or org to retrieve in the request.</td>
																			<td><i>To query the skills models for an instance with the name of "Programming"</i>:<br><a target="_blank" href="/api/get/skills?name=Programming">'''+URL+'''/api/get/skills?name=Programming</td>
																			</tr>
																			<tr>
																			<th scope="row">orgs, jobs, skills, edus</th>
																			<td>desc_short</td>
																			<td>Specifies the short description of the model object to retrieve in the request.</td>
																			<td><i>To query an org with a short description of "Test"</i>:<br><a target="_blank" href="/api/get/orgs?desc_short=Test">'''+URL+'''/api/get/orgs?desc_short=Test</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, skills, edus</th>
																			<td>desc_long</td>
																			<td>Specifies the long description of the model object to retrieve in the request.</td>
																			<td><i>To query an edu with a short description of "Test"</i>:<br><a target="_blank" href="/api/get/edus?desc_long=Test">'''+URL+'''/api/get/edus?desc_long=Test</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, orgs, edus</th>
																			<td>aid</td>
																			<td>Specifies the address id underlying an org. The org may be underlying a job or an edu.</td>
																			<td><i>To query an job with an underlying org that has an underlying address id of "1"</i>:<br><a target="_blank" href="/api/get/jobs?aid=1">'''+URL+'''/api/get/jobs?aid=1</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, orgs, edus</th>
																			<td>aname</td>
																			<td>Specifies the address id underlying an org. The org may be underlying a job or an edu.</td>
																			<td><i>To query a job that has an underlying org with an underlying address name of "515 Eastern Ave, Allegan, MI 49010"</i>:<br><a target="_blank" href="/api/get/jobs?aname=515 Eastern Ave, Allegan, MI 49010">'''+URL+'''/api/get/jobs?aname=515%20Eastern%20Ave,%20Allegan,%20MI%2049010</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>skill_ids</td>
																			<td>Specifies a number of skill_ids that are underlying either a job or edu.</td>
																			<td><i>To query an edu with underlying skill_ids of "f8481972-a7e44ecf-9322a5ef-8ff66a1e,df09ea12-80be422d-8701b975-240a3c7a,ebde125d-8c32410a-a7fea526-b4679de3"</i>:<br><a target="_blank" href="/api/get/edus?skill_ids=f8481972-a7e44ecf-9322a5ef-8ff66a1e,df09ea12-80be422d-8701b975-240a3c7a,ebde125d-8c32410a-a7fea526-b4679de3">'''+URL+'''/api/get/jobs?skill_ids=f8481972-a7e44ecf-9322a5ef-8ff66a1e,df09ea12-80be422d-8701b975-240a3c7a,ebde125d-8c32410a-a7fea526-b4679de3</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>oid</td>
																			<td>Specifies the org id of an org underlying a job or an edu.</td>
																			<td><i>To query a job with an underlying org that has an id of "4bbf911f-cccb471e-9d683a4e-173cf89b"</i>:<br><a target="_blank" href="/api/get/jobs?oid=4bbf911f-cccb471e-9d683a4e-173cf89b">'''+URL+'''/api/get/jobs?oid=4bbf911f-cccb471e-9d683a4e-173cf89b</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>oname</td>
																			<td>Specifies the org name of an org underlying a job or an edu.</td>
																			<td><i>To query an edu with an underlying org that has a name of "Western Michigan University"</i>:<br><a target="_blank" href="/api/get/edus?oname=Western%20Michigan%20University">'''+URL+'''/api/get/edus?oname=Western%20Michigan%20University</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>ophone</td>
																			<td>Specifies the org phone number of an org underlying a job or an edu. Phone numbers should have no formatting characters and be 10-digit numbers.</td>
																			<td><i>To query an edu with an underlying org that has a phone number of of "5177968425"</i>:<br><a target="_blank" href="/api/get/edus?ophone=5177968425">'''+URL+'''/api/get/edus?ophone=5177968425</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>odesc_short</td>
																			<td>Specifies the short description of an org underlying a job or an edu.</td>
																			<td><i>To query an edu with an underlying org that has a short description of "Test"</i>:<br><a target="_blank" href="/api/get/edus?odesc_short=Test">'''+URL+'''/api/get/edus?odesc_short=Test</td>
																			</tr>
																			<tr>
																			<th scope="row">jobs, edus</th>
																			<td>owebsite</td>
																			<td>Specifies the org website of an org underlying a job or an edu.</td>
																			<td><i>To query a job with an underlying org that has a website of "https://www.perrigo.com/"</i>:<br><a target="_blank" href="/api/get/jobs?owebsite=https://www.perrigo.com/">'''+URL+'''/api/get/jobs?owebsite=https://www.perrigo.com/</td>
																			</tr>
																			</tbody>
																			</table>
																		</div>
																	</div>
																</div><hr>
															</div>
														</div>
													</div>
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
												<div class="col-sm-12 mx-auto" style="display:flex; justify-content:center;align-items:center;">
													<img  src="/static/logo.png" width="50" height="50"/>
												</div>
											</div>
											<div class="row" style="padding-top:15px;">
												<div class="col-sm-9">
														This is a site I have developed myself with the intention of gaining some further
														exposure to several frameworks and technologies, showcase my technical proficiencies,
														and digitize my resume in a palatable manner. <br><br>

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
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Add skill commentary.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Add long descriptions to education and work experience.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Circle back on implementation of custom 404 pages and error handling on queries on non-existant data.</p>
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
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Implement controllers for data integrity - allow for reversion to actual resume data when present state is altered by a guest.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-success">Completed</span>
												</div>
												<div class="col-sm-8">
													<p style="text-decoration:line-through;">Extend the application into a full RESTful API to GET any resume data via JSON.</p>
												</div>
											</div>
											<div class="row" style="padding-left:45px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Add api documentation.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-info">In Progress</span>
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

	def render_err (self, session, resource):
		if not session['mobile']:
			html = '''	<div class="jumbotron">
							<div style="position:relative;left:12.5%;">
								<div class="card w-75">
									<div class="card-body">
										<ul class="list-group list-group-flush">
											<li class="list-group-item">
												<h1>404 Error</h1>
												<h6>We were unable to locate the requested resource.</h6><br>
												<p>It looks like you were attempting to access a
												"''' + resource + '''" that does not exist. You can try again or feel free to check out the below similar resources that do exist.</p>
												<p>Or return <a href="/home">Home</a>.
											</li>
											<li class="list-group-item">
												<h3>''' + resource + '''s</h3>'''
			if resource == 'Job':
				similar = self.mc.home_jobs_query()
				uri = '/jobs'
			elif resource == 'Education':
				similar = self.mc.home_edu_query()
				uri = '/edus'
			elif resource == 'Organization':
				similar = self.mc.orgs_for_add_query()
				if len(similar) == 0:
					similar = None
				else:
					similar = similar[:4]
				uri = '/orgs'
			elif resource == 'Skill':
				similar = self.mc.skills_for_add_query()
				if len(similar) == 0:
					similar = None
				else:
					similar = similar[:6]
				uri = '/skills'
			else:
				similar = None
			if similar == None:
				html +=	'''						<p><i>We couldn't find any similar resources. Perhaps you need to login as a member to add one?</i><p>
												<p>Or feel free to return to <a href='/home'>Home</a>.'''
			else:
				html += '''						<div class="row">'''
				for s in similar:
					if resource == 'Job':
						name = s.title
					elif resource == 'Education':
						name = s.degree
					elif resource == 'Organization':
						name = s.name
					elif resource == 'Skill':
						name = s.name
					else:
						name = "Unknown resource"
					html += '''						<div class="col-sm-6">
														<a href="''' + uri + '''/''' + s.id + '''">
															''' + resource + ''': ''' + name + '''
														</a>
													</div>'''
				html +=	'''						</div>'''
			html += '''						</li>
											<li class="list-group-item">
												<h5>Session Details</h5>
												<div class="row">
													<div class="col-sm-4">
														<b>Authenticated username: </b><br>
														<i>''' + session['username'] + '''
														</i>
													</div>
													<div class="col-sm-4">
														<b>Authenticated user ID: </b><br>
														<i>''' + session['uid'] + '''
														</i>
													</div>
													<div class="col-sm-4">
														<b>Authenticated user group ID: </b><br>
														<i>''' + session['gid'] + '''</i>
													</div>
												</div>
											</li>
										</ul>
									</div>
								</div>
							</div>
						</div>'''
		else:
			html = '''	<div class="jumbotron">
							<div style="position:relative;">
								<div class="card w-100">
									<div class="card-body">
										<ul class="list-group list-group-flush">
											<li class="list-group-item">
												<h1>404 Error</h1>
												<h6>We were unable to locate the requested resource.</h6><br>
												<p>It looks like you were attempting to access a
												"''' + resource + '''" that does not exist. You can try again or feel free to check out the below similar resources that do exist.</p>
												<p>Or return <a href="/home">Home</a>.
											</li>
											<li class="list-group-item">
												<h3>''' + resource + '''s</h3>'''
			if resource == 'Job':
				similar = self.mc.home_jobs_query()
				uri = '/jobs'
			elif resource == 'Education':
				similar = self.mc.home_edu_query()
				uri = '/edus'
			elif resource == 'Organization':
				similar = self.mc.orgs_for_add_query()
				if len(similar) == 0:
					similar = None
				else:
					similar = similar[:4]
				uri = '/orgs'
			elif resource == 'Skill':
				similar = self.mc.skills_for_add_query()
				if len(similar) == 0:
					similar = None
				else:
					similar = similar[:6]
				uri = '/skills'
			else:
				similar = None
			if similar == None:
				html +=	'''						<p><i>We couldn't find any similar resources. Perhaps you need to login as a member to add one?</i><p>
												<p>Or feel free to return to <a href='/home'>Home</a>.'''
			else:
				html += '''						<div class="row">'''
				for s in similar:
					if resource == 'Job':
						name = s.title
					elif resource == 'Education':
						name = s.degree
					elif resource == 'Organization':
						name = s.name
					elif resource == 'Skill':
						name = s.name
					else:
						name = "Unknown resource"
					html += '''						<div class="col-sm-6">
														<a href="''' + uri + '''/''' + s.id + '''">
															''' + resource + ''': ''' + name + '''
														</a>
													</div>'''
				html +=	'''						</div>'''
			html += '''						</li>
											<li class="list-group-item">
												<h5>Session Details</h5>
												<div class="row">
													<div class="col-sm-4">
														<b>Authenticated username: </b><br>
														<i>''' + session['username'] + '''
														</i>
													</div>
													<div class="col-sm-4">
														<b>Authenticated user ID: </b><br>
														<i>''' + session['uid'] + '''
														</i>
													</div>
													<div class="col-sm-4">
														<b>Authenticated user group ID: </b><br>
														<i>''' + session['gid'] + '''</i>
													</div>
												</div>
											</li>
										</ul>
									</div>
								</div>
							</div>
						</div>'''
		return html

	def render_restore (self, session, redirect):
		html = ''
		location = redirect.replace('_', '/')

		if not session['mobile']:
			html += '''	<script type="text/javascript">
							function Redirect() {
								window.location = "''' + location + '''"
							}
							setTimeout('Redirect()', 3000);
						</script>

						<div style="position:relative;width:100%;height:100%;">
							<div style="position:relative;width:100%;height:10%;top:45%;">
								<div class="row">
									<div class="col-sm-12 mx-auto" style="text-align:center;">
										<h2>Processing Operation</h2>
									</div>
									<div class="col-sm-12 mx-auto" style="padding-top:15px;">
										<img src="/static/loading.gif" height="40" width="40" style="position:relative;left:49%;" />
									</div>
									<div class="col-sm-12 mx-auto" style="text-align:center;padding-top:15px;">
										<h6>Restoring site data to original</h6>
									</div>
								</div>
							</div>
						<div>'''

		else:
			html += '''	<script type="text/javascript">
							function Redirect() {
								window.location = "''' + location + '''"
							}
							setTimeout('Redirect()', 3000);
						</script>

						<div style="position:relative;width:100%;height:100%;">
							<div style="position:relative;width:100%;height:10%;top:35%;">
								<div class="row">
									<div class="col-sm-12 mx-auto" style="text-align:center;width:100%;">
										<h2>Processing Operation</h2>
									</div>
									<div class="col-sm-12 mx-auto" style="padding-top:15px;width:100%;">
										<img src="/static/loading.gif" height="40" width="40" style="position:relative;left:45%;" />
									</div>
									<div class="col-sm-12 mx-auto" style="text-align:center;padding-top:15px;">
										<h6>Restoring site data to original</h6>
									</div>
								</div>
							</div>
						<div>'''

		self.dbm.restore_from_backup()
		return html

	def render_go_between (self, method, type, form_data, session):
		html = ''
		if type == 'job' and method == 'add':
			location = '/jobs/' + form_data['job']['id']
			id = form_data['job']['id']
		elif type == 'job' and method == 'update':
			location = '/jobs/' + form_data['id']
			id = form_data['id']
		elif type == 'job' and method == 'delete':
			location = '/home'
			id = form_data['jid']
		elif type == 'edu' and method == 'add':
			location = '/edus/' + form_data['edu']['id']
			id = form_data['edu']['id']
		elif type == 'edu' and method == 'update':
			location = '/edus/' + form_data['id']
			id = form_data['id']
		elif type == 'edu' and method == 'delete':
			location = '/home'
			id = form_data['eid']
		elif type == 'org' and method == 'add':
			location = '/orgs/' + form_data['id']
			id = form_data['id']
		elif type == 'org' and method == 'update':
			location = '/orgs/' + form_data['id']
			id = form_data['id']
		elif type == 'org' and method == 'delete':
			location = '/home'
			id = form_data['oid']
		elif type == 'skill' and method == 'add':
			location = '/skills/' + form_data['id']
			id = form_data['id']
		elif type == 'skill' and method == 'update':
			location = '/skills/' + form_data['id']
			id = form_data['id']
		elif type == 'skill' and method =='delete':
			location = '/skills'
			id = form_data['id']
		elif type == 'contact' and method =='update':
			location = '/home'
			id = form_data['id']
		else:
			location = '/home'

		cb = NoneAccount()
		cb.retrieve(self.dbm, id=session['uid'])

		if not session['mobile']:
			html += '''	<script type="text/javascript">
							function Redirect() {
								window.location = "''' + location + '''"
							}
							setTimeout('Redirect()', 3000);
						</script>

						<div style="position:relative;width:100%;height:100%;">
							<div style="position:relative;width:100%;height:10%;top:45%;">
								<div class="row">
									<div class="col-sm-12 mx-auto" style="text-align:center;">
										<h2>Processing Operation</h2>
									</div>
									<div class="col-sm-12 mx-auto" style="padding-top:15px;">
										<img src="/static/loading.gif" height="40" width="40" style="position:relative;left:49%;" />
									</div>
									<div class="col-sm-12 mx-auto" style="text-align:center;padding-top:15px;">'''
			if method == 'add':
				html += '''				<h6>Adding new \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			elif method == 'update':
				html += '''				<h6>Updating \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			elif method == 'delete':
				html += '''				<h6>Deleting \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			html += '''				</div>
								</div>
							</div>
						<div>'''

		else:
			html += '''	<script type="text/javascript">
							function Redirect() {
								window.location = "''' + location + '''"
							}
							setTimeout('Redirect()', 3000);
						</script>

						<div style="position:relative;width:100%;height:100%;">
							<div style="position:relative;width:100%;height:10%;top:35%;">
								<div class="row">
									<div class="col-sm-12 mx-auto" style="text-align:center;width:100%;">
										<h2>Processing Operation</h2>
									</div>
									<div class="col-sm-12 mx-auto" style="padding-top:15px;width:100%;">
										<img src="/static/loading.gif" height="40" width="40" style="position:relative;left:49%;" />
									</div>
									<div class="col-sm-10 mx-auto" style="text-align:center;padding-top:15px;">'''
			if method == 'add':
				html += '''				<h6>Adding new \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			elif method == 'update':
				html += '''				<h6>Updating \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			elif method == 'delete':
				html += '''				<h6>Deleting \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			html += '''				</div>
								</div>
							</div>
						<div>'''


		if cb.group.name == 'Owners':
			bak = DBM('../dat/db.sqlite.bak.sqlite', False)

		if type == 'job' and method == 'add':
			if 'org' in form_data:
				if 'address' in form_data:
					a = Address(form_data['address']['id'], form_data['address']['name'], form_data['address']['uri'], cb, cb)
					a.create(self.dbm)

					if cb.group.name == 'Owners':
						a.create(bak)
				else:
					a = NoneAddress()
					a.retrieve(self.dbm, id=form_data['org']['address'])

				if form_data['org']['logo'] == None:
					logo = self.dbm.imgtobin('static/placeholder-logo.png')
				else:
					logo = form_data['org']['logo']
				if form_data['org']['image_head'] == None:
					image_head = self.dbm.imgtobin('static/placeholder-header.png')
				else:
					image_head = form_data['org']['image_head']

				o = Org(form_data['org']['id'], form_data['org']['name'], a, form_data['org']['phone'], form_data['org']['desc_short'], form_data['org']['website'], logo, image_head, cb, cb)
				o.create(self.dbm)

				if cb.group.name == 'Owners':
					o.create(bak)

			else:
				o = NoneOrg()
				o.retrieve(self.dbm, id=form_data['job']['org_id'])

			if 'skills' in form_data:
				for s in form_data['skills']:
					if s['icon'] == None:
						icon = self.dbm.imgtobin('static/placeholder-logo.png')
					else:
						icon = s['icon']

					new_s = Skill(s['id'], s['name'], s['exposure'], s['soft_or_hard'], s['reference'], icon, s['category'], s['desc_short'], s['desc_long'], cb, cb)
					new_s.create(self.dbm)

					if cb.group.name == 'Owners':
						new_s.create(bak)

			j = Job(form_data['job']['id'], form_data['job']['title'], form_data['job']['present'], form_data['job']['date_start'], form_data['job']['date_stop'], form_data['job']['desc_short'], form_data['job']['desc_long'], form_data['job']['skill_ids'], o, cb, cb)
			j.create(self.dbm)

			if cb.group.name == 'Owners':
				j.create(bak)

		elif type == 'job' and method == 'update':
			o = NoneOrg()
			o.retrieve(self.dbm, id=form_data['org'])

			j = NoneJob()
			j.retrieve(self.dbm, id=form_data['id'])
			j.title = form_data['title']
			j.present = form_data['present']
			j.date_start = form_data['date_start']
			j.date_stop = form_data['date_stop']
			j.desc_short = form_data['desc_short']
			j.desc_long = form_data['desc_long']
			j.org = o
			j.skill_ids = form_data['skill_ids']
			j.modified_by = cb

			j.update(self.dbm)

			if cb.group.name == 'Owners':
				j.update(bak)

		elif type == 'job' and method == 'delete':
			j = NoneJob()
			if j.retrieve(self.dbm, id=form_data['jid']):
				j.delete(self.dbm)
				if cb.group.name == 'Owners':
					j.delete(bak)
			
			if form_data['del_org'] == True:
				o = NoneOrg();
				if o.retrieve(self.dbm, id=form_data['oid']):
					o.delete(self.dbm)
					if cb.group.name == 'Owners':
						o.delete(bak)
						
			if form_data['del_addr'] == True:
				a = NoneAddress();
				print(a.retrieve(self.dbm, id=form_data['aid']))
				if a.retrieve(self.dbm, id=form_data['aid']):
					a.delete(self.dbm)
					if cb.group.name == 'Owners':
						a.delete(bak)
						
			return html

		elif type == 'edu' and method == 'add':
			if 'org' in form_data:
				if 'address' in form_data:
					a = Address(form_data['address']['id'], form_data['address']['name'], form_data['address']['uri'], cb, cb)
					a.create(self.dbm)

					if cb.group.name == 'Owners':
						a.create(bak)
				else:
					a = NoneAddress()
					a.retrieve(self.dbm, id=form_data['org']['address'])

				if form_data['org']['logo'] == None:
					logo = self.dbm.imgtobin('static/placeholder-logo.png')
				else:
					logo = form_data['org']['logo']
				if form_data['org']['image_head'] == None:
					image_head = self.dbm.imgtobin('static/placeholder-header.png')
				else:
					image_head = form_data['org']['image_head']

				o = Org(form_data['org']['id'], form_data['org']['name'], a, form_data['org']['phone'], form_data['org']['desc_short'], form_data['org']['website'], logo, image_head, cb, cb)
				o.create(self.dbm)

				if cb.group.name == 'Owners':
					o.create(bak)

			else:
				o = NoneOrg()
				o.retrieve(self.dbm, id=form_data['edu']['org'])

			if 'skills' in form_data:
				for s in form_data['skills']:
					if s['icon'] == None:
						icon = self.dbm.imgtobin('static/placeholder-logo.png')
					else:
						icon = s['icon']

					new_s = Skill(s['id'], s['name'], s['exposure'], s['soft_or_hard'], s['reference'], icon, s['category'], s['desc_short'], s['desc_long'], cb, cb)
					new_s.create(self.dbm)

					if cb.group.name == 'Owners':
						new_s.create(bak)

			e = Education(form_data['edu']['id'], o, form_data['edu']['degree'], form_data['edu']['gpa'], form_data['edu']['skill_ids'], form_data['edu']['date_stop'], form_data['edu']['desc_short'], form_data['edu']['desc_long'], cb, cb)
			e.create(self.dbm)

			if cb.group.name == 'Owners':
				e.create(bak)

		elif type == 'edu' and method == 'update':
			o = NoneOrg()
			o.retrieve(self.dbm, id=form_data['org'])

			e = NoneEducation()
			e.retrieve(self.dbm, id=form_data['id'])
			e.degree = form_data['degree']
			e.gpa = form_data['gpa']
			e.date_stop = form_data['date_stop']
			e.desc_short = form_data['desc_short']
			e.desc_long = form_data['desc_long']
			e.org = o
			e.skill_ids = form_data['skill_ids']
			e.modified_by = cb

			e.update(self.dbm)

			if cb.group.name == 'Owners':
				e.update(bak)
				
		elif type == 'edu' and method == 'delete':	
		
			e = NoneEducation()
			if e.retrieve(self.dbm, id=form_data['eid']):
				e.delete(self.dbm)
				if cb.group.name == 'Owners':
					e.delete(bak)
					
			if form_data['del_org'] == True:
				o = NoneOrg();
				if o.retrieve(self.dbm, id=form_data['oid']):
					o.delete(self.dbm)
					if cb.group.name == 'Owners':
						o.delete(bak)
						
			if form_data['del_addr'] == True:
				a = NoneAddress();
				print(a.retrieve(self.dbm, id=form_data['aid']))
				if a.retrieve(self.dbm, id=form_data['aid']):
					a.delete(self.dbm)
					if cb.group.name == 'Owners':
						a.delete(bak)
		
		elif type == 'contact' and method == 'update':
			if form_data['new_address']:
				aid = self.dbm.genid()
				param = [("q", form_data['address'])]
				uri = "https://www.google.com/search?" + urlencode(param)
				a = Address(aid, form_data['address'], uri, cb, cb)
				a.create(self.dbm)
				if cb.group.name == 'Owners':
					a.create(bak)
					
			else:
				a = NoneAddress()
				a.retrieve(self.dbm, id=form_data['address'])
			
			c = NoneContact()
			c.retrieve(self.dbm, id=form_data['id'])
			c.name = form_data['name']
			c.phone1 = form_data['phone1']
			c.phone2 = form_data['phone2']
			c.email = form_data['email']
			c.objective = form_data['objective']
			c.address = a
			c.modified_by = cb
			c.update(self.dbm)
			
			if cb.group.name == 'Owners':
				c.update(bak)
			
		elif type == 'org' and method == 'add':
			if form_data['new_addr']:
				param = [("q", form_data['aname'])]
				uri = "https://www.google.com/search?" + urlencode(param)
				a = Address(form_data['aid'], form_data['aname'], uri, cb, cb)
				a.create(self.dbm)
				
				if cb.group.name == 'Owners':
					a.create(bak)
					
			else:
				a = NoneAddress()
				a.retrieve(self.dbm, id=form_data['aid'])
			
			o = Org(form_data['id'], form_data['name'], a, form_data['phone'], form_data['desc_short'], form_data['website'], form_data['logo'], form_data['image_head'], cb, cb)
			o.create(self.dbm)
			
			if cb.group.name == 'Owners':
				o.create(bak)
				
			return html
			
		elif type == 'org' and method == 'update':
			if form_data['new_address']:
				param = [("q", form_data['aname'])]
				uri = "https://www.google.com/search?" + urlencode(param)
				a = Address(form_data['aid'], form_data['aname'], uri, cb, cb)
				a.create(self.dbm)
				
				if cb.group.name == 'Owners':
					a.create(bak)
			else:
				a = NoneAddress()
				a.retrieve(self.dbm, id=form_data['aid'])
				
			o = NoneOrg()
			o.retrieve(self.dbm, id=form_data['id'])
			o.name = form_data['name']
			o.phone = form_data['phone']
			o.desc_short = form_data['desc_short']
			o.website = form_data['website']
			if form_data['new_logo']:
				o.logo = form_data['logo']
			if form_data['new_image_head']:
				o.image_head = form_data['image_head']
			o.address = a
			o.modified_by = cb
			
			o.update(self.dbm)
			
			if cb.group.name == 'Owners':
				o.update(bak)

		elif type == 'org' and method == 'delete':
			print(str(form_data))
						
			if form_data['num_jobs'] > 0:
				for i in range(form_data['num_jobs']):
					jadj = NoneJob()
					oadj = NoneOrg()
					print(form_data['job_adj'][i][0])
					jadj.retrieve(self.dbm, id=form_data['job_adj'][i][0])
					oadj.retrieve(self.dbm, id=form_data['job_adj'][i][1])
					jadj.org = oadj
					jadj.update(self.dbm)
					
					if cb.group.name == 'Owners':
						jadj.update(bak)
						
			if form_data['num_edus'] > 0:
				for i in range(form_data['num_edus']):
					eadj = NoneEducation()
					oadj = NoneOrg()
					eadj.retrieve(self.dbm, id=form_data['edu_adj'][i][0])
					oadj.retrieve(self.dbm, id=form_data['edu_adj'][i][1])
					eadj.org = oadj
					eadj.update(self.dbm)
					
					if cb.group.name == 'Owners':
						eadj.update(bak)
						
			o = NoneOrg()
			if (o.retrieve(self.dbm, id=form_data['oid'])):
				o.delete(self.dbm)
				if cb.group.name == 'Owners':
					o.delete(bak)
			
			if form_data['del_addr']:
				a = NoneAddress()
				if a.retrieve(self.dbm, id=form_data['aid']):
					a.delete(self.dbm)
					if cb.group.name == 'Owners':
						a.delete(bak)

		elif type == 'skill' and method == 'add':
			s = Skill(form_data['id'], form_data['name'], form_data['exposure'], form_data['soft_or_hard'], form_data['reference'], form_data['icon'], form_data['category'], form_data['desc_short'], form_data['desc_long'], cb, cb)
			s.create(self.dbm)
			
			if cb.group.name == 'Owners':
				s.create(bak)
				
		elif type == 'skill' and method == 'update':
			s = NoneSkill()
			if s.retrieve(self.dbm, id=form_data['id']):
				s.name = form_data['name']
				s.exposure = form_data['exposure']
				s.soft_or_hard = form_data['soft_or_hard']
				s.reference = form_data['reference']
				if form_data['update_icon']:
					s.icon = form_data['icon']
				s.category = form_data['category']
				s.desc_short = form_data['desc_short']
				s.desc_long = form_data['desc_long']
				s.modified_by = cb
				
				s.update(self.dbm)
				
				if cb.group.name == 'Owners':
					s.update(bak)
					
		elif type == 'skill' and method == 'delete':
			if form_data['del_jobs']:
				for jid in form_data['jobs']:
					j = NoneJob()
					if j.retrieve(self.dbm, id=jid):
						sids = j.skill_ids
						split = sids.split(',')
						split.remove(form_data['id'])
						final_str = ""
						for i in range(len(split)):
							if i != len(split) - 1:
								final_str += split[i] + ','
							else:
								final_str += split[i]
						j.skill_ids = final_str
						j.modified_by = cb
						j.update(self.dbm)
						
						if cb.group.name == 'Owners':
							j.update(self.bak)
			
			if form_data['del_edus']:
				for eid in form_data['edus']:
					e = NoneEducation()
					if e.retrieve(self.dbm, id=eid):
						sids = e.skill_ids
						split = sids.split(',')
						split.remove(form_data['id'])
						final_str = ""
						for i in range(len(split)):
							if i != len(split) - 1:
								final_str += split[i] + ','
							else:
								final_str += split[i]
						e.skill_ids = final_str
						e.modified_by = cb
						e.update(self.dbm)
						
						if cb.group.name == 'Owners':
							e.update(self.bak)
			
			s = NoneSkill()
			if s.retrieve(self.dbm, id=form_data['id']):
				s.delete(self.dbm)
				
				if cb.group.name == 'Owners':
					s.delete(bak)

		return html
