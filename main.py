import mechanize
import getpass
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from calendar import monthrange
import datetime
from welcome import welcome
import urllib


global html ,br , header, stu_id
br = mechanize.Browser()
now = datetime.datetime.now()
stu_id= ""

def overall_attendanc():
	for link in br.links():
	    if link.text== 'Attendance':
		break
	##click on the link
	req = br.click_link(link)
	##open the link 
	br.open(req)
	##get the html response
	html = br.response().read()
	soup = BeautifulSoup(html,"lxml")
	
	
	##get the average of the attendance 
	overall_attendance= PrettyTable(['Subject Name', 'Total', 'Present', 'Attendance %'])
	attendance_table = soup.find("table", { "class" : "table_data" })
	for row in attendance_table.findAll("tr", {"class":['odd','even']}):
		data = row.findAll('td')
		overall_attendance.add_row([data[1].get_text(), data[3].get_text(),data[4].get_text(),data[5].get_text()])
	##get the overall of the attendance
	final = soup.find('tr', attrs={'class': 'report_footer disp-curr-sem'})
	final_data = final.findAll('td')
	overall_attendance.add_row(['--------','-----','-----','-----'])
	overall_attendance.add_row([final_data[0].get_text(),final_data[1].get_text(),final_data[2].get_text(),final_data[3].get_text()])
	
	header = final_data[0].get_text()
	return overall_attendance


def month_attend(month,year,stu_id):
	data = urllib.urlencode({u'studentradio':'2',u'months':month,u'yearData':year})
	br.open("http://bgkv.edusec.org/student/attendence/studentAttendenceReport/"+stu_id, data)
        sub_list = list()

	##get the html response
	html = br.response().read()
	soup = BeautifulSoup(html,"lxml")
	
	##get the average of the attendance 
	overall_attendance= PrettyTable(['Sno','Subject Name', 'Total', 'Present', 'Attendance %'])
	attendance_table = soup.find("table", { "class" : "table_data" })
	for row in attendance_table.findAll("tr", {"class":['odd','even']}):
		data = row.findAll('td')
		overall_attendance.add_row([data[0].get_text(),data[1].get_text(), data[4].get_text(),data[5].get_text(),data[6].get_text()])
	
		
	##get the overall of the attendance
	final = soup.find('tr', attrs={'class': 'report_footer'})
	footer_head = final.findAll('td')
	final_data = final.findAll('th')
	overall_attendance.add_row(['--','--------','-----','-----','-----'])
	overall_attendance.add_row(['--',footer_head[0].get_text(),final_data[0].get_text(),final_data[1].get_text(),final_data[2].get_text()])
	
	return overall_attendance
	

def yearlst(stu_id):
	#parse the url using br.geturl() and then pass the value to open it using br.open
	br.open("http://bgkv.edusec.org/student/attendence/studentAttendenceReport/"+stu_id)
	html = br.response().read()
	soup = BeautifulSoup(html,"lxml")	
	year_list = list()
	row = soup.find("select",attrs={'name':'yearData'})
	for row1 in row.findAll("option"):
		year_list.append(row1['value'])
	del year_list[0]
	year_list = map(int, year_list)
	return year_list

def subject_link(month,year,stu_id):
	data = urllib.urlencode({u'studentradio':'2',u'months':month,u'yearData':year})
	#parse the url using br.geturl() and then pass the value to open it using br.open
	br.open("http://bgkv.edusec.org/student/attendence/studentAttendenceReport/"+stu_id, data)
        sub_list = list()
	sub_link_list = list()
	sub_final = dict()
	##get the html response
	html = br.response().read()
	soup = BeautifulSoup(html,"lxml")	
	
	for a in soup.findAll('a', { "class" : "link" }):
	    	sub_link_list.append(a['href'])
		sub_list.append(a.text)

	sub_list = map(str, sub_list)
	sub_final = zip(sub_list,sub_link_list)		
	return sub_final

	

	



