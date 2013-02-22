# this script will open a file with email addresses in it, then extract 
# those address and write them to a new file
# some of the script is from http://snipplr.com/view/23938/

import os
import re
import httplib
from urlparse import urlparse
from prettytable import PrettyTable

# vars for filenames
filename = 'about_us.html'
newfilename = 'emaillist-rev.txt'

# function to check whether url exists
def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    #print url + str(resp.status) + str(resp.reason)
    return resp.status < 400

# read file
if os.path.exists(filename):
	data = open(filename,'r')
	bulkemails = data.read()
else:
	print "File not found."
	raise SystemExit

# regex = whoEver@wHerever.xxx
r = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
results = r.findall(bulkemails)    

emails = ""  
table = PrettyTable(["id", "/~{id}       " , "/members/{id}", "Homepage"]) 
table.align["id"] = "l"
table.align["domain"] = "l"  
table.align["Homepage"] = "l"
table.hrule = 2
table.vrule = 1

for x in results:
	email = str(x)
	splited = email.split('@')
	nick = splited[0]
	domian = splited[1]
	url1 = "http://delicias.dia.fi.upm.es/~" + nick + "/"
        url2 = "http://delicias.dia.fi.upm.es/members/" + nick + "/"
	url3 = "http://delicias.dia.fi.upm.es/members/" + nick[:2].upper() + nick[2:] + "/"
	url4 = ""
	page = ""
	pattern1 = ""
	pattern2 = ""
	check1 = checkUrl(url1)
	if check1:
		page = url1
		pattern1 = "Found"
        check2 = checkUrl(url2)
	if check2:
		page = url2
		pattern2 = "Found"
        check3 = checkUrl(url3)
	if check3:
		page = url3
		pattern2 = "Found"
	check2 = check2 or check3
	for line in open("oeg_net_page.txt"):
		if nick in line:
	   		url4 = line[:-1]
        if page:
		urls = str(page) + "\n" + str(url4) 
	else:
		urls = str(url4)
        table.add_row([nick, pattern1, pattern2, urls ])
	
print table.get_string(sortby="id")

print "[1] - http://delicias.dia.fi.upm.es/~{id}"
print "[2] - http://delicias.dia.fi.upm.es/members/{id}" 
