import base64
import datetime
import hashlib
import os
import sqlite3
from urllib.parse import urlencode
import uuid


class DBM:
	def __init__(self, db_path):
		self.db_path = db_path
		if self.valid():
			self.connect()
		else:
			self.instantiate()
			
	def execute(self, query):
		try:
			res = self.cur.execute(query)
			self.con.commit()
			return res
		except sqlite3.Error as e:
			print(e.args[0])
			return None
	
	def execute_d(self, query, data):
		try: 
			res = self.cur.execute(query, data)
			self.con.commit()
			return res
		except sqlite3.Error as e:
			print(e.args[0])
			return None

	def connect(self):
		self.con = sqlite3.connect(self.db_path, check_same_thread=False)
		self.cur = self.con.cursor()

	def close(self):
		self.cur.close()
		self.con.close()

	def valid(self):
		if os.path.isfile(self.db_path):
			return True
		else:
			return False
			
	def genid(self):
		id = uuid.uuid4().hex
		id = "-".join(id[i:i+8] for i in range(0, len(id), 8))
		return id
		
	def reset(self):
		self.close()
		if os.path.exists(self.db_path):
			os.remove(self.db_path)
			self.instantiate()

	def instantiate(self):
		db = open(self.db_path, "x")
		db.close()
		self.connect()
		
		with open('../dat/def/schema.sql') as sql:
			script = sql.read()
			
		self.cur.executescript(script)
		
		query = """INSERT INTO 'Groups'
					('id', 'name', 'auth_key') VALUES
					(?, ?, ?);"""
		names = [ "Owners", "Contributors", "Readers" ]
		g_ids = []
		
		for name in names:
			id = self.genid()
			g_ids.append(id)
			auth_key = uuid.uuid4().hex
			
			data = (id, name, auth_key)
			self.execute_d(query, data)
		
		query = """INSERT INTO 'Accounts'
					('id', 'username', 'password', 'salt', 'name', 'group_id') VALUES
					(?, ?, ?, ?, ?, ?);"""
		usernames = [ "admin", "member", "guest" ]
		passwords = [ "admin_pass", "member", "guest" ]
		names = [ "Administrator", "Member", "Guest" ]
		act_ids = []
		
		for i in range(len(names)):
			id = self.genid()
			act_ids.append(id)
			username = usernames[i]
			raw_pass = passwords[i]
			name = names[i]
			g_id = g_ids[i]
			salt = uuid.uuid4().hex
			password = hashlib.sha512((raw_pass + salt).encode('utf-8')).hexdigest()
			
			data = (id, username, password, salt, name, g_id)
			self.execute_d(query, data)
			
		query = """INSERT INTO 'Addresses'
					('id', 'name', 'uri', 'created_by') VALUES
					(?, ?, ?, ?);"""
		names = [ 
					"400 E North St, Jackson, MI 49202", 
					"2003 Horton Rd Suite B, Jackson, MI, 49203",
					"544 Wildwood Ave, Jackson, MI 49201",
					"1903 W Michigan Ave, Kalamazoo, MI 49008", 
					"625 Kenmoor Ave SE, Suite 311, Grand Rapids, MI 49546",
					"515 Eastern Ave, Allegan, MI 49010",
					"2111 Emmons Rd, Jackson, MI 49201",
					"10527 S Sprinkle Rd, Vicksburg, MI 49097"
				]
		a_ids = []
		cb = act_ids[0]
		
		for i in range(len(names)):
			id = self.genid()
			a_ids.append(id)
			name = names[i]
			param = [ ("q", name) ]
			uri = "https://www.google.com/search?" + urlencode(param)
			data = (id, name, uri, cb)
			self.execute_d(query, data)
			
		query = """INSERT INTO 'Skills'
					('id', 'name', 'exposure', 'soft_or_hard', 'reference', 'icon', 'category', 'created_by') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?);"""
					
		skilldata = 	[
							["Programming", 7, 1, "https://en.wikipedia.org/wiki/Computer_programming", "static/programming-ico.png", "Programming/Scripting Languages"],
							["Scripting", 7, 1, "https://www.geeksforgeeks.org/introduction-to-scripting-languages/", "static/scripting-ico.png", "Programming/Scripting Languages"],
							["C", 7, 1, "https://en.wikipedia.org/wiki/C_(programming_language)", "static/c-ico.png", "Programming/Scripting Languages"],
							["C#", 9, 1, "https://en.wikipedia.org/wiki/C_Sharp_(programming_language)",
							"static/csharp-ico.png", "Programming/Scripting Languages"],
							["Java", 8, 1, "https://en.wikipedia.org/wiki/Java_%28programming_language%29",
							"static/java-ico.png", "Programming/Scripting Languages"],
							["Python", 9, 1, "https://en.wikipedia.org/wiki/Python_(programming_language)", "static/python-ico.png", "Programming/Scripting Languages"],
							["SQL", 7, 1, "https://en.wikipedia.org/wiki/SQL", "static/sql-ico.png", "Programming/Scripting Languages"],
							["Powershell", 8, 1, "https://en.wikipedia.org/wiki/PowerShell", "static/powershell-ico.png", "Programming/Scripting Languages"],
							["C++", 5, 1, "https://en.wikipedia.org/wiki/C++", "static/cpp-ico.png", "Programming/Scripting Languages"],
							["JavaScript", 6, 1, "https://en.wikipedia.org/wiki/JavaScript", "static/js-ico.png", "Programming/Scripting Languages"],
							["PHP", 5, 1, "https://en.wikipedia.org/wiki/PHP", "static/php-ico.png", "Programming/Scripting Languages"],
							["HTML", 6, 1, "https://en.wikipedia.org/wiki/HTML", "static/html-ico.png", "Programming/Scripting Languages"],
							["CSS", 6, 1, "https://en.wikipedia.org/wiki/CSS", "static/css-ico.png", "Programming/Scripting Languages"],
							["LaTeX", 5, 1, "https://en.wikipedia.org/wiki/LaTeX", "static/latex-ico.png", "Programming/Scripting Languages"],
							["Ruby", 3, 1, "https://en.wikipedia.org/wiki/Ruby_(programming_language)", "static/ruby-ico.png", "Programming/Scripting Languages"],
							["Go", 4, 1, "https://en.wikipedia.org/wiki/Go_(programming_language)", "static/go-ico.png", "Programming/Scripting Languages"],
							["Rust", 2, 1, "https://en.wikipedia.org/wiki/Rust_(programming_language)#:~:text=Rust%20is%20a%20multi-paradigm%20programming%20language%20designed%20for,without%20garbage%20collection%2C%20and%20reference%20counting%20is%20optional.", "static/rust-ico.png", "Programming/Scripting Languages"],
							["Bash", 4, 1, "https://en.wikipedia.org/wiki/Bash_(Unix_shell)", "static/bash-ico.png", "Programming/Scripting Languages"],
							[".NET", 6, 1, "https://en.wikipedia.org/wiki/.NET_Framework", "static/dotnet-ico.png", "Frameworks"],
							["Bootstrap", 5, 1, "https://en.wikipedia.org/wiki/Bootstrap_(front-end_framework)", "static/bootstrap-ico.png", "Frameworks"],
							["Selenium", 7, 1, "https://en.wikipedia.org/wiki/Selenium_(software)", "static/selenium-ico.png", "Frameworks"],
							["Ruby on Rails", 2, 1, "https://en.wikipedia.org/wiki/Ruby_on_Rails", "static/rails-ico.png", "Frameworks"],
							["Django", 3, 1, "https://en.wikipedia.org/wiki/Django_(web_framework)", "static/django-ico.png", "Frameworks"],
							["JQuery", 3, 1, "https://en.wikipedia.org/wiki/JQuery", "static/jquery-ico.png", "Frameworks"],
							["Unity Engine", 5, 1, "https://en.wikipedia.org/wiki/Unity_(game_engine)", "static/unity-ico.png", "Frameworks"],
							["Keras", 2, 1, "https://en.wikipedia.org/wiki/Keras", "static/keras-ico.png", "Frameworks"],
							["Data Structures", 7, 1, "https://en.wikipedia.org/wiki/Data_structure", "static/datastructures-ico.png", "Theoretical Knowledge"],
							["Algorithm Analysis", 7, 1, "https://en.wikipedia.org/wiki/Analysis_of_algorithms", "static/aa-ico.png", "Theoretical Knowledge"]
						]
						
		for i in range(len(skilldata)):
			id = self.genid()
			skilldata[i].append(id)
			data = (id, skilldata[i][0], skilldata[i][1], skilldata[i][2], skilldata[i][3], self.imgtobin(skilldata[i][4]), skilldata[i][5], cb)
			self.execute_d(query, data)

		query = """INSERT INTO 'Orgs'
					('id', 'name', 'address', 'phone', 'created_by', 'website', 'logo', 'image_head', 'desc') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
		names = [ 
					"City of Jackson: Nixon Water Park", 
					"Marco's Pizza",
					"Jackson High School",
					"Western Michigan University", 
					"TEKsystems", 
					"Perrigo Company",
					"Jackson College"
				]
		descs = [
					'''Waterpark? Nixon’s got one. Skateboard park? Got that too. Four softball fields, a playground, and a picnic shelter? Let’s just call it - Nixon Park has it all.
					<br>
					Nixon Water Park and Skate Park is a great place to enjoy those hot summer days! Throughout the summer there are gym and swim days, creative themed parties, and customer appreciation discounted rate days at the water park. This water park features a zero-depth pool, along with water slides for the thrill seekers.''',
					
					'''Marco's Pizza, operated by Marco's Franchising, LLC, is an American restaurant chain and interstate franchise based in Toledo, Ohio, that specializes in Italian-American cuisine. The first store was opened in Oregon, Ohio on Starr Ave. It was founded by Italian immigrant Pasquale "Pat" Giammarco in 1978.
					''',
					
					'''Jackson High School is a public high school located near downtown Jackson, Michigan. The school was created in 1908 with the merger of Jackson's West Side and East Side High Schools and moved to its present location in 1927. The school's mascot is the Viking. The athletic teams compete as members of the Southeastern Conference as of 2018. It is a part of the Jackson Public Schools.''',
					
					'''Western Michigan University (WMU) is a public research university in Kalamazoo, Michigan. It was established in 1903 by Dwight B. Waldo. Its enrollment, as of the Fall 2019 semester, was 21,470. It is classified among "R2: Doctoral Universities – High research activity".''',
					
					'''TEKsystems is a United States-based recruitment company that provides information technology staffing solutions. It has offices in North America, Europe, and Asia. Its parent company is Allegis Group.
					<br>
					The company connects information technology professionals with companies seeking their expertise. Specialties covered by TEKsystems include cloud enablement, risk and security, data analytics and insights, enterprise applications, and more. The company has worked in the industries of financial services, healthcare services, communications, and government.
					''',
					
					'''Perrigo Company plc is an American Irish–registered manufacturer of private label over-the-counter pharmaceuticals, and while 70% of Perrigo's net sales are from the U.S. healthcare system, Perrigo is legally headquartered in Ireland for tax purposes, which accounts for 0.60% of net sales. In 2013, Perrigo completed the 6th-largest US corporate tax inversion in history when it reregistered its tax status to Ireland to avoid U.S. corporate taxes.''',
					
					'''Jackson College is a public college in Jackson County, Michigan. It was originally established as Jackson Junior College in 1928. Jackson College has been accredited by the Higher Learning Commission since 1933 and offers 48 associate degrees, certificate programs, and transfer options to Jackson County and Michigan residents. Today, the college has a yearly enrollment of nearly 8,000 students between its several locations.'''
				]
		phones = [ "5177884068", "5177800100", "5178413701", "2693872152", "6169742560", "2696738451", "5177968425" ]
		websites = 	[
						"https://www.cityofjackson.org/1072/Nixon-Skate-Park",
						"https://www.marcos.com/",
						"https://www.jpsk12.org/jacksonhs",
						"https://wmich.edu/studentaffairs",
						"https://www.teksystems.com/en",
						"https://www.perrigo.com/",
						"https://www.jccmi.edu/"
					]
		logo_paths = 	[
							"static/coj-logo.png",
							"static/marcos-logo.png",
							"static/jhs-logo.png",
							"static/wmu-logo.png",
							"static/teksystems-logo.png",
							"static/perrigo-logo.png",
							"static/jc-logo.png"
						]
		ihead_paths = 	[
							"static/coj-header.png",
							"static/marcos-header.png",
							"static/jhs-header.png",
							"static/wmu-header.png",
							"static/teksystems-header.png",
							"static/perrigo-header.png",
							"static/jc-header.png"
						]
		o_ids = []
					
		for i in range(len(names)):
			id = self.genid()
			o_ids.append(id)
			name = names[i]
			phone = phones[i]
			website = websites[i]
			desc = descs[i]
			if i == len(names) - 1:
				a_id = a_ids[5]
			else:
				a_id = a_ids[i]
			logo = self.imgtobin(logo_paths[i])
			header = self.imgtobin(ihead_paths[i])
			
			data = (id, name, a_id, phone, cb, website, logo, header, desc)
			self.execute_d(query, data)
			
		query_a = """INSERT INTO 'Jobs'
					('id', 'title', 'present', 'date_start', 'date_stop', 'desc_short',
					'desc_long', 'skill_ids', 'org_id', 'created_by') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
		query_b = """INSERT INTO 'Jobs'
					('id', 'title', 'present', 'date_start', 'desc_short',
					'desc_long', 'skill_ids', 'org_id', 'created_by') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
		titles = [ "Lifeguard", "Pizza Delivery Driver", "Offensive Coach", "Helpdesk Technician",
				   "Service Desk Analyst", "Sr Service Desk Analyst", "Service Desk Supervisor" ]
		present = [ 0, 0, 0, 0, 0, 0, 1 ]
		date_starts = [ "06/01/2011", "06/01/2013", "10/01/2012", "09/01/2014", 
						"10/01/2016", "12/01/2017", "03/01/2020" ]
		date_ends = [ "09/01/2012", "09/01/2013", "04/01/2013", "09/01/2016",
						"12/01/2017", "03/01/2020", None ]
		desc_shorts = 	[ 
							"""Summer job in which lifeguard training and certification from the Red Cross was received to prepare for role. Duties included opening and closing off the pool, providing swim lessons, monitoring activities in the pool area, and identifying any safety issues.""",
							
							"""Summer job delivering pizzas to clientele. Cross-trained to be able to not only deliver food to clients and on good customer service practices, but also to prepare and make the food, as well as sanitation and food safety practices.""",
							
							""""Volunteer experience coaching high school hockey at alma mater. Duties included assembling offensive line combinations, calling lines during games, and practice planning.""",
							
							"""Assisted in the management of computer environment by providing physical and remote support to clientele. Experiences with hardware and software troubleshooting, service delivery, project management, knowledge management and asset management were attained. Some additional experience attained in development of software and OS image deployment scripting.""",
							
							"""Provide quality service support in a large, multi-national business environment. Duties include analyzing, interpreting, and resolving user issues in strong collaboration with a team.""",
							
							"""Provide quality service support in a large, multi-national business environment. Duties include analyzing, interpreting, and resolving user issues in strong collaboration with a team. Solely responsible for maintaining the company's US mobility (cellular) program. Obtained some experience developing automated solutions, primarily in .NET and python, used intrateam to streamline processes.""",
							
							"""Directly manage a small team of remote service desk staff, providing day-to-day guidance and delegation. Obtained some experiences in project management, interfacing with a wide variety of IT and business stakeholders to address requirements with respect to the team."""
						]
						
		desc_longs = 	[
							"""Summer job in which lifeguard training and certification from the Red Cross was received to prepare for role. Duties included opening and closing off the pool, providing swim lessons, monitoring activities in the pool area, and identifying any safety issues.""",
							
							"""Summer job delivering pizzas to clientele. Cross-trained to be able to not only deliver food to clients and on good customer service practices, but also to prepare and make the food, as well as sanitation and food safety practices.""",
							
							"""Volunteer experience coaching high school hockey at alma mater. Duties included assembling offensive line combinations, calling lines during games, and practice planning.""",
							
							"""Assisted in the management of computer environment by providing physical and remote support to clientele. Experiences with hardware and software troubleshooting, service delivery, project management, knowledge management and asset management were attained. Some additional experience attained in development of software and OS image deployment scripting.""",
							
							"""Provide quality service support in a large, multi-national business environment. Duties include analyzing, interpreting, and resolving user issues in strong collaboration with a team.""",
							
							"""Provide quality service support in a large, multi-national business environment. Duties include analyzing, interpreting, and resolving user issues in strong collaboration with a team. Solely responsible for maintaining the company's US mobility (cellular) program. Obtained some experience developing automated solutions, primarily in .NET and python, used intrateam to streamline processes.""",
							
							"""Directly manage a small team of remote service desk staff, providing day-to-day guidance and delegation. Obtained some experiences in project management, interfacing with a wide variety of IT and business stakeholders to address requirements with respect to the team."""
						]
		skill_ids = 	[
							[],
							[],
							[],
							[ skilldata[7][6], skilldata[1][6] ],
							[],
							[],
							[]
						]
		presents = [ 0, 0, 0, 0, 0, 0, 1 ]
		org_ids = [ o_ids[0], o_ids[1], o_ids[2], o_ids[3], o_ids[4], o_ids[5], o_ids[5]]
		
		for i in range(len(titles)):
			id = self.genid()
			title = titles[i]
			present = presents[i]
			date_start = date_starts[i]
			date_end = date_ends[i]
			desc_short = desc_shorts[i]
			desc_long = desc_longs[i]
			skill_id = ""
			for j in range(len(skill_ids[i])):
				if (j != len(skill_ids[i]) - 1):
					skill_id += skill_ids[i][j] + ","
				else:
					skill_id += skill_ids[i][j]
					
			if present == 1:
				if (len(skill_ids) > 0):
					data = (id, title, present, date_start, desc_short, desc_long, skill_id, org_ids[i], cb)
					self.execute_d(query_b, data)
				else:
					data = (id, title, present, date_start, desc_short, desc_long, None, org_ids[i], cb)
					self.execute_d(query_b, data)
			else:
				if (len(skill_ids) > 0):
					data = (id, title, present, date_start, date_end, desc_short, desc_long, skill_id, org_ids[i], cb)
					self.execute_d(query_a, data)
				else:
					data = (id, title, present, date_start, date_end, desc_short, desc_long, None, org_ids[i], cb)
					self.execute_d(query_a, data)
			
			
		query = '''INSERT INTO 'Contact'
					('id', 'name', 'address', 'phone1', 'phone2', 'email', 'created_by', 'objective') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?);'''
		id = self.genid()
		addr = a_ids[7]
		obj = "To secure a software engineering role in a team-driven environment that utilizes my exceptional work ethic, accessible demeanor, and technical expertise."
		data = (id, "Tom Esser", addr, "3057109723", "5177401802", "esserth1@outlook.com", cb, obj)
		self.execute_d(query, data)
		
		query = '''INSERT INTO 'Education'
					('id', 'org', 'degree', 'gpa', 'skill_ids', 'created_by', 'date_end', 'desc_short', 'desc_long') VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
		
		edu_data = [
						[o_ids[2], "High School Diploma", 4.0, None, cb, "06/01/2012", '''Graduated as class valedictorian. Particpiated in National Honor Society and school sports including hockey and soccer.''', "Placeholder1"],
						[o_ids[6], "Associate in Applied Science", 3.2, None, cb, "05/01/2013", '''Academic experiences with technical skills, including systems design and analysis, project management, and multiple programming language proficiencies, and soft skills, including, leadership and intrapersonal development and communication.''', "Placeholder2"],
						[o_ids[3], "Bachelor in Computer Science", 3.0, None, cb, "12/01/2021", '''Academic experiences with theoretical aspects of computer programming, including systems programming and algorithmic logic and design. Further experience attained in software development lifecycle paradigms and project management. Obtained some graduate level experiences with data structures and database management systems design.''', "Placeholder3"]
					]
					
		for i in range(len(edu_data)):
			id = self.genid()
			data = (id, edu_data[i][0], edu_data[i][1], edu_data[i][2], edu_data[i][3], edu_data[i][4], edu_data[i][5], edu_data[i][6], edu_data[i][7])
			self.execute_d(query, data)
		
		
	def imgtobin(self, path):
		file = open(path, 'rb').read()
		file = base64.b64encode(file)
		return file
		
		