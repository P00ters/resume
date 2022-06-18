import base64
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
from educations import retrieve_educations
from jobs import retrieve_jobs
import orgs
from orgs import Org, retrieve_orgs
from fmat import addresslines, telelink, teleformat, sanitize

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"

class OrgRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm

	def render_org_tile (self, mobile, auth, **kwargs):
		this_org = kwargs.get('this_org', None)
		next_org = kwargs.get('next_org', None)
		last_org = kwargs.get('last_org', None)
		this_job = kwargs.get('this_job', None)
		next_job = kwargs.get('next_job', None)
		last_job = kwargs.get('last_job', None)
		this_edu = kwargs.get('this_edu', None)
		next_edu = kwargs.get('next_edu', None)
		last_edu = kwargs.get('last_edu', None)

		if this_org != None:
			logo = "data:image/png;base64," +  this_org.logo.decode('utf-8')
			head = "data:image/png;base64," + this_org.image_head.decode('utf-8')
		elif this_job != None:
			logo = "data:image/png;base64," + this_job.org.logo.decode('utf-8')
			head = "data:image/png;base64," + this_job.org.image_head.decode('utf-8')
		elif this_edu != None:
			logo = "data:image/png;base64," + this_edu.org.logo.decode('utf-8')
			head = "data:image/png;base64," + this_edu.org.image_head.decode('utf-8')
		else:
			# return 404
			return
			
		if auth:
			if this_job != None and next_job != None and last_job != None:
				j = this_job
				a_edit = "'" + sanitize(j.id) + "', '" + sanitize(j.org.id) + "', '" + sanitize(j.org.name) + "', '" + sanitize(j.title) + "', " + str(j.present) + ", '" + str(j.date_start) + "', '" + str(j.date_stop) + "', '" + sanitize(j.desc_short) + "', '" + sanitize(j.desc_long) + "', " + str(len(j.skills(self.dbm)))
				
				
					
				oid = j.org.id
				odangle_count = 0
				edangles = retrieve_educations(self.dbm, org=oid)
				odangle_count += len(edangles)
				jdangles = retrieve_jobs(self.dbm, org=oid)
				odangle_count += len(jdangles)
				if (odangle_count <= 1):
					b_odangles = 1
				else:
					b_odangles = 0
					b_adangles = 0
					
				if (b_odangles):
					aid = j.org.address.id
					adangle_count = 0
					odangles = retrieve_orgs(self.dbm, address=aid)
					adangle_count += len(odangles)
					if adangle_count <= 1:
						b_adangles = 1
					else:
						b_adangles = 0
						
				a_del = "'" + sanitize(j.id) + "', '" + sanitize(j.title) + "', " + str(b_odangles) + ", '" + sanitize(j.org.id) + "', '" + sanitize(j.org.name) + "', " + str(b_adangles) + ", '" + sanitize(j.org.address.id) + "', '" + sanitize(j.org.address.name) + "'"
			
			if this_edu != None and next_edu != None and last_edu != None:
				e = this_edu
				a_edit = "'" + sanitize(e.id) + "', '" + sanitize(e.org.id) + "', '" + sanitize(e.org.name) + "', '" + sanitize(e.degree) + "', " + str(e.gpa) + ", '" + e.date_stop + "', '" + sanitize(e.desc_short) + "', '" + sanitize(e.desc_long) + "', " + str(len(e.skills(self.dbm)))
					
				oid = e.org.id
				odangle_count = 0
				edangles = retrieve_educations(self.dbm, org=oid)
				odangle_count += len(edangles)
				jdangles = retrieve_jobs(self.dbm, org=oid)
				odangle_count += len(jdangles)
				if (odangle_count <= 1):
					b_odangles = 1
				else:
					b_odangles = 0
					b_adangles = 0
					
				if (b_odangles):
					aid = e.org.address.id
					adangle_count = 0
					odangles = retrieve_orgs(self.dbm, address=aid)
					adangle_count += len(odangles)
					if adangle_count <= 1:
						b_adangles = 1
					else:
						b_adangles = 0
						
				a_del = "'" + sanitize(e.id) + "', '" + sanitize(e.degree) + "', " + str(b_odangles) + ", '" + sanitize(e.org.id) + "', '" + sanitize(e.org.name) + "', " + str(b_adangles) + ", '" + sanitize(e.org.address.id) + "', '" + sanitize(e.org.address.name) + "'"

		html = ''
		if not mobile:
			html = '''	<div class="jumbotron">'''
	
			html += '''		<img src="'''+head+'''" style="position:relative;width:70%;left:15%;z-index:0;max-height:25%;"/>'''
			if this_org != None and next_org != None and last_org != None:
				html += '''	<a href="/orgs/''' + str(next_org.id) + '''">
								<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;" />
							</a>
							<a href="/orgs/''' + str(last_org.id) + '''">
								<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
							</a>'''
			elif this_job != None and next_job != None and last_job != None:
				this_org = this_job.org
				html += '''	<a href="/jobs/''' + str(next_job.id) + '''">
								<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
							</a>
							<a href="/jobs/''' + str(last_job.id) + '''">
								<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
							</a>'''
			elif this_edu != None and next_edu != None and last_edu != None:
				this_org = this_edu.org
				html += '''	<a href="/edus/''' + str(next_edu.id) + '''">
								<img src="/static/r-arr.png" width="75" height="75" style="position:relative;left:17.5%;"/>
							</a>
							<a href="/edus/''' + str(last_edu.id) + '''">
								<img src="/static/l-arr.png" width="75" height="75" style="position:relative;left:-67.5%;"/>
							</a>'''
			else:
				# return 404
				return
			html += '''		<br>
							<div style="position:relative;width:100%;z-index:1;">
								<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0">
									<div class="card-header">
										<div class="row">
											<div class="col-9">
												<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index:2">
													<img src="''' +  logo + '''" width="45" height="45" />
												</div>
												<a href="/orgs/''' + str(this_org.id) + '''" style="color:black;">
													<h4 style="display:inline;padding-left:10px;vertical-align:middle;">
														''' + str(this_org.name) + '''
													</h4>
												</a>
											</div>
											<div class="col-3">'''
			if auth:
				if this_job != None and next_job != None and last_job != None:
					if len(j.skills(self.dbm)) > 0:
						eskills = j.skills(self.dbm)
						html += '''			<form id="'''+j.id+'''" style="display:none;">'''
						for i in range(len(eskills)):
							html +=			'''<input type="hidden" id="job_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
						html += '''			</form>'''
					html += '''				
											<a href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal"><button type="button" style="position:relative;width:50px;display:inline;left:10px;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>
											<a href="javascript:void(0)" data-toggle="modal" data-target="#editJobModal">
												<button style="position:relative;width:50px;display:inline;left:30px;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_job('''+a_edit+''')"><img src='/static/edit.png' width="30"/></button>
											</a>
											<a href="javascript:void(0)" data-toggle="modal" data-target="#delJobModal">
												<button style="position:relative;width:50px;display:inline;left:50px;" type="button" class="btn btn-outline-danger btn-lg btn-block" onClick="del_job('''+a_del+''')"><img src='/static/delete.png' width="30"/></button>
											</a>'''
				if this_edu != None and next_edu != None and last_edu != None:
					if len(e.skills(self.dbm)) > 0:
						eskills = e.skills(self.dbm)
						html += '''			<form id="'''+e.id+'''" style="display:none;">'''
						for i in range(len(eskills)):
							html +=			'''<input type="hidden" id="edu_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
						html += '''			</form>'''
					html += '''
											<a href="javascript:void(0)" data-toggle="modal" data-target="#addEduModal"><button type="button" style="position:relative;width:50px;display:inline;left:10px;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>
											<a href="javascript:void(0)" data-toggle="modal" data-target="#editEduModal">
												<button style="position:relative;width:50px;display:inline;left:30px;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_edu('''+a_edit+''')"><img src='/static/edit.png' width="30"/></button>
											</a>
											<a href="javascript:void(0)" data-toggle="modal" data-target="#delEduModal">
												<button style="position:relative;width:50px;display:inline;left:50px;" type="button" class="btn btn-outline-danger btn-lg btn-block" onClick="del_edu('''+a_del+''')"><img src='/static/delete.png' width="30"/></button>
											</a>'''
												
			html += '''						</div>
										</div>
									</div>'''


			if this_job == None and this_edu == None:
				html +=	'''			<div class="card-body" style="z-index:0;">
										<div class="row">
											<div class="col-sm-6">
												<h6>Description:</h6>
												''' + str(this_org.desc_short) + '''
											</div>
											<div class="col-sm-2">
												<h6>Information:</h6>
												''' + addresslines(str(this_org.address.name)) + '''
												<a href="''' + telelink(this_org.phone) + '''">
												''' + teleformat(this_org.phone) + '''
												</a>
												<br>
												<a href="''' + str(this_org.website) + '''" target="_blank">
													Website
												</a>
											</div>
											<div class="col-sm-4">
												<iframe width="350" height="200" frameborder="0" style="0"
													referrerpolicy="no-referrer-when-downgrade"
													src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''&q=''' + str(this_org.address.name) + '''" allowfullscreen>
												</iframe>
											</div>
										</div>
									</div>
								</div>'''
			else:
				html += '''		</div>'''

		else:
			if this_org != None and next_org != None and last_org != None:
				this_org = this_org
			elif this_job != None and next_job != None and last_job != None:
				this_org = this_job.org
			elif this_edu != None and next_edu != None and last_edu != None:
				this_org = this_edu.org
			else:
				# return 404
				return

			html = '''	<div class="jumbotron">
							<img src="'''+head+'''" style="position:relative;width:100%;left:0%;z-index:0;"/>
							<div style="position:relative;width:100%;z-index=1;">
							<div class="card">
								<div class="card-header">
									<div class="row">
										<div class="col-1">
											<div style="width:35px;height:35px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
												<img src="'''+logo+'''" width="35" height="35"/>
											</div>
										</div>
										<div class="col-8" style="position:relative;display:inline;left:15px;top:5px;">
											<a href="/orgs/''' + str(this_org.id) + '''" style="color:black;"><u>
												<h5 style="vertical-align:middle;">
													''' + str(this_org.name) + '''</u></h4>
											</a>
										</div>
										<div class="col-3">'''
			
			if auth:
				if this_job != None and next_job != None and last_job != None:
					if len(j.skills(self.dbm)) > 0:
						eskills = j.skills(self.dbm)
						html += '''			<form id="'''+j.id+'''" style="display:none;">'''
						for i in range(len(eskills)):
							html +=			'''<input type="hidden" id="job_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
						html += '''			</form>'''
					html += '''				<ul class="navbar-nav mr-auto" style="width:100%; 
												<li class="nav-item dropdown" style="width:100%;">
													<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;vertical-align:middle;">Change</a>
													<div class="dropdown-menu", aria-labelledby="dropdown04">
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addJobModal">New</a>
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" onClick="edit_job('''+a_edit+''')"  data-target="#editJobModal">Edit</a>
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#delJobModal" onClick="del_job('''+a_del+''')">Delete</a>
													</div>
												</li>
											</ul>
											'''
				if this_edu != None and next_edu != None and last_edu != None:
					if len(e.skills(self.dbm)) > 0:
						eskills = e.skills(self.dbm)
						html += '''			<form id="'''+e.id+'''" style="display:none;">'''
						for i in range(len(eskills)):
							html +=			'''<input type="hidden" id="edu_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
						html += '''			</form>'''
					html += '''				<ul class="navbar-nav mr-auto" style="width:100%; 
												<li class="nav-item dropdown" style="width:100%;">
													<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown10" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;vertical-align:middle;">Change</a>
													<div class="dropdown-menu", aria-labelledby="dropdown10">
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addEduModal">New</a>
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" onClick="edit_edu('''+a_edit+''')"  data-target="#editEduModal">Edit</a>
														<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#delEduModal" onClick="del_edu('''+a_del+''')">Delete</a>
													</div>
												</li>
											</ul>'''
											
			html += '''					</div>
									</div>
								</div>
							</div>'''
			if this_job == None and this_edu == None:
				html += '''	<div class="card">
								<div class="card-body" style="z-index:0;">
									<div class="row">
										<div class="col-sm-12">
											<div style="position:relative;width:50%;left:0%;display:inline;">
												<a href="/orgs/''' + str(last_org.id) + '''">< Last Org</a>
											</div>
											<div style="position:relative;width:50%;left:50%;display:inline;text-align:right;">
												<a href="/orgs/''' + str(next_org.id) + '''">Next Org ></a>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="card">
								<div class="card-body" style="z-index:0;">
									<div class="row">
										<div class="col-sm-8">
											<h6>Description:</h6>
											''' + str(this_org.desc_short) + '''<br><br>
										</div>
										<div class="col-sm-4">
												<h6>Information:</h6>
												''' + addresslines(str(this_org.address.name))+'''
												<a href="''' + telelink(str(this_org.phone)) + '''">
													''' + teleformat(str(this_org.phone)) + '''
												</a>
												<br>
												<a href="''' + str(this_org.website) + '''" target="_blank">Website</a>
										</div>
										<div class="col-sm-4">
											<iframe
												width="350"
												height="200"
												frameborder="0" style="border:0"
												referrerpolicy="no-referrer-when-downgrade"
												src="https://www.google.com/maps/embed/v1/place?key='''+g_api+'''+&q=''' + str(this_org.name) +'''"
												allowfullscreen>
											</iframe>
										</div>
									</div>
									<div style="position:relative;left:71%;width:25%;font-size:8px;text-align:right;padding-top:10px;">
										<a href="/orgs/''' + str(this_org.id) + '''">''' + str(this_org.id) + '''</a>
									</div>
								</div>
							</div>'''
			else:
				html += '''	</div>'''

		return html


	def addresslines (self, address):
		a = address.split(',')
		c = ""
		for b in a:
			c += b + '<br>'
		return c
