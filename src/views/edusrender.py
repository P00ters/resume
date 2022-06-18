import base64
import datetime
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import educations
from educations import Education, retrieve_educations
from jobs import Job, retrieve_jobs
from orgs import Org, retrieve_orgs
import skills
from skills import Skill
from fmat import datereformat, sanitize

class EduRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm
		
	def render_home_tile (self, e, mobile, auth):
		# Set logo source
		src = "data:image/png;base64," + e.org.logo.decode('utf-8')
		date_stop = datetime.datetime.strptime(e.date_stop, '%Y-%m-%d')
		date_stop_str = date_stop.strftime('%b %Y')
		html = ''
		
		if not mobile:
			html += '''	<div class="card w-75">
							<div class="card-header">
								<div class="row">
									<div class="col-1 d-flex align-items-center">
										<img width="30" height="30" src="''' + src + '''" />
									</div>
									<div class="col-7 d-flex align-items-center">
										<a href="/orgs/''' + str(e.org.id) + '''" style="color:black;">
											<h6 style="margin-top:5px;">''' + str(e.org.name) + '''</h6>
										</a>
									</div>'''
			if auth:

				a_edit = "'" + sanitize(e.id) + "', '" + sanitize(e.org.id) + "', '" + sanitize(e.org.name) + "', '" + sanitize(e.degree) + "', " + str(e.gpa) + ", '" + e.date_stop + "', '" + sanitize(e.desc_short) + "', '" + sanitize(e.desc_long) + "', " + str(len(e.skills(self.dbm)))
				
				if len(e.skills(self.dbm)) > 0:
					eskills = e.skills(self.dbm)
					html += '''			<form id="'''+e.id+'''">'''
					for i in range(len(eskills)):
						html +=			'''<input type="hidden" id="edu_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
					html += '''			</form>'''
					
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
						
				html += '''			<div style="margin-right:25; margin-left:auto;">
										<a href="javascript:void(0)" data-toggle="modal" data-target="#delEduModal">
											<button style="position:relative;width:50px;margin-left:auto;margin-right:10;display:inline;" type="button" class="btn btn-outline-danger btn-lg btn-block" onClick="del_edu('''+a_del+''')"><img src='/static/delete.png' width="30"/></button>
										</a>
										<a href="javascript: void(0)" data-toggle="modal" data-target="#editEduModal">
											<button style="position:relative;width:50px;margin-left:auto;margin-right:0;display:inline;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_edu('''+a_edit+''')"><img src='/static/edit.png' width="30"/></button>
										</a>
									</div>'''
			html += '''			</div>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<div class="row">
											<div class="col-7">
												<a href="/edus/''' + str(e.id) + '''" style="color:black;">
												<h5 class="card-title">''' + str(e.degree) + '''</h5></a>
											</div>
											<div class="col-5" style="text-align:right;">
												<i style="margin-top:5px;">''' + date_stop_str + '''</i>
											</div>
										</div>
										<p class="card-text">''' + str(e.desc_short) + '''</p>
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
											<a href="/edus/''' + str(e.id) + '''">''' + str(e.id) + '''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(e.skills(self.dbm)) > 0:
				for s in e.skills(self.dbm):
					html += '''				<a href="/skills/''' + s.id + '''" style=padding-left:10px;">
												<span class="badge badge-pill badge-dark">
													''' + s.name + '''
												</span>
											</a>'''
			else:
				html += '''					<i style="padding-left:15px;">No associated skills identified for this experience.</i>'''
			html += '''					</div>
									</li>
								</ul>
							</div>
						</div>
						<br>'''
		
		else:
			html += '''	<div class="card w-100">
							<div class="card-header">
								<div class="row">
									<div class="col-1">
										<img width="30" height="30" src="''' + src + '''" />
									</div>
									<div class="col-8">
										<a href="/orgs/'''+str(e.org.id)+'''" style="color:black;">
										<h6 style="margin-top:5px;"><u>''' + str(e.org.name) + '''</u></h6>
										</a>
									</div>
									
								'''
			if auth:
				html += '''			<div class="col-3" style="position:relative;top:-5px;display:inline;margin-right:0px;">'''
				
				a_edit = "'" + sanitize(e.id) + "', '" + sanitize(e.org.id) + "', '" + sanitize(e.org.name) + "', '" + sanitize(e.degree) + "', " + str(e.gpa) + ", '" + e.date_stop + "', '" + sanitize(e.desc_short) + "', '" + sanitize(e.desc_long) + "', " + str(len(e.skills(self.dbm)))
				
				if len(e.skills(self.dbm)) > 0:
					eskills = e.skills(self.dbm)
					html += '''			<form id="'''+e.id+'''" style="display:none;">'''
					for i in range(len(eskills)):
						html +=			'''<input type="hidden" id="edu_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
					html += '''			</form>'''
					
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
						
				html += '''			<ul class="navbar-nav mr-auto" style="width:100%; display:inline;">
										<li class="nav-item dropdown" style="width:100%;">
											<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">Change</a>
											<div class="dropdown-menu", aria-labelledby="dropdown04">
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" onClick="edit_edu('''+a_edit+''')"  data-target="#editEduModal">Edit</a>
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#delEduModal" onClick="del_edu('''+a_del+''')">Delete</a>
											</div>
										</li>
									</ul>
									</div>'''
			html += '''			</div>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<div class="row">
											<div class="col-8 d-flex align-items-center">
												<a href="/edus/'''+str(e.id)+'''" style="color:black;">
												<h5 class="card-title"><u>''' + str(e.degree) + '''</u></h5></a>
											</div>
											<div class="col-4" style="text-align:right;">
												<i style="margin-top:5px;">''' + date_stop_str + '''</i>
											</div>
										</div>
										<p class="card-text">''' + str(e.desc_short) + '''</p>
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
											<a href="/edus/''' + str(e.id) + '''">''' + str(e.id) + '''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(e.skills(self.dbm)) > 0:
				for s in e.skills(self.dbm):
					html += '''				<a href="/skills/''' + s.id + '''" style=padding-left:10px;">
												<span class="badge badge-pill badge-dark">
													''' + s.name + '''
												</span>
											</a>'''
			else:
				html += '''					<i>No associated skills identified for this experience.</i>'''
			html += '''					</div>
									</li>
								</ul>
							</div>
						</div>'''
						
		return html
	
	def render_edu_page (self, this_edu, next_edu, last_edu, mobile):
		html = ''
	
		if not mobile:
			html += '''	<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
							<div class="card-header">
								<div class="row">
									<div class="col-sm-7">
										<h4 style="vertical-align:middle;">''' + str(this_edu.degree) + '''</h4>
									</div>
									<div class="col-sm-5" style="text-align:right;">
										<i style="vertical-align:middle;">
											''' + datereformat(str(this_edu.date_stop)) + '''
										</i>
									</div>
								</div>
							</div>
							<div class="card-body" style="z-index:0;">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<h6>Abstract</h6>
										''' + str(this_edu.desc_short) + '''
										<br><br>
										<h6>Description</h6>
										''' + str(this_edu.desc_long) + '''
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
											<a href="/edus/''' + str(this_edu.id) + '''">
												''' + str(this_edu.id) + '''
											</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(this_edu.skills(self.dbm)) > 0:
				for s in this_edu.skills(self.dbm):
					html +=	'''				<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
												<span class="badge badge-pill badge-dark">
													''' + str(s.name) + '''
												</span>
											</a>'''
			else:
				html += '''					<i style="padding-left:15px;">No associated skills identified for this experience.</i>'''
			html +=	'''					</div>
									</li>
								</ul>
							<div>
						</div>'''
						
		else:
			html += '''	<div class="card">
							<div class="card-body">
								<div class="row">
									<div class="col-sm-12">
										<div style="position:relative;width:50%;left:0%;display:inline;">
											<a href="/edus/''' + str(last_edu.id) + '''" style="text-align:left;">
												< Last Edu
											</a>
										</div>
										<div style="position:relative;width:50%;left:50%;display:inline;">
											<a href="/edus/''' + str(next_edu.id) + '''" style="text-align:right;position:relative;width:50%;">
												Next Edu >
											</a>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card">
							<div class="card-header">
								<div class="row">
									<div class="col-sm-7">
										<h4 style="vertical-align:middle;">''' + str(this_edu.degree) + '''</h4>
									</div>
									<div class="col-sm-5" style="text-align:right;">
										<i style="vertical-align:middle;">
											''' + datereformat(str(this_edu.date_stop)) + '''
										</i>
									</div>
								</div>
							</div>
							<div class="card-body" style="z-index:0;">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<h6>Abstract</h6>
										''' + str(this_edu.desc_short) + '''
										<br><br>
										<h6>Description</h6>
										''' + str(this_edu.desc_long) + '''
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
											<a href="/edus/''' + str(this_edu.id) + '''">
												''' + str(this_edu.id) + '''
											</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(this_edu.skills(self.dbm)) > 0:
				for s in this_edu.skills(self.dbm):
					html +=	'''				<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
												<span class="badge badge-pill badge-dark">
													''' + str(s.name) + '''
												</span>
											</a>'''
			else:
				html += '''					<i>No associated skills identified for this experience.</i>'''
			html +=	'''					</div>
									</li>
								</ul>
							</div>
						</div>'''
	
			
		return html