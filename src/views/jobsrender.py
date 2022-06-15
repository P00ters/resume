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
	
	def render_home_tile (self, j, mobile):
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
							<div class="col-1">
								<img width="30" height="30" src="''' + org_logo_src + '''" />
							</div>
							<div class="col-6">
								<a href="/orgs/''' + str(j.org.id) + '''" style="color:black;">
									<h6 style="margin-top:5px;">''' + str(j.org.name) + '''</h6>
								</a>
							</div>
						</div>
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
									<div class="col-11">
										<a href="/orgs/''' + str(job.org.id) + '''" style="color:black;">
											<h6 style="margin-top:5px;"><u>''' + str(j.org.name) + '''</u></h6>
										</a>
									</div>
								</div>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<div class="row">
											<div class="col-7">
												<a href="/jobs/''' + str(j.id) + '''" style="color:black">
													<h5 class="card-title"><u>''' + str(j.title) + '''</u></h5>
												</a>
											</div>
											<div class="col-5" style="text-align:right;">
												<i style="margin-top:5px;">
													'''+ date_start_str + ''' - ''' + date_stop_str + '''
												</i>
											</div>
										</div>
										
										<p class="card-text">''' + str(j.desc_short) + '''</p>
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
										<div style="position:relative;width:50%;lef:50%;display:inline;">
											<a href="/jobs/''' + str(next_job.id) + '''">Next Job ></a>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="card">
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