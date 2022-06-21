import base64
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import skills
from skills import Skill
from jobs import Job
from educations import Education

class SkillRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm

	def render_skills_general (self, all_skills, mobile):
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
											<h4>Technical Skills</h4>
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
											<h4>Soft Skills</h4>
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
								<div class="col-sm-10 mx-auto">
									<div class="card w-100">
										<div class="card-header">
											<h4>Technical Skills</h4>
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
											<h4>Soft Skills</h4>
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

	def render_skills_page (self, skill, similar, appears_in, mobile):
		src = "data:image/png;base64," + skill.icon.decode('utf-8')
		html = ''

		if not mobile:
			html = '''	<div class="jumbotron">
							<div class="row">
								<div class="col-sm-8 mx-auto">
									<div class="card w-100">
										<div class="card-header" >
											<img src="''' + src + '''" width="40" height="40" style="display:inline;"/>
											<h4 style="display:inline;padding-left:15px;vertical-align:middle;">
												''' + str(skill.name) + '''
											</h4>
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
								<div class="col-sm-8 mx-auto">
									<div class="card w-100">
										<div class="card-header" >
											<img src="''' + src + '''" width="40" height="40" style="display:inline;"/>
											<h4 style="display:inline;padding-left:15px;vertical-align:middle;">
												''' + str(skill.name) + '''
											</h4>
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
																Reference: <a href="''' + str(skill.reference) + '''">Website</a>
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
