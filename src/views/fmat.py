import datetime

def addresslines (address):
	a = address.split(',')
	c = ""
	for b in a:
		c += b + '<br>'
	return c
	
def datereformat (date):
	d = datetime.datetime.strptime(date, '%Y-%m-%d')
	return d.strftime('%b %Y')
	
def telelink (phone):
		return "tel:+1" + phone

def teleformat (phone):
	return '(' + phone[:3] + ') ' + phone[3:6] + '-' + phone[6:10]
	
def sanitize (str):
	if '<br>' in str:
		print("BREAK")
	s = str.replace('"', "\'")
	s = s.replace("'", "\\'")
	s = s.replace('\n', '<br>')
	return s