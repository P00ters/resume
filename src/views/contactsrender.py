import sys
sys.path.append("../models")

import dbm
from dbm import DBM
from contacts import Contact
from fmat import teleformat, telelink


class ContactRenderer:
	def __init__ (self, dbm):
		self.dbm = dbm
		
	def render_home_contact (self, contact, mobile):
		html = ''
		
		if not mobile:
			html += '''
				<div style="background-color:#c6bc24;position:relative;width:100%;">
					<h1 style="position:absolute;left:50%;top:25%;color:white;font-size:55px;">
						''' + str(contact.name) + '''
					</h1>

					<div style="position:absolute;left:50%;top:55%;z-index:2;">
						<img src="/static/Addr.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="''' + str(contact.address.uri) + '''" style="color:white;" target="_blank">''' + str(contact.address.name) + '''</a>
						</h4>
					</div>

					<div style="position:absolute;left:50%;top:67.5%;z-index:2;">
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;padding-left:5px;position:relative;top:5px;">
						<a href="''' + telelink(str(contact.phone1)) + '''" style="color:white;">''' + teleformat(str(contact.phone1)) + '''</a></h4>
						<img src="/static/Phone.png" width="35" height=35" style="display:inline;position:relative;left:50px;" />
						<h4 style="display:inline;padding-left:5px;position:relative;left:50px;top:5px;">
						<a href="''' + telelink(str(contact.phone2)) + '''" style="color:white;">''' + teleformat(str(contact.phone2)) + '''</a></h4>
					</div>

					<div style="position:absolute;left:50%;top:80%;z-index:2;">
						<img src="/static/Mail.png" width="35" height=35" style="display:inline;" />
						<h4 style="display:inline;position:relative;top:5px;left:5px;">
							<a href="mailto:''' + str(contact.email) + '''" style="color:white;">''' + str(contact.email) +'''</a>
						</h4>
					</div>

					<img src="/static/HeaderAnim.gif" style="position:relative;width:100%;"/>

				</div>
				<br>'''
			html +='''	<div class="row" style="overflow:hidden;">
					<div class="col-sm-5" style="padding-left:40px;">
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
								<h4>Contact Information</h4>
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
									<h4 style="padding-left:20px;">Objective</h4>
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