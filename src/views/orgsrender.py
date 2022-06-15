import base64
import sys
sys.path.append("../models")

import dbm
from dbm import DBM
import orgs
from orgs import Org
from fmat import addresslines, telelink, teleformat

g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"

class OrgRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm
		
	def render_org_tile (self, mobile, **kwargs):
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
			
		if not mobile:
			html = '''	<div class="jumbotron">
							<img src="'''+head+'''" style="position:relative;width:70%;left:15%;z-index:0;max-height:25%;"/>'''
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
										<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index:2">
											<img src="''' +  logo + '''" width="45" height="45" />
										</div>
										<a href="/orgs/''' + str(this_org.id) + '''" style="color:black;">
											<h4 style="display:inline;padding-left:10px;vertical-align:middle;">
												''' + str(this_org.name) + '''
											</h4>
										</a>
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
			if this_job != None and next_job != None and last_job != None:
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
									<div style="width:45px;height:45px;border-radius:50%;background-color:#FFF;display:inline-block;z-index=2;">
										<img src="'''+logo+'''" width="45" height="45"/>
									</div>
									<a href="/orgs/''' + str(this_org.id) + '''" style="color:black;"><u>
										<h4 style="display:inline;padding-left:10px;vertical-align:middle;">
											''' + str(this_org.name) + '''</u></h4>
									</a>
								</div>'''
			if this_job == None and this_edu == None:
				html += '''
								<div class="card-body" style="z-index:0;">
									<div class="row">
										<div class="col-sm-8">
											<h6>Description:</h6>
											''' + str(this_org.desc_short) + '''<br><br>
										</div>
										<div class="col-sm-4">
												<h6>Information:</h6>
												''' + addresslines(str(this_org.address))+'''
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