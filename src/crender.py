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

from flask import Flask, session, render_template, request, redirect

sys.path.append("models")
sys.path.append("views")
sys.path.append("controllers")

from mastercontroller import MasterController
from dbm import DBM
from accounts import NoneAccount
from addresses import retrieve_all_addresses, Address, NoneAddress
from contactsrender import ContactRenderer
from jobsrender import JobRenderer
from jobs import Job, retrieve_all_jobs, jobs_date_sort, NoneJob
from orgsrender import OrgRenderer
from orgs import Org, retrieve_all_orgs, NoneOrg
from educations import Education, retrieve_all_educations, edus_date_sort, NoneEducation
from edusrender import EduRenderer
from skillsrender import SkillRenderer
from skills import retrieve_skills_custom, NoneSkill, Skill, retrieve_skills, retrieve_all_skills

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"


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
		html += self.contactrenderer.render_home_contact(contact, session['mobile'])

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
									</div>'''
			html += '''			</div>
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
		html = self.orgrenderer.render_org_tile(mobile, this_job=jobs[0], next_job=jobs[1], last_job=jobs[2])
		html += self.jobrenderer.render_job_page(jobs[0], jobs[1], jobs[2], mobile)

		return html

	def edus_edus_htmlify (self, edus, mobile):
		html = self.orgrenderer.render_org_tile(mobile, this_edu=edus[0], next_edu=edus[1], last_edu=edus[2])
		html += self.edurenderer.render_edu_page(edus[0], edus[1], edus[2], mobile)

		return html

	def org_htmlify (self, orgs, mobile):
		return self.orgrenderer.render_org_tile(mobile, this_org=orgs[0], next_org=orgs[1], last_org=orgs[2])

	def skills_general_htmlify (self, all_skills, mobile):
		return self.skillrenderer.render_skills_general(all_skills, mobile)

	def skills_skills_htmlify (self, skill, mobile):
		html = self.skillrenderer.render_skills_page(skill[0], skill[1], skill[2], mobile)
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
			html += '''									<select "style=width:100%;" size="6" id="org_selector" name="org_selector">'''
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
												<p>Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<p>Extend the application into a full RESTful API to GET any resume data via JSON.</p>
												<div style="padding-left:10px;position:relative;top:3px;">
													<span class="badge badge-pill badge-warning">Up Next</span>
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
													<span class="badge badge-pill badge-info">In Progress</span>
												</div>
												<div class="col-sm-8">
													<p>Implement CRUD operations within the view portion of the application using existing authentication and access control structures.</p>
												</div>
											</div>
											<div class="row" style="padding-left:15px;">
												<div class="col-sm-2">
													<span class="badge badge-pill badge-warning">Up Next</span>
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
		elif type == 'edu' and method == 'add':
			location = '/edus/' + form_data['edu']['id']
			id = form_data['edu']['id']
		elif type == 'edu' and method == 'update':
			location = '/edus/' + form_data['id']
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
									<div class="col-sm-12 mx-auto" style="text-align:center;padding-top:15px;">'''
			if method == 'add':
				html += '''				<h6>Adding new \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			elif method == 'update':
				html += '''				<h6>Updating \'''' + type + '''\' with <i>id</i> of <b>''' + id + '''</b></h6>'''
			html += '''				</div>
								</div>
							</div>
						<div>'''


		if cb.group.name == 'Owners':
			bak = DBM('../dat/db.sqlite.bak.sqlite')
			
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

		return html
