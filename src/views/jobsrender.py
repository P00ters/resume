import base64
import datetime
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import jobs
from jobs import Job
import skills
from skills import Skill
from fmat import datereformat

class JobRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm

	def render_home_tile (self, j, mobile, auth):
		# Set logo source
		if j.org.logo != None and j.org.logo != '':
			org_logo_src = "data:image/png;base64," + j.org.logo.decode('utf-8')
		else:
			org_logo_src = "/static/placeholder-logo.png"

		# Format date strings
		date_start = datetime.datetime.strptime(j.date_start, '%Y-%m-%d')
		if j.present == 1:
			date_stop = 'Present'
		else:
			date_stop = datetime.datetime.strptime(j.date_stop, '%Y-%m-%d')
		date_start_str = date_start.strftime('%b %Y')
		if j.present != 1:
			date_stop_str = date_stop.strftime('%b %Y')
		else:
			date_stop_str = 'Present'

		html = ""
		# Render desktop view
		if not mobile:
			html += '''
				<!-- Job home tile card -->

				<div class="card w-75">
					<div class="card-header">
						<div class="row">
							<div class="col-1 d-flex align-items-center">
								<img width="30" height="30" src="''' + org_logo_src + '''" />
							</div>
							<div class="col-6 d-flex align-items-center">
								<a href="/orgs/''' + str(j.org.id) + '''" style="color:black;">
									<h6 style="margin-top:5px;">''' + str(j.org.name) + '''</h6>
								</a>
							</div>'''
			if auth:
				short_desc = j.desc_short.replace("'", "\\'")
				long_desc = j.desc_long.replace("'", "\\'")
				a_edit = "'" + j.id + "', '" + j.org.id + "', '" + j.org.name + "', '" + j.title + "', " + str(j.present) + ", '" + str(j.date_start) + "', '" + str(j.date_stop) + "', '" + short_desc + "', '" + long_desc + "', " + str(len(j.skills(self.dbm)))
				
				if len(j.skills(self.dbm)) > 0:
					eskills = j.skills(self.dbm)
					html += '''			<form id="'''+j.id+'''" style="display:none;">'''
					for i in range(len(eskills)):
						html +=			'''<input type="hidden" id="job_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
					html += '''			</form>'''
				html += '''	<div style="margin-right:25; margin-left:auto;">
								<a href="javascript:void(0)" data-toggle="modal" data-target="#deleteModal" style="margin-right:0; margin-left:auto;">
									<button style="position:relative;width:50px;margin-left:auto;margin-right:10;display:inline;" type="button" class="btn btn-outline-danger btn-lg btn-block"><img src='/static/delete.png' width="30"/></button>
								</a>
								<a href="javascript:void(0)" data-toggle="modal" data-target="#editJobModal" style="margin-right:0; margin-left:auto;">
										<button style="position:relative;width:50px;margin-left:auto;margin-right:0;display:inline;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_job('''+a_edit+''')"><img src='/static/edit.png' width="30"/></button>
								</a>
							</div>'''
			html += '''	</div>
					</div>
					<div class="card-body">
						<ul class="list-group list-group-flush">
							<li class="list-group-item">
								<div class="row">
									<div class="col-7">
										<a href="/jobs/''' + str(j.id) + '''" style="color:black;">
											<h5 class="card-title">''' + str(j.title) + '''</h5>
										</a>
									</div>
									<div class="col-5" style="text-align:right;">
										<i style="margin-top:5px;">
											''' + date_start_str + ' - ' + date_stop_str + '''
										</i>
									</div>
								</div>
								<p class="card-text">''' + str(j.desc_short) + '''</p>
								<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
									<a href="/jobs/''' + str(j.id) + '''">''' + str(j.id) + '''</a>
								</div>
							</li>
							<li class="list-group-item">
								<h6 style="margin-top:5px;">Skills</h6>
								<div class="row" style=margin-top:10px;display:inline;">'''
			if len(j.skills(self.dbm)) > 0:
				for s in j.skills(self.dbm):
					html += '''		<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
										<span class="badge badge-pill badge-dark">''' + str(s.name) + '''</span>
									</a>'''
			else:
				html += '''
									<i style="padding-left:15px;">No associated skills identified for this experience.</i>'''
			html +=	'''			</div>
							</li>
						</ul>
					</div>
				</div>
				<br>'''

		# Render mobile view
		else:
			html += '''
						<!-- Job home tile card -->
						<div class="card w-100">
							<div class="card-header">
								<div class="row">
									<div class="col-1">
										<img width="30" height="30" src="''' + str(org_logo_src) + '''" />
									</div>
									<div class="col-8">
										<a href="/orgs/''' + str(j.org.id) + '''" style="color:black;">
											<h6 style="margin-top:5px;"><u>''' + str(j.org.name) + '''</u></h6>
										</a>
									</div>'''
			if auth:
				html += '''			<div class="col-3" style="position:relative;top:-5px;display:inline;margin-right:0px;">'''
				short_desc = j.desc_short.replace("'", "\\'")
				long_desc = j.desc_long.replace("'", "\\'")
				a_edit = "'" + j.id + "', '" + j.org.id + "', '" + j.org.name + "', '" + j.title + "', " + str(j.present) + ", '" + str(j.date_start) + "', '" + str(j.date_stop) + "', '" + short_desc + "', '" + long_desc + "', " + str(len(j.skills(self.dbm)))
				
				if len(j.skills(self.dbm)) > 0:
					eskills = j.skills(self.dbm)
					html += '''			<form id="'''+j.id+'''" style="display:none;">'''
					for i in range(len(eskills)):
						html +=			'''<input type="hidden" id="job_skill''' + str(i) + '''" value="'''+eskills[i].id+''','''+eskills[i].name+'''"></input>'''
					html += '''			</form>'''
						
				html += '''			<ul class="navbar-nav mr-auto" style="width:100%; display:inline;">
										<li class="nav-item dropdown" style="width:100%;">
											<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown08" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">Change</a>
											<div class="dropdown-menu", aria-labelledby="dropdown08">
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" onClick="edit_job('''+a_edit+''')"  data-target="#editJobModal">Edit</a>
												<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#deleteJobModal">Delete</a>
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
												<a href="/jobs/''' + str(j.id) + '''" style="color:black">
													<h5 class="card-title" ><u>''' + str(j.title) + '''</u></h5>
												</a>
											</div>
											<div class="col-4" style="text-align:right;">
												<i>
													'''+ date_start_str + ''' - ''' + date_stop_str + '''
												</i>
											</div>
										</div>

										<p class="card-text" style="padding-top:10px;">''' + str(j.desc_short) + '''</p>
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right">
											<a href="/jobs/''' + str(j.id) + '''">
												''' + str(j.id) + '''
											</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(j.skills(self.dbm)) > 0:
				for s in j.skills(self.dbm):
					html += '''				<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
												<span class="badge badge-pill badge-dark">''' + str(s.name) + '''</span>
											</a>'''
			else:
				html += '''
											<i>No associated skills identified for this experience.</i>'''

			html += '''					</div>
									</li>
								</ul>
							</div>
						</div>'''

		return html

	def render_job_page (self, this_job, next_job, last_job, mobile):
		html = ''

		# Render desktop view
		if not mobile:
			html +=	'''		<!-- Job Tile -->
							<div class="card" style="position:relative;width:70%;left:15%;top:-25px;z-index:0;">
								<div class="card-header">
									<div class="row">
										<div class="col-sm-7">
											<h4 style="vertical-align:middle;">
											''' + str(this_job.title) + '''
											</h4>
										</div>
										<div class="col-sm-5" style="text-align:right;">
											<i style="vertical-align:middle;">'''
			if this_job.present == 0:
				html += datereformat(this_job.date_start)+''' - '''+datereformat(this_job.date_stop)+'''</i>'''
			else:
				html += datereformat(this_job.date_start)+''' - Present</i>'''
			html += '''					</div>
									</div>
								</div>
								<div class="card-body" style="z-index:0;">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
											<h6>Abstract</h6>
											''' + str(this_job.desc_short) + '''
											<br><br>
											<h6>Description</h6>
											''' + str(this_job.desc_long) + '''
											<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
												<a href="/jobs/''' + str(this_job.id) + '''">
													''' + str(this_job.id) + '''
												</a>
											</div>
										</li>
										<li class="list-group-item">
											<h6 style="margin-top:5px;">Skills</h6>
											<div class="row" style="margin-top:10px;display:inline;">'''
			if len(this_job.skills(self.dbm)) > 0:
				for s in this_job.skills(self.dbm):
					html += '''					<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
													<span class="badge badge-pill badge-dark">
														''' + str(s.name) + '''
													</span>
												</a>'''
			else:
				html += '''						<i style="padding-left:15px;">No associated skills identified for this experience.</i>'''
			html += '''						</div>
										</li>
									</ul>
								<div>
							<div>'''

		# Render mobile view
		else:
			html += '''	<div class="card">
							<div class="card-body">
								<div class="row">
									<div class="col-sm-12">
										<div style="position:relative;width:50%;left:0%;display:inline;">
											<a href="/jobs/''' + str(last_job.id) + '''">< Last Job</a>
										</div>
										<div style="position:relative;width:50%;left:50%;display:inline;text-align:right;">
											<a href="/jobs/''' + str(next_job.id) + '''">Next Job ></a>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card">
							<div class="card-header">
								<div class="row">
									<div class="col-sm-12">
										<h4 style="vertical-align:middle;">
											''' + str(this_job.title) + '''
										</h4>
									</div>
									<div class="col-sm-12" style="text-align:left;">
										<i style="vertical-align:middle;">'''
			if this_job.present == 0:
				html += datereformat(this_job.date_start)+''' - '''+datereformat(this_job.date_stop)+'''</i>'''
			else:
				html += datereformat(this_job.date_start)+''' - Present</i>'''
			html += '''				</div>
								</div>
							</div>
							<div class="card-body" style="z-index:0;">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<h6>Abstract</h6>
										''' + str(this_job.desc_short) + '''
										<br><br>
										<h6>Description</h6>
										''' + str(this_job.desc_long) + '''
										<div style="position:relative;left:25%;width:75%;font-size:8px;text-align:right;">
											<a href="/jobs/''' + str(this_job.id) + '''">
												''' + str(this_job.id) + '''
											</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6 style="margin-top:5px;">Skills</h6>
										<div class="row" style="margin-top:10px;display:inline;">'''
			if len(this_job.skills(self.dbm)) > 0:
				for s in this_job.skills(self.dbm):
					html += '''				<a href="/skills/''' + str(s.id) + '''" style="padding-left:10px;">
												<span class="badge badge-pill badge-dark">
													''' + str(s.name) + '''
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
