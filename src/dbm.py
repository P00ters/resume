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
					('id', 'name', 'exposure', 'soft_or_hard', 'reference', 'icon', 'category', 'created_by', desc, desc_long) VALUES
					(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
					
		skilldata = 	[
							["Programming", 7, 1, "https://en.wikipedia.org/wiki/Computer_programming", "static/programming-ico.png", "Programming/Scripting Languages", "Computer programming is the process of performing a particular computation (or more generally, accomplishing a specific computing result), usually by designing and building an executable computer program. Programming involves tasks such as analysis, generating algorithms, profiling algorithms' accuracy and resource consumption, and the implementation of algorithms (usually in a chosen programming language, commonly referred to as coding).", ""],
							["Scripting", 7, 1, "https://www.geeksforgeeks.org/introduction-to-scripting-languages/", "static/scripting-ico.png", "Programming/Scripting Languages", "A scripting language or script language is a programming language for a runtime system that automates the execution of tasks that would otherwise be performed individually by a human operator. Scripting languages are usually interpreted at runtime rather than compiled.", ""],
							["C", 7, 1, "https://en.wikipedia.org/wiki/C_(programming_language)", "static/c-ico.png", "Programming/Scripting Languages", "C is a general-purpose computer programming language. It was created in the 1970s by Dennis Ritchie, and remains very widely used and influential. By design, C's features cleanly reflect the capabilities of the targeted CPUs. It has found lasting use in operating systems, device drivers, protocol stacks, though decreasingly for application software, and is common in computer architectures that range from the largest supercomputers to the smallest microcontrollers and embedded systems.", ""],
							["C#", 9, 1, "https://en.wikipedia.org/wiki/C_Sharp_(programming_language)",
							"static/csharp-ico.png", "Programming/Scripting Languages", "C# is a general-purpose, multi-paradigm programming language. C# encompasses static typing, strong typing, lexically scoped, imperative, declarative, functional, generic, object-oriented (class-based), and component-oriented programming disciplines]", ""],
							["Java", 8, 1, "https://en.wikipedia.org/wiki/Java_%28programming_language%29",
							"static/java-ico.png", "Programming/Scripting Languages", "Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile.", ""],
							["Python", 9, 1, "https://en.wikipedia.org/wiki/Python_(programming_language)", "static/python-ico.png", "Programming/Scripting Languages", "Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming.", ""],
							["SQL", 7, 1, "https://en.wikipedia.org/wiki/SQL", "static/sql-ico.png", "Programming/Scripting Languages", "SQL is a domain-specific language used in programming and designed for managing data held in a relational database management system (RDBMS), or for stream processing in a relational data stream management system (RDSMS). It is particularly useful in handling structured data, i.e. data incorporating relations among entities and variables.", ""],
							["Powershell", 8, 1, "https://en.wikipedia.org/wiki/PowerShell", "static/powershell-ico.png", "Programming/Scripting Languages", "PowerShell is a task automation and configuration management program from Microsoft, consisting of a command-line shell and the associated scripting language. Initially a Windows component only, known as Windows PowerShell, it was made open-source and cross-platform on 18 August 2016 with the introduction of PowerShell Core. The former is built on the .NET Framework, the latter on .NET Core.", ""],
							["C++", 5, 1, "https://en.wikipedia.org/wiki/C++", "static/cpp-ico.png", "Programming/Scripting Languages", "C++ is a general-purpose programming language created by Bjarne Stroustrup as an extension of the C programming language, or 'C with Classes'. The language has expanded significantly over time, and modern C++ has object-oriented, generic, and functional features in addition to facilities for low-level memory manipulation.", ""],
							["JavaScript", 6, 1, "https://en.wikipedia.org/wiki/JavaScript", "static/js-ico.png", "Programming/Scripting Languages", "JavaScript, often abbreviated JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS. Over 97% of websites use JavaScript on the client side for web page behavior, often incorporating third-party libraries. All major web browsers have a dedicated JavaScript engine to execute the code on users' devices.", ""],
							["PHP", 5, 1, "https://en.wikipedia.org/wiki/PHP", "static/php-ico.png", "Programming/Scripting Languages", "PHP is a server scripting language, and a powerful tool for making dynamic and interactive Web pages. PHP is a widely-used, free, and efficient alternative to competitors such as Microsoft's ASP.", ""],
							["HTML", 6, 1, "https://en.wikipedia.org/wiki/HTML", "static/html-ico.png", "Programming/Scripting Languages", "The HyperText Markup Language or HTML is the standard markup language for documents designed to be displayed in a web browser. It can be assisted by technologies such as Cascading Style Sheets (CSS) and scripting languages such as JavaScript.", ""],
							["CSS", 6, 1, "https://en.wikipedia.org/wiki/CSS", "static/css-ico.png", "Programming/Scripting Languages", "Cascading Style Sheets (CSS) is a style sheet language used for describing the presentation of a document written in a markup language such as HTML. CSS is a cornerstone technology of the World Wide Web, alongside HTML and JavaScript.", ""],
							["LaTeX", 5, 1, "https://en.wikipedia.org/wiki/LaTeX", "static/latex-ico.png", "Programming/Scripting Languages", "LaTeX is a high-quality typesetting system; it includes features designed for the production of technical and scientific documentation. LaTeX is the de facto standard for the communication and publication of scientific documents.", ""],
							["Ruby", 3, 1, "https://en.wikipedia.org/wiki/Ruby_(programming_language)", "static/ruby-ico.png", "Programming/Scripting Languages", "Ruby is an interpreted, high-level, general-purpose programming language which supports multiple programming paradigms. It was designed with an emphasis on programming productivity and simplicity. In Ruby, everything is an object, including primitive data types. It was developed in the mid-1990s by Yukihiro 'Matz' Matsumoto in Japan.", ""],
							["Go", 4, 1, "https://en.wikipedia.org/wiki/Go_(programming_language)", "static/go-ico.png", "Programming/Scripting Languages", "Go is a statically typed, compiled programming language designed at Google[10] by Robert Griesemer, Rob Pike, and Ken Thompson. It is syntactically similar to C, but with memory safety, garbage collection, structural typing, and CSP-style concurrency. It is often referred to as Golang because of its former domain name, golang.org, but its proper name is Go.", ""],
							["Rust", 2, 1, "https://en.wikipedia.org/wiki/Rust_(programming_language)#:~:text=Rust%20is%20a%20multi-paradigm%20programming%20language%20designed%20for,without%20garbage%20collection%2C%20and%20reference%20counting%20is%20optional.", "static/rust-ico.png", "Programming/Scripting Languages", "Rust is a multi-paradigm, general-purpose programming language. It is designed for performance and safety, especially safe concurrency. Rust is known for enforcing memory safety — that is, that all references point to valid memory — without requiring the use of a garbage collector or reference counting like other memory-safe languages. Memory safety is enforced by a borrow checker, which tracks object lifetime and variable scope as references are passed throughout the program during compilation.[16] Rust can be used for systems programming with mechanisms for low-level memory management,[18] but also offers high-level features such as functional programming.", ""],
							["Bash", 4, 1, "https://en.wikipedia.org/wiki/Bash_(Unix_shell)", "static/bash-ico.png", "Programming/Scripting Languages", "Bash is a Unix shell and command language written by Brian Fox for the GNU Project as a free software replacement for the Bourne shell. First released in 1989, it has been used as the default login shell for most Linux distributions. Bash is a command processor that typically runs in a text window where the user types commands that cause actions. Bash can also read and execute commands from a file, called a shell script.", ""],
							[".NET", 6, 1, "https://en.wikipedia.org/wiki/.NET_Framework", "static/dotnet-ico.png", "Frameworks", ".NET is a free, open-source development platform for building many kinds of apps, such as: Web apps, web APIs, and microservices, Serverless functions in the cloud, Cloud native apps, Mobile apps, Desktop apps, Windows WPF, Windows Forms, Universal Windows Platform (UWP), Games, Internet of Things (IoT), Machine learning, Console apps, and Windows services", ""],
							["Bootstrap", 5, 1, "https://en.wikipedia.org/wiki/Bootstrap_(front-end_framework)", "static/bootstrap-ico.png", "Frameworks", "Bootstrap is a free and open-source CSS framework directed at responsive, mobile-first front-end web development. It contains HTML, CSS and (optionally) JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.", ""],
							["Selenium", 7, 1, "https://en.wikipedia.org/wiki/Selenium_(software)", "static/selenium-ico.png", "Frameworks", "Selenium is an open source umbrella project for a range of tools and libraries aimed at supporting browser automation. It provides a playback tool for authoring functional tests without the need to learn a test scripting language (Selenium IDE). It also provides a test domain-specific language (Selenese) to write tests in a number of popular programming languages, including JavaScript (Node.js), C#, Groovy, Java, Perl, PHP, Python, Ruby and Scala. The tests can then run against most modern web browsers.", ""],
							["Ruby on Rails", 2, 1, "https://en.wikipedia.org/wiki/Ruby_on_Rails", "static/rails-ico.png", "Frameworks", "Rails is a web application development framework written in the Ruby programming language. It is designed to make programming web applications easier by making assumptions about what every developer needs to get started. It allows you to write less code while accomplishing more than many other languages and frameworks.", ""],
							["Django", 3, 1, "https://en.wikipedia.org/wiki/Django_(web_framework)", "static/django-ico.png", "Frameworks", "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.", ""],
							["JQuery", 3, 1, "https://en.wikipedia.org/wiki/JQuery", "static/jquery-ico.png", "Frameworks", "jQuery is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers.", ""],
							["Unity Engine", 5, 1, "https://en.wikipedia.org/wiki/Unity_(game_engine)", "static/unity-ico.png", "Frameworks", "Unity is a cross-platform game engine developed by Unity Technologies, first announced and released in June 2005 at Apple Worldwide Developers Conference as a Mac OS X game engine. The engine has since been gradually extended to support a variety of desktop, mobile, console and virtual reality platforms. It is particularly popular for iOS and Android mobile game development and is considered easy to use for beginner developers and is popular for indie game development.", ""],
							["Keras", 2, 1, "https://en.wikipedia.org/wiki/Keras", "static/keras-ico.png", "Frameworks", "Keras is a deep learning API written in Python, running on top of the machine learning platform TensorFlow. It was developed with a focus on enabling fast experimentation. Being able to go from idea to result as fast as possible is key to doing good research.", ""],
							["Data Structures", 7, 1, "https://en.wikipedia.org/wiki/Data_structure", "static/datastructures-ico.png", "Theoretical Knowledge", "A data structure is a particular way of organizing data in a computer so that it can be used effectively. The idea is to reduce the space and time complexities of different tasks.", ""],
							["Algorithm Analysis", 7, 1, "https://en.wikipedia.org/wiki/Analysis_of_algorithms", "static/aa-ico.png", "Theoretical Knowledge", "Algorithm analysis is an important part of computational complexity theory, which provides theoretical estimation for the required resources of an algorithm to solve a specific computational problem. Most algorithms are designed to work with inputs of arbitrary length. Analysis of algorithms is the determination of the amount of time and space resources required to execute it.", ""],
							["PDQ Deploy", 6, 1, "https://www.pdq.com/pdq-deploy/", "static/pdq-ico.png", "Software Solutions", "As your business grows, so do the demands on your IT team. Automating repetitive processes is one of the simplest and most cost-effective ways to maximize efficiency without hiring new personnel. PDQ Deploy serves as an automated patch manager and software deployment tool so you can update more computers in less time.", ""],
							["Notepad++", 7, 1, "https://en.wikipedia.org/wiki/Notepad++", "static/nppp-ico.png", "Software Solutions", "Notepad++ is a text and source code editor for use with Microsoft Windows. It supports tabbed editing, which allows working with multiple open files in a single window. The product's name comes from the C postfix increment operator.", ""],
							["Atom", 8, 1, "https://en.wikipedia.org/wiki/Atom_(text_editor)", "static/atom-ico.png", "Software Solutions", "Atom is a free and open-source text and source code editor for macOS, Linux, and Microsoft Windows with support for plug-ins written in JavaScript, and embedded Git Control. Developed by GitHub, Atom is a desktop application built using web technologies. Most of the extending packages have free software licenses and are community-built and maintained. Atom is based on Electron (formerly known as Atom Shell), a framework that enables cross-platform desktop applications using Chromium and Node.js. Atom was initially written in CoffeeScript and Less, but much of it has been converted to JavaScript.", ""],
							["Microsoft Visual Studio", 7, 1, "https://en.wikipedia.org/wiki/Microsoft_Visual_Studio", "static/visualstudio-ico.png", "Software Solutions", "Microsoft Visual Studio is an integrated development environment (IDE) from Microsoft. It is used to develop computer programs, as well as websites, web apps, web services and mobile apps. Visual Studio uses Microsoft software development platforms such as Windows API, Windows Forms, Windows Presentation Foundation, Windows Store and Microsoft Silverlight. It can produce both native code and managed code.", ""],
							["Eclipse", 7, 1, "https://en.wikipedia.org/wiki/Eclipse_(software)", "static/eclipse-ico.png", "Software Solutions", "Eclipse is an integrated development environment (IDE) used in computer programming. It contains a base workspace and an extensible plug-in system for customizing the environment. It is the second-most-popular IDE for Java development, and, until 2016, was the most popular. Eclipse is written mostly in Java and its primary use is for developing Java applications, but it may also be used to develop applications in other programming languages via plug-ins, including Ada, ABAP, C, C++, C#, Clojure, COBOL, D, Erlang, Fortran, Groovy, Haskell, JavaScript, Julia, Lasso, Lua, NATURAL, Perl, PHP, Prolog, Python, R, Ruby (including Ruby on Rails framework), Rust, Scala, and Scheme", ""],
							["Putty", 7, 1, "https://en.wikipedia.org/wiki/PuTTY", "static/putty-ico.png", "Software Solutions", "PuTTY is a free and open-source terminal emulator, serial console and network file transfer application. It supports several network protocols, including SCP, SSH, Telnet, rlogin, and raw socket connection. It can also connect to a serial port.", ""],
							["Git", 7, 1, "https://en.wikipedia.org/wiki/Git", "static/git-ico.png", "Software Solutions", "Git is software for tracking changes in any set of files, usually used for coordinating work among programmers collaboratively developing source code during software development. Its goals include speed, data integrity, and support for distributed, non-linear workflows (thousands of parallel branches running on different systems).", ""],
							["TEXstudio", 5, 1, "https://en.wikipedia.org/wiki/TeXstudio", "static/texstudio-ico.png", "Software Solutions", "TeXstudio is a cross-platform open-source LaTeX editor. Its features include an interactive spelling checker, code folding, and syntax highlighting. It does not provide LaTeX itself – the user must choose a TeX distribution and install it first.", ""],
							["Oracle VirtualBox", 5, 1, "https://en.wikipedia.org/wiki/VirtualBox", "static/oraclevirtualbox-ico.png", "Software Solutions", "Oracle VM VirtualBox is a type-2 hypervisor for x86 virtualization developed by Oracle Corporation. VirtualBox was originally created by Innotek GmbH, which was acquired by Sun Microsystems in 2008, which was in turn acquired by Oracle in 2010. VirtualBox may be installed on Microsoft Windows, macOS, Linux, Solaris and OpenSolaris. There are also ports to FreeBSD and Genode. It supports the creation and management of guest virtual machines running Windows, Linux, BSD, OS/2, Solaris, Haiku, and OSx86, as well as limited virtualization of macOS guests on Apple hardware.", ""],
							["VMware Workstation", 5, 1, "https://en.wikipedia.org/wiki/VMware_Workstation", "static/vmwareworkstation-ico.png", "Software Solutions", "VMware Workstation Pro (known as VMware Workstation until release of VMware Workstation 12 in 2015) is a hosted hypervisor that runs on x64 versions of Windows and Linux operating systems (an x86-32 version of earlier releases was available); it enables users to set up virtual machines (VMs) on a single physical machine and use them simultaneously along with the host machine. Each virtual machine can execute its own operating system, including versions of Microsoft Windows, Linux, BSD, and MS-DOS.", ""],
							["Microsoft Power BI", 4, 1, "https://en.wikipedia.org/wiki/Microsoft_Power_BI", "static/powerbi-ico.png", "Software Solutions", "Power BI is an interactive data visualization software product developed by Microsoft with a primary focus on business intelligence. It is part of the Microsoft Power Platform. Power BI is a collection of software services, apps, and connectors that work together to turn unrelated sources of data into coherent, visually immersive, and interactive insights. Data may be input by reading directly from a database, webpage, or structured files such as spreadsheets, CSV, XML, and JSON.", ""],
							["Microsoft Office", 8, 1, "https://en.wikipedia.org/wiki/Microsoft_Office", "static/mso-ico.png", "Software Solutions", "Microsoft Office, or simply Office, is a family of client software, server software, and services developed by Microsoft. Initially a marketing term for an office suite (bundled set of productivity applications), the first version of Office contained Microsoft Word, Microsoft Excel, and Microsoft PowerPoint. Over the years, Office applications have grown substantially closer with shared features such as a common spell checker, Object Linking and Embedding data integration and Visual Basic for Applications scripting language. Microsoft also positions Office as a development platform for line-of-business software under the Office Business Applications brand.", ""],
							["Microsoft Power Apps", 3, 1, "https://docs.microsoft.com/en-us/power-apps/powerapps-overview", "static/mspa-ico.png", "Power Apps is a suite of apps, services, and connectors, as well as a data platform, that provides a rapid development environment to build custom apps for your business needs. Using Power Apps, you can quickly build custom business apps that connect to your data stored either in the underlying data platform (Microsoft Dataverse) or in various online and on-premises data sources (such as SharePoint, Microsoft 365, Dynamics 365, SQL Server, and so on).", ""],
							["ServiceNow", 6, 1, "https://en.wikipedia.org/wiki/ServiceNow", "static/sn-ico.png", "Software Solutions", "ServiceNow is a platform-as-a-service provider, providing technical management support, such as IT service management, to the IT operations of large corporations, including providing help desk functionality. The company's core business revolves around management of 'incident, problem, and change' IT operational events.", ""],
							["Spiceworks", 3, 1, "https://en.wikipedia.org/wiki/Spiceworks", "static/spiceworks-ico.png", "Software Solutions", "Spiceworks is an online community where users can collaborate and seek advice from one another, and also engage in a marketplace to purchase IT-related services and products. The network is estimated to be used by more than six million IT professionals and 3,000 technology vendors. The company's free proprietary software is written in Ruby on Rails, and runs exclusively on Microsoft Windows. The software discovers IP-addressable devices and includes help desk functionality and an integrated knowledge base.", ""], 
							["Microsoft Azure", 4, 1, "https://en.wikipedia.org/wiki/Microsoft_Azure", "static/azure-ico.png", "Software Solutions", "Microsoft Azure, often referred to as Azure, is a cloud computing service operated by Microsoft for application management via Microsoft-managed data centers. It provides software as a service (SaaS), platform as a service (PaaS) and infrastructure as a service (IaaS) and supports many different programming languages, tools, and frameworks, including both Microsoft-specific and third-party software and systems.", ""],
							["Google Cloud", 2, 1, "https://en.wikipedia.org/wiki/Google_Cloud_Platform", "static/gc-ico.png", "Software Solutions", "Google Cloud Platform (GCP), offered by Google, is a suite of cloud computing services that runs on the same infrastructure that Google uses internally for its end-user products, such as Google Search, Gmail, Google Drive, and YouTube. Alongside a set of management tools, it provides a series of modular cloud services including computing, data storage, data analytics and machine learning. Google Cloud Platform provides infrastructure as a service, platform as a service, and serverless computing environments.", ""],
							["AWS", 2, 1, "https://en.wikipedia.org/wiki/Amazon_Web_Services", "static/aws-ico.png", "Software Solutions", "Amazon Web Services, Inc. (AWS) is a subsidiary of Amazon that provides on-demand cloud computing platforms and APIs to individuals, companies, and governments, on a metered pay-as-you-go basis. These cloud computing web services provide distributed computing processing capacity and software tools via AWS server farms.", ""]
						]
						
		for i in range(len(skilldata)):
			id = self.genid()
			skilldata[i].append(id)
			data = (id, skilldata[i][0], skilldata[i][1], skilldata[i][2], skilldata[i][3], self.imgtobin(skilldata[i][4]), skilldata[i][5], cb, skilldata[i][6], skilldata[i][7])
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
							[ skilldata[7][8], skilldata[1][8], skilldata[28][8], skilldata[39][8], skilldata[42][8] ],
							[ skilldata[7][8], skilldata[39][8], skilldata[41][8] ],
							[ skilldata[5][8], skilldata[7][8], skilldata[20][8], skilldata[39][8], skilldata[41][8] ],
							[ skilldata[5][8], skilldata[7][8], skilldata[20][8], skilldata[38][8], skilldata[39][8]  ]
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
				if (len(skill_ids[i]) > 0):
					data = (id, title, present, date_start, desc_short, desc_long, skill_id, org_ids[i], cb)
					self.execute_d(query_b, data)
				else:
					data = (id, title, present, date_start, desc_short, desc_long, "", org_ids[i], cb)
					self.execute_d(query_b, data)
			else:
				if (len(skill_ids[i]) > 0):
					data = (id, title, present, date_start, date_end, desc_short, desc_long, skill_id, org_ids[i], cb)
					self.execute_d(query_a, data)
				else:
					data = (id, title, present, date_start, date_end, desc_short, desc_long, "", org_ids[i], cb)
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
		skill_ids = [
						[ skilldata[39][8]],
						[ skilldata[0][8], skilldata[4][8], skilldata[8][8], skilldata[10][8], skilldata[11][8], skilldata[12][8], skilldata[29][8], skilldata[32][8], skilldata[39][8] ],
						[skilldata[0][8], skilldata[1][8], skilldata[2][8], skilldata[4][8], skilldata[6][8], skilldata[9][8], skilldata[11][8], skilldata[12][8], skilldata[13][8], skilldata[14][8], skilldata[17][8], skilldata[19][8], skilldata[21][8], skilldata[23][8], skilldata[26][8], skilldata[27][8], skilldata[29][8], skilldata[30][8], skilldata[32][8], skilldata[33][8], skilldata[34][8], skilldata[35][8], skilldata[36][8], skilldata[37][8], skilldata[39][8] ],
					]
					
		for i in range(len(edu_data)):
			s = ""
			for j in range(len(skill_ids[i])):
				if j != len(skill_ids[i]) - 1:
					s += skill_ids[i][j] + ','
				else:
					s += skill_ids[i][j]
			id = self.genid()
			data = (id, edu_data[i][0], edu_data[i][1], edu_data[i][2], s, edu_data[i][4], edu_data[i][5], edu_data[i][6], edu_data[i][7])
			self.execute_d(query, data)
		
		
	def imgtobin(self, path):
		file = open(path, 'rb').read()
		file = base64.b64encode(file)
		return file
		
		