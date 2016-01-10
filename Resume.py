import urllib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
def getContextLink(initurl):
	html=urllib.urlopen(initurl).read()
	context=re.findall(r"""<div><a href="(/article/ParttimeJob/\d*)">(.+?)</a>""",html)
	Linklist=[]
	for con in context:
		Linklist.append(["http://m.byr.cn"+con[0],con[1]])
	return Linklist
def getContextEmail(context):
	sumer=0
	companyEmail=[]
	for con in context:	
		html=urllib.urlopen(con[0]).read()
		tmphtml=re.findall(r"""<div class="sp">(.+?)<span href="/a""",html)
		company=con[1]
		email=re.findall(r"""[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?""",tmphtml[0])
 		if email!=[]:
			companyEmail.append([company,email[0]])
	return companyEmail
class Email:
	def __init__(self,email_from,email_to,password):
		self.msg=MIMEMultipart()
		self.msg['from'] = email_from
		self.msg['to'] = email_to
		self.password=password
	def addFile(self,filename):
		att1 = MIMEText(open('filename', 'rb').read(), 'base64', 'gb2312')
		att1["Content-Type"] = 'application/octet-stream'
		att1["Content-Disposition"] = 'attachment; filename="drcom.rar"'
		self.msg.attach(att1)
	def addContext(self,context):
		txt = MIMEText(context,'plain','gb2312')
		self.msg.attach(txt)
	def addSubject(self,subject):
		self.msg['subject'] = subject
	def sendEmail(self):
		try:
		    server = smtplib.SMTP()
		    server.connect('smtp.qq.com')
		    server.starttls()
		    print 'connected'
		    server.login(self.msg['from'],self.password)
		    server.sendmail(self.msg['from'], self.msg['to'],self.msg.as_string())
		    server.quit()
		    print 'send success'
		except Exception, e:
		    print str(e)
def main():
	email_from=raw_input("Please input your emailAddress: ")
	password=raw_input("Please input your emailPassword: ")	
	emailContext=raw_input("Please input your emailContext: ")
	emailSubject=raw_input("Please input your emailSubject: ")
	emailSet=set()
	pagelong=30
	print "Alalyse Starting......"
	for i in range(pagelong):
		i=i+1
		progress=40
		percent=i/(pagelong*1.0)
		probar='['
		for i in range(40):
			if i<int(progress*percent):
				probar+="="
			elif i==int(progress*percent):
				probar+=">"
			else:
				probar+=" "
		probar+="]"
		print (probar+"Percemt of %d has finished!"%(percent*100)+"\t")
		initurl="http://m.byr.cn/board/ParttimeJob?p=%d"%i
		context=getContextLink(initurl)
		companyEmail=getContextEmail(context)
	   	count=0
		for con in companyEmail:
			count+=1
			emailSet.add(con[1])
	for email_to emailSet:
		try:
			emailSet.add(con[1])
			email=Email(email_from,email_to,password)
			email.addContext(emailContext)
			email.addSubject(emailSubject)
			email.addFile(filename)
			email.sendEmail()
		except:
			print "password or emailaddress is wrong!"
main()
