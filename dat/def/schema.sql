CREATE TABLE Accounts
	(id TEXT PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, salt TEXT NOT NULL,
	name TEXT NOT NULL, group_id TEXT NOT NULL);
CREATE TABLE Groups
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, auth_key TEXT NOT NULL UNIQUE);
CREATE TABLE Addresses
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, uri TEXT NOT NULL UNIQUE, created_by TEXT NOT NULL, 
	FOREIGN KEY(created_by) REFERENCES Accounts(id));
CREATE TABLE Orgs
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, address TEXT NOT NULL, phone TEXT NOT NULL, desc TEXT NOT NULL,
    created_by TEXT NOT NULL, website TEXT UNIQUE, logo BLOB, image_head BLOB, 
	FOREIGN KEY(address) REFERENCES Addresses(id), 
	FOREIGN KEY(created_by) REFERENCES Accounts(id));
CREATE TABLE Jobs
	(id TEXT PRIMARY KEY, title TEXT NOT NULL, present INTEGER NOT NULL, date_start TEXT NOT NULL, 
	date_stop TEXT, desc_short TEXT NOT NULL, desc_long TEXT NOT NULL, skill_ids TEXT, 
	org_id TEXT NOT NULL, created_by TEXT NOT NULL,
	FOREIGN KEY(org_id) REFERENCES Orgs(id), 
	FOREIGN KEY(created_by) REFERENCES Accounts(id));
CREATE TABLE Skills
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, exposure INTEGER NOT NULL, 
	soft_or_hard INTEGER NOT NULL, reference TEXT, icon BLOB, category TEXT NOT NULL, desc TEXT NOT NULL, desc_long TEXT NOT NULL,
	created_by TEXT NOT NULL, 
	FOREIGN KEY(created_by) REFERENCES Accounts(id));
CREATE TABLE Contact
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, 
	address TEXT NOT NULL, phone1 TEXT NOT NULL UNIQUE, phone2 TEXT NOT NULL UNIQUE, 
	email TEXT NOT NULL UNIQUE, created_by TEXT NOT NULL, objective TEXT NOT NULL,
	FOREIGN KEY(created_by) REFERENCES Accounts(id), 
	FOREIGN KEY(address) REFERENCES Addresses(id));
CREATE TABLE Certifications
	(id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, obtained TEXT NOT NULL, 
	skill_ids TEXT, logo blob, created_by TEXT NOT NULL, 
	FOREIGN KEY(created_by) REFERENCES Accounts(id));
CREATE TABLE Education
	(id TEXT PRIMARY KEY, org TEXT NOT NULL, degree TEXT NOT NULL UNIQUE, gpa REAL NOT NULL, 
	skill_ids TEXT, created_by TEXT NOT NULL, date_end TEXT NOT NULL, 
	desc_short TEXT NOT NULL UNIQUE, desc_long TEXT NOT NULL UNIQUE,
	FOREIGN KEY(created_by) REFERENCES Accounts(id),
	FOREIGN KEY(org) REFERENCES Orgs(id));