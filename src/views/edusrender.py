import base64
import datetime
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import educations
from educations import Education
import skills
from skills import Skill
from fmat import datereformat

class EduRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm
		
	def render_home_tile (self, e, mobile):
		# Set logo source
		src = "data:image/png;base64," + e.org.logo.decode('utf-8')
		date_stop = datetime.datetime.strptime(e.date_stop, '%Y-%m-%d')
		date_stop_str = date_stop.strftime('%b %Y')
		html = ''
		
		if not mobile:
			html += '''	<div class="card w-75">
							<div class="card-header">
								<div class="row">
									<div class="col-1">
										<img width="30" height="30" src="''' + src + '''" />
									</div>
									<div class="col-6">
										<a href="/orgs/''' + str(e.org.id) + '''" style="color:black;">
											<h6 style="margin-top:5px;">''' + str(e.org.name) + '''</h6>
										</a>
									</div>
								</div>
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
									<div class="col-11">
										<a href="/orgs/'''+str(e.org.id)+'''" style="color:black;">
										<h6 style="margin-top:5px;"><u>''' + str(e.org.name) + '''</u></h6>
										</a>
									</div>
								</div>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<div class="row">
											<div class="col-7">
												<a href="/edus/'''+str(e.id)+'''" style="color:black;">
												<h5 class="card-title"><u>''' + str(e.degree) + '''</u></h5></a>
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