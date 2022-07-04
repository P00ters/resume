import sys
sys.path.append("../models")

import dbm
from dbm import DBM
from contacts import Contact
from fmat import teleformat, telelink, sanitize
g_api = "AIzaSyAQmRwQrAmnbDOU_d0ILUMlT2l9OAldR00"

class ContactRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm

	def render_home_contact (self, contact, mobile, auth):
		html = ''

		if not mobile:
			html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;overflow-y:hidden;overflow-x:hidden;">
					<div style="position:absolute;left:50%;height:100%;width:50%;">
						<div style="position:relative;height:50%;width:100%;">
							<h1 style="position:relative;top:50%;color:white;font-size:55px;display:inline;">
								''' + str(contact.name) + '''
							</h1>'''
			if auth:
				a_edit = "'" + sanitize(contact.id) + "', '" + sanitize(contact.name) + "', '" + sanitize(contact.phone1) + "', '" + sanitize(contact.phone2) + "', '" + sanitize(contact.email) + "', '" + sanitize(contact.objective) + "', '" + sanitize(contact.address.id) + "', '" + sanitize(contact.address.name) + "'"
			
				html +=	'''	
							<a href="javascript: void(0)" data-toggle="modal" data-target="#editContactModal">
								<button style="position:relative;top:42.5%;width:50px;left:25px;z-index:20;display:inline;" type="button" class="btn btn-outline-warning btn-lg btn-block" onClick="edit_contact('''+a_edit+''')"><img src='/static/edit.png' width="30"/></button>
							</a>'''
					
			html +='''	</div>
						<div style="position:relative;height:45%;width:100%;top:2.5%">
							<div class="row" style="padding-top:5px;z-index:2;">
								<div class="col-12">
									<img src="/static/Addr.png" width="35" height=35" style="display:inline;" />
									<h4 style="display:inline;position:relative;top:5px;left:5px;z-index:2;">
										<a href="''' + str(contact.address.uri) + '''" style="color:white;" target="_blank">''' + str(contact.address.name) + '''</a>
									</h4>
								</div>
							</div>
							<div class="row" style="padding-top:5px;z-index:2;">
								<div class="col-12" style="z-index:2;">
									<img src="/static/Phone.png" width="35" height=35" style="display:inline;" />
									<h4 style="display:inline;padding-left:5px;position:relative;top:5px;">
									<a href="''' + telelink(str(contact.phone1)) + '''" style="color:white;">''' + teleformat(str(contact.phone1)) + '''</a></h4>
									<img src="/static/Phone.png" width="35" height=35" style="display:inline;position:relative;left:50px;" />
									<h4 style="display:inline;padding-left:5px;position:relative;left:50px;top:5px;">
									<a href="''' + telelink(str(contact.phone2)) + '''" style="color:white;">''' + teleformat(str(contact.phone2)) + '''</a></h4>
								</div>
							</div>
							<div class="row" style="padding-top:5px;z-index:2;">
								<div class="col-12">
									<img src="/static/Mail.png" width="35" height=35" style="display:inline;" />
									<h4 style="display:inline;position:relative;top:5px;left:5px;z-index:2;">
										<a href="mailto:''' + str(contact.email) + '''" style="color:white;">''' + str(contact.email) +'''</a>
									</h4>
								</div>
							</div>
						</div>
					</div>
					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;top:0%;"/>
				</div>
				<br>'''
			html +='''	<div class="row" style="overflow:hidden;padding-left:25px;">
					<div class="col-sm-5">
						<h2 class="mb-4">Objective</h2>
							<div class="card w-75">
								<div class="card-body">
									''' + str(contact.objective) + '''
								</div>
							</div>
						<br>'''

		else:
			html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;">
					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;"/>
				</div>
				<div class="row" style="overflow:hidden;">
					<div class="col-sm-12">
						<div class="card">
							<div class="card-header">
								<div class="row">
									<div class="col-9">
										<h4>Contact Information</h4>
									</div>'''
			if auth:
				a_edit = "'" + sanitize(contact.id) + "', '" + sanitize(contact.name) + "', '" + sanitize(contact.phone1) + "', '" + sanitize(contact.phone2) + "', '" + sanitize(contact.email) + "', '" + sanitize(contact.objective) + "', '" + sanitize(contact.address.id) + "', '" + sanitize(contact.address.name) + "'"
				
				html +=	'''			<div class="col-3" style="position:relative;top:-5px;display:inline;margin-right:0px;">
										<ul class="navbar-nav mr-auto" style="width:100%; display:inline;">
											<li class="nav-item dropdown" style="width:100%;">
												<a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="text-align:right;position:relative;width:100%;">Change</a>
												<div class="dropdown-menu", aria-labelledby="dropdown04">
													<a class="dropdown-item" href="javascript:void(0)" data-toggle="modal" data-target="#editContactModal" onClick="edit_contact('''+a_edit+''')">Edit</a>
												</div>
											</li>
										</ul>
									</div>
								'''
			html += '''			</div>
							</div>
							<div class="card-body">
								<ul class="list-group list-group-flush">
									<li class="list-group-item">
										<h5>''' + str(contact.name) + '''</h5>
									</li>
									<li class="list-group-item">
										<h6>Phone</h6>
										<div class="col-sm-6" style="display:inline;">
											<a href="''' + telelink(str(contact.phone1)) + '''">''' + teleformat(str(contact.phone1))+'''</a>
										</div>
										<div class="col-sm-6" style="display:inline;">
											<a href="''' + telelink(str(contact.phone2)) + '''">''' + teleformat(str(contact.phone2)) + '''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6>Email</h6>
										<div class="col-sm-12">
											<a href="mailto:''' + str(contact.email) + '''">''' + str(contact.email) + '''</a>
										</div>
									</li>
									<li class="list-group-item">
										<h6>Address</h6>
										<div class="col-sm-12">
											<a href="''' + str(contact.address.uri) +'''" target="_blank">''' + str(contact.address.name) + '''</a>
										</div>
										<div class="col-sm-12">
											<iframe
												width="325"
												height="200"
												frameborder="0" style="border:0"
												referrerpolicy="no-referrer-when-downgrade"
												src="https://www.google.com/maps/embed/v1/place?key=''' + g_api + '''+&q=''' + str(contact.address.name) + '''"
												allowfullscreen>
											</iframe>
										</div>
									</li>
								</ul>
							</div>
						</div>'''
			html += '''
							<div class="card">
								<div class="card-header">
									<div class="row">
										<div class="col-8">
											<h4>Objective</h4>
										</div>
									</div>
								</div>
								<div class="card-body">
									<ul class="list-group list-group-flush">
										<li class="list-group-item">
										''' + str(contact.objective) + '''
										</li>
									</ul>
								</div>
							</div>'''

		return html