def month_wise(stu_id):
	try:
		month = int(raw_input("Enter the Month : "))
		year = int(raw_input("Enter the Year : "))

		if year not in yearlst(stu_id):
			print "Sorry try again"
			month_wise()
		elif month > now.month and year == now.year:
			print type(month)
			print type(now.month)
			print "Sorry Wrong Month Select"
			month_wise()
		else:
			month_atnd = month_attend(month,year,stu_id)	
			print month_atnd
			print "======================"
			opt = raw_input("Do you want to see Monthly Sheet attendance (y/n)")
			if opt == 'y' or opt == 'Y':
				print subject_wise(month_atnd,month,year,stu_id)				
			else:
				return 						
	except ValueError, Argument:
		return "Try again invalid" 

	
	
def subject_wise(month_atnd,month,year,stu_id):
	sub_list = subject_link(month,year,stu_id)	
	month_range = monthrange(year,month)
	try:
		month_attendance= PrettyTable()
		day = list(range(1,month_range[1]+1))
		month_attendance.add_column('Day',day)
		
		for sub in sub_list: 					
			url = "http://bgkv.edusec.org"+sub[1]			
			br.set_handle_robots(False)
			br.open(url)	
			html = br.response().read()
			soup = BeautifulSoup(html,"lxml")

			month = list()
			notes = list()
	

	                ##get the average of the attendance 
			attendance_table = soup.find("table", { "class" : "table_data" })
			attendance = attendance_table.find("tr", { "class" : "odd" })
			note = attendance.findAll('td')
			for n,i in enumerate(note):
				note[n] = note[n].get_text()
			month_attendance.add_column("".join(e[0] for e in sub[0].split()),note)
				
		return month_attendance		
			
	except ValueError, Argument:
		return "Try again invalid" 


	
def daily(date,month,year,stu_id):	
	sub_list = subject_link(month,year,stu_id)	
	try:
		daily_attendance= PrettyTable(['Subject', 'P/A'])
		for sub in sub_list:
			url = "http://bgkv.edusec.org"+sub[1]			
			br.set_handle_robots(False)
			br.open(url)	
			html = br.response().read()
			soup = BeautifulSoup(html,"lxml")				
			month = list()
			notes = list()
			##get the average of the attendance 
			
			attendance_table = soup.find("table", { "class" : "table_data" })
			days = attendance_table.find("tr", { "class" : "table_header" })
			attendance = attendance_table.find("tr", { "class" : "odd" })
			day = days.findAll('th')
			note = attendance.findAll('td')
			del day[0]			
			for a,b in zip(day,note):	
				if int(a.get_text()) == date:					
					daily_attendance.add_row([sub[0],b.get_text()])
					break	

		return daily_attendance

	except ValueError, Argument:
		return "Try again invalid" 
		

def menu(stu_id):
	ans=True
	while ans:
		print("""
  	 	 1. Overall Attendance
  	 	 2. Month Wise Attendance
  		 3. Daily Attendance
  		 4. Exit/Quit
  	 	 """) 	  	 
  		ans=raw_input("What would you like to do? ")
  	 	if ans=="1":
		    print "================================"
  		    print overall_attendanc()
  		elif ans=="2":
 		    print month_wise(stu_id)
 		elif ans=="3":
		    date=raw_input("Enter Date ")
		    print "Attendance for "+ date
		
  		    print daily(int(date),now.month,now.year,stu_id)
  		elif ans=="4":
   		   print("\n Goodbye") 
   		   ans = None
  		else:
   	 	   print("\n Not Valid Choice Try again")




		

def login(enroll,passwd):   	
	response = br.open("http://bgkv.edusec.org/site/login/")
	br.form = list(br.forms())[0]  # use when form is unnamed
	br.form['LoginForm[username]'] = enroll+'@bapugkv.ac.in'
	br.form['LoginForm[password]'] = passwd
	response = br.submit()	
	if response.geturl() == "http://bgkv.edusec.org/site/login/" :
		print("login fail")
	else:
		html = br.response().read()
		soup = BeautifulSoup(html,"lxml")
		name = soup.find("li", { "class" : "welcome" })
		stu_id = soup.find("a", { "title" : "My Attendance" })['href'].split('/')[-1]
		print name.get_text()
		menu(stu_id)
welcome()

enroll_no = '130750116023' #raw_input("Please enter your enrollment no : ")
passwd = 'nick@2211' #getpass.getpass("Please enter your password : ")
login(enroll_no,passwd)
