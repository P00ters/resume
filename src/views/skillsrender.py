import base64
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import skills
from skills import Skill
from jobs import Job, retrieve_all_jobs
from educations import Education, retrieve_all_educations
from fmat import sanitize

class SkillRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm

	def render_skills_general (self, all_skills, mobile, auth):
		html = ''

		if not mobile:
			html += '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-6 mx-auto">
									<h1 style="text-align:center;">Skills</h1>
								</div>
							</div>
							<br>
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card w-100">
										<div class="card-header">
											<div class="row">
												<div class="col-11" >
													<h4 style="padding-top:10px;">Technical Skills</h4>
												</div>
												<div class="col-1">'''
			if auth:
				html += '''							<a href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal"><button type="button" style="position:relative;width:50px;display:inline;margin-right:0px;margin-left:auto;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>'''
			html += '''							</div>
											</div>
										</div>
										<div class="card-body">
											<div class="row">'''
			for s in all_skills:
				if s.soft_or_hard == 1:
					src = "data:image/png;base64," + s.icon.decode('utf-8')
					html +=	'''					<div class="col-sm-2">
													<a href="/skills/''' + str(s.id) + '''">
														<span style="display:inline;">
															<img src="''' + src + '''" width="25" height="25" />
															<span class="badge badge-pill badge-dark">
																''' + str(s.name) + '''
															</span>
														</span>
													</a>
												</div>'''
			html += '''						</div>
										</div>
									</div>
								</div>
							</div>
							<br>
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card w-100">
										<div class="card-header">
											<div class="row">
												<div class="col-11" >
													<h4 style="padding-top:10px;">Soft Skills</h4>
												</div>
												<div class="col-1">'''
			if auth:
				html += '''							<a href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal"><button type="button" style="position:relative;width:50px;display:inline;margin-right:0px;margin-left:auto;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>'''
			html += '''							</div>
											</div>
										</div>
										<div class="card-body">
											<div class="row">'''
			for s in all_skills:
				if s.soft_or_hard == 0:
					src = "data:image/png;base64," + s.icon.decode('utf-8')
					html +=	'''					<div class="col-sm-2">
													<a href="/skills/''' + str(s.id) + '''">
														<span style="display:inline;">
															<img src="''' + src + '''" width="25" height="25" />
															<span class="badge badge-pill badge-dark">
																''' + str(s.name) + '''
															</span>
														</span>
													</a>
												</div>'''
			html += '''						</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						'''
		else:
			html = '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-6 mx-auto">
									<h1 style="text-align:center;">Skills</h1>
								</div>
							</div>
							<br>
							<div class="row">
								<div class="col-sm-12 mx-auto">
									<div class="card w-100">
										<div class="card-header">
											<div class="row">
												<div class="col-9">
													<h4>Technical Skills</h4>
												</div>
												<div class="col-3">'''
			if auth:
					html += '''						<ul class="navbar-nav mr-auto" style="width:100%; 
														<li class="nav-item dropdown" style="width:100%;">
															<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown10" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;vertical-align:middle;">Change</a>
															<div class="dropdown-menu", aria-labelledby="dropdown10">
																<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal">New</a>
															</div>
														</li>
													</ul>'''
			html += '''							</div>
											</div>
										</div>
										<div class="card-body">
											<div class="row">'''
			for s in all_skills:
				if s.soft_or_hard == 1:
					src = "data:image/png;base64," + s.icon.decode('utf-8')

					html += '''					<div class="col-sm-4">
													<a href="/skills/''' + str(s.id) + '''">
														<span style="display:inline;">
															<img src="''' + src + '''" width="25" height="25" />
															<span class="badge badge-pill badge-dark">
																''' + str(s.name) + '''
															</span>
														</span>
													</a>
												</div>'''
			html +=	'''						</div>
										</div>
									</div>
								</div>
							</div>
							<br>
							<div class="row">
								<div class="col-sm-10 mx-auto">
									<div class="card w-100">
										<div class="card-header">
											<div class="row">
												<div class="col-9">
													<h4>Soft Skills</h4>
												</div>
												<div class="col-3">'''
			if auth:
					html += '''						<ul class="navbar-nav mr-auto" style="width:100%; 
														<li class="nav-item dropdown" style="width:100%;">
															<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown10" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;vertical-align:middle;">Change</a>
															<div class="dropdown-menu", aria-labelledby="dropdown10">
																<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal">New</a>
															</div>
														</li>
													</ul>'''
			html += '''							</div>
											</div>
										</div>
										<div class="card-body">
											<div class="row">'''
			for s in all_skills:
				if s.soft_or_hard == 0:
					src = "data:image/png;base64," + s.icon.decode('utf-8')

					html += '''					<div class="col-sm-4">
													<a href="/skills/''' + str(s.id) + '''">
														<span style="display:inline;">
															<img src="''' + src + '''" width="25" height="25" />
															<span class="badge badge-pill badge-dark">
																''' + str(s.name) + '''
															</span>
														</span>
													</a>
												</div>'''
			html += '''						</div>
										</div>
									</div>
								</div>
							</div>
						</div>'''


		return html

	def render_skills_page (self, skill, similar, appears_in, mobile, auth):
		src = "data:image/png;base64," + skill.icon.decode('utf-8')
		html = ''
		
		if auth:
			s = skill
			s_edit = "'" + sanitize(s.id) + "', '" + sanitize(s.name) + "', " + str(s.exposure) + ", '" + str(s.soft_or_hard) + "', '" + sanitize(s.reference) + "', '" + sanitize(s.category) + "', '" + sanitize(s.desc_short) + "', '" + sanitize(s.desc_long) + "', '" + str(mobile) + "'"
			
			js = retrieve_all_jobs(self.dbm)
			es = retrieve_all_educations(self.dbm)
			
			jdangles = ""
			b_jdangles = 1
			edangles = ""
			b_edangles = 1
			if len(js) > 0:
				for j in js:
					split = j.skill_ids.split(',')
					for item in split:
						if item == s.id:
							jdangles += j.id + ',' + j.title + ','
				jdangles = jdangles[:-1]
			else:
				b_jdangles = 0
			if len(es) > 0:
				for e in es:
					split = e.skill_ids.split(',')
					for item in split:
						if item == s.id:
							edangles += e.id + ',' + e.degree + ','
				edangles = edangles[:-1]
			else:
				b_edangles = 0
			
			
			s_del = "'" + sanitize(s.id) + "', '" + sanitize(s.name) + "', " + str(b_jdangles) + ", '" + sanitize(jdangles) + "', " + str(b_edangles) + ", '" + sanitize(edangles) + "', '" + str(mobile) + "'"
			
			

		if not mobile:
			html = '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-8 mx-auto">
									<div class="card w-100">
										<div class="card-header" >
											<div class="row">
												<div class="col-9">
													<img src="''' + src + '''" width="40" height="40" style="display:inline;"/>
													<h4 style="display:inline;padding-left:15px;vertical-align:middle;">
														''' + str(skill.name) + '''
													</h4>
												</div>
												<div class="col-3">'''
			if auth:
				
				html += '''				
													<a href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal"><button type="button" style="position:relative;width:50px;display:inline;left:10px;" class="btn btn-outline-success btn-lg btn-block"><img src="/static/add.png" width="30" /></button></a>
													<a href="javascript:void(0)" data-toggle="modal" data-target="#editSkillModal">
														<button style="position:relative;width:50px;display:inline;left:30px;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_skill('''+s_edit+''')" id="edit_skill_btn"><img src='/static/edit.png' width="30"/></button>
													</a>
													<a href="javascript:void(0)" data-toggle="modal" data-target="#delSkillModal">
														<button style="position:relative;width:50px;display:inline;left:50px;" type="button" class="btn btn-outline-danger btn-lg btn-block" id="skill_del_btn" onClick="del_skill('''+s_del+''')"><img src='/static/delete.png' width="30"/></button>
													</a>'''
				html += '''							<form id="''' + skill.id + '''" style="display:none;">
														<input type="hidden" id="skill_icon_bin" value="data:image/png;base64,''' + skill.icon.decode('utf-8') + '''"></input>
													</form>'''
			html += '''							</div>
											</div>
										</div>
										<div class="card-body">
											<ul class="list-group list-group-flush">
												<li class="list-group-item">
													<div class="row">
														<h5>Details</h5>
													</div><br>
													<div class="row">
														<div class="col-sm-6">
															<h6>Comments</h6>
														</div>
														<div class="col-sm-6">
															<h6>Exposure</h6>
														</div>
													</div>
													<div class="row">
														<div class="col-sm-8">
															''' + str(skill.desc_long) + '''
														</div>
														<div class="col-sm-4">
															<div class="progress">
																<div class="progress-bar" role="progressbar" aria-valuenow="'''+str(skill.exposure * 10)+'''" aria-valuemin="0" aria-valuemax="100" style="width: '''+str(skill.exposure * 10)+'''%;"></div>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Meta</h5>
													</div>
													<div class="row">
														<div class="col-sm-6">
															<h6>Description</h6>
														</div>
														<div class="col-sm-4">
															<h6>Information</h6>
														</div>
													</div>
													<div class="row">
														<div class="col-sm-6">
															''' + str(skill.desc_short) + '''
														</div>
														<div class="col-sm-4">
															<div>
																Technical Skill: '''
			if skill.soft_or_hard == 1:
				html += '''											<b>True</b>'''
			else:
				html += '''											<b>False</b>'''
			html +=	'''											<br>
																	Category: <b> ''' + str(skill.category) + ''' </b>
																<br>
																Reference: <a href="''' + str(skill.reference) + '''" target="_blank">Website</a>
																<br>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Similar</h5>
													</div>
													<div class="row">'''
			if len(similar) > 0:
				for s in similar:
					src = "data:image/png;base64," + s.icon.decode('utf-8')
					name = str(s.name)
					if len(name) > 16:
						name = name[:14] + '...'
					html += '''							<div class="col-sm-2">
															<a href="/skills/''' + s.id + '''">
																<span style="display:inline;">
																	<img src="'''+src+'''" width="25" height="25" />
																	<span class="badge badge-pill badge-dark">'''+name+'''</span>
																</span>
															</a>
														</div>'''
				html += '''							</div>'''
			else:
				html += '''								<i>No skills found in a similar category</i>
													</div>'''
			html += '''							</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Exposed In</h5>
													</div>'''
			if len(appears_in[0]) == 0 and len(appears_in[1]) == 0:
				html += '''							<div class="row" >
														<i>No appearances in education or work experiences<i>
													</div>'''
			else:
				if len(appears_in[0]) > 0:
					html +=	'''						<div class="row" style="padding-top:10px;">
														<div class="col-sm-12">
															<h6>Work Experiences</h6>
														</div>
													</div>
													<div class="row">'''
					for exp in appears_in[0]:
						img = "data:image/png;base64," + exp.org.logo.decode('utf-8')
						html += '''						<div class="col-sm-6">
															<span style="display:inline;">
																<a href="/jobs/''' + str(exp.id) + '''">
																	<img src="''' + img + '''" width="25" height="25" />
																	''' + str(exp.org.name) + ''' - ''' + str(exp.title) + '''
																</a>
															</span>
														</div>'''
					html += '''						</div>'''
				if len(appears_in[1]) > 0:
					html += '''						<div class="row" style="padding-top:10px;">
														<div class="col-sm-12">
															<h6>Education</h6>
														</div>
													</div>
													<div class="row">'''
					for exp in appears_in[1]:
						img = "data:image/png;base64," + exp.org.logo.decode('utf-8')
						html += '''						<div class="col-sm-6">
															<span style="display:inline;">
																<a href="/edus/''' + str(exp.id) + '''">
																	<img src="''' + img + '''" width="25" height="25" />
																	''' + str(exp.org.name) + ''' - ''' + str(exp.degree) + '''
																</a>
															</span>
														</div>'''
					html += '''						</div>'''
			html += '''							</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</div>'''

		else:
			src = "data:image/png;base64," + skill.icon.decode('utf-8')

			html += '''	<div class="jumbotron">
							<div class="row">
								<div class="col-12">
									<div class="card w-100">
										<div class="card-header" >
											<div class="row">
											<div class="col-9">
												<img src="''' + src + '''" width="40" height="40" style="display:inline;"/>
												<h4 style="display:inline;padding-left:15px;vertical-align:middle;">
													''' + str(skill.name) + '''
												</h4>
											</div>
											<div class="col-3">'''
			if auth:
				html += '''						<ul class="navbar-nav mr-auto" style="width:100%; 
													<li class="nav-item dropdown" style="width:100%;">
														<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown10" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;vertical-align:middle;">Change</a>
														<div class="dropdown-menu", aria-labelledby="dropdown10">
															<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#addSkillModal">New</a>
															<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" onClick="edit_skill('''+s_edit+''')"  data-target="#editSkillModal" id="edit_skill_btn">Edit</a>
															<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#delSkillModal" id="skill_del_btn"  onClick="del_skill('''+s_del+''')">Delete</a>
														</div>
													</li>
												</ul>'''
				html += '''							<form id="''' + skill.id + '''" style="display:none;">
														<input type="hidden" id="skill_icon_bin" value="data:image/png;base64,''' + skill.icon.decode('utf-8') + '''"></input>
													</form>'''
			html += '''						</div>
											</div>
										</div>
										<div class="card-body">
											<ul class="list-group list-group-flush">
												<li class="list-group-item">
													<div class="row">
														<h5>Details</h5>
													</div><br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Comments</h6>
														</div>
														<div class="col-sm-8">
															''' + str(skill.desc_long) + '''
														</div>
													</div>
													<br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Exposure</h6>
														</div>
														<div class="col-sm-8">
															<div class="progress">
																<div class="progress-bar" role="progressbar" aria-valuenow="'''+str(skill.exposure * 10)+'''" aria-valuemin="0" aria-valuemax="100" style="width: '''+str(skill.exposure * 10)+'''%;"></div>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Meta</h5>
													</div>
													<div class="row">
														<div class="col-sm-4">
															<h6>Description</h6>
														</div>
														<div class="col-sm-8">
															''' + str(skill.desc_short) + '''
														</div>
													</div>
													<br>
													<div class="row">
														<div class="col-sm-4">
															<h6>Information</h6>
														</div>
														<div class="col-sm-8">
															<div>
																Technical Skill: '''
			if skill.soft_or_hard == 1:
				html += '''											<b>True</b>'''
			else:
				html += '''											<b>False</b>'''
			html +=	'''											<br>
																	Category: <b> ''' + str(skill.category) + ''' </b>
																<br>
																Reference: <a href="''' + str(skill.reference) + '''" target="_blank">Website</a>
																<br>
															</div>
														</div>
													</div>
												</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Similar</h5>
													</div>
													<div class="row">'''
			if len(similar) > 0:
				for s in similar:
					src = "data:image/png;base64," + s.icon.decode('utf-8')
					name = str(s.name)
					if len(name) > 16:
						name = name[:14] + '...'
					html += '''							<div class="col-sm-6">
															<a href="/skills/'''+s.id+'''">
																<span style="display:inline;">
																	<img src="''' + src + '''" width="25" height="25" />
																	<span class="badge badge-pill badge-dark">'''+name+'''</span>
																</span>
															</a>
														</div>'''
				html += '''							</div>'''
			else:
				html += '''								<i>No skills found in a similar category</i>
													</div>'''
			html += '''							</li>
												<li class="list-group-item">
													<div class="row">
														<h5>Exposed In</h5>
													</div>'''
			if len(appears_in[0]) == 0 and len(appears_in[1]) == 0:
				html += '''							<div class="row" >
														<i>No appearances in education or work experiences<i>
													</div>'''
			else:
				if len(appears_in[0]) > 0:
					html +=	'''						<div class="row" style="padding-top:10px;">
														<div class="col-sm-12">
															<h6>Work Experiences</h6>
														</div>
													</div>
													<div class="row">'''
					for exp in appears_in[0]:
						img = "data:image/png;base64," + exp.org.logo.decode('utf-8')
						html += '''						<div class="col-sm-6">
															<span style="display:inline;">
																<a href="/jobs/''' + str(exp.id) + '''">
																	<img src="''' + img + '''" width="25" height="25" />
																	''' + str(exp.org.name) + ''' - ''' + str(exp.title) + '''
																</a>
															</span>
														</div>'''
					html += '''						</div>'''
				if len(appears_in[1]) > 0:
					html += '''						<div class="row" style="padding-top:10px;">
														<div class="col-sm-12">
															<h6>Education</h6>
														</div>
													</div>
													<div class="row">'''
					for exp in appears_in[1]:
						img = "data:image/png;base64," + exp.org.logo.decode('utf-8')
						html += '''						<div class="col-sm-6">
															<span style="display:inline;">
																<a href="/edus/''' + str(exp.id) + '''">
																	<img src="''' + img + '''" width="25" height="25" />
																	''' + str(exp.org.name) + ''' - ''' + str(exp.degree) + '''
																</a>
															</span>
														</div>'''
					html += '''						</div>'''
			html += '''							</li>
											</ul>
										</div>
									</div>
								</div>
							</div>
						</div>'''

		return html
