from flask import Flask, request, jsonify
import re
import smtplib
import ssl
import os
from dotenv import load_dotenv

#load in local credentials
load_dotenv('.env')

app = Flask(__name__)


# endpoint for submiting json form. only recives POSTs
# returns 'success' and code 200 if submission is correct
# returns error and error messgage if submission is broken in anyway
@app.route('/submit/', methods=['POST'])
def submit():
	try:
		if request.is_json:
			is_valid_submission(request.get_json())
		else:
			raise ValueError("got something other than json")
	except ValueError as e:
		return 'invalid submission, {err}'.format(err = e), 400

	try:
		send_customer_info(request.get_json())
		send_thanks_email(request.get_json()['email'])
		return 'success', 200
	except:
		return 'sending out emails failed', 500

# return w/o error if received json follows example.json format
	# 4 keys named 'name', 'email', 'scm' , and 'teamSize'
	# name, email, and scm are strings, teamSize is int
	# scm is one of Github, Gitlab, BitBucket, TFS, Other 
	# email is a correctly formated email address
def is_valid_submission(req):
	# ensure keys are valid length
	if len(list(req.keys())) != 4 or list(req.keys()) != ['name', 'email', 'scm', 'teamSize']:
		raise ValueError("malformed json, keys mismatch")
	
	#ensure name, email, and scm are strings and teamSize is non-negative int
	elif type(req['name']) is not str or type(req['email']) is not str or type(req['scm']) is not str or type(req['teamSize']) is not int or req['teamSize'] < 0:
		raise ValueError("invalid input types")
	
	#ensure scm is a valid option
	elif req['scm'] not in ("Github", "Gitlab"," BitBucket", "TFS", "Other"):
		raise ValueError("not a valid scm option")
	
	#ensure email is valid by matching regex
	elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", req['email']):
		raise ValueError("email not formatted correctly")
	else:
		return

# create a connection to mail server with info specified in .env. Return the connection
def init_mail_server():
	try:
		context = ssl.create_default_context()
		server = smtplib.SMTP_SSL(os.environ.get("MAIL_SERVER"), os.environ.get("MAIL_PORT"), context = context)
		server.login(os.environ.get("EMAIL"), os.environ.get("PASS"))
		return server
	except:
		raise 

# send information that was received to DEST_EMAIL in .env
def send_customer_info(req):
	message = """Subject:Customer Info- codebox api


	request submitted by {name} with email {email}, who uses {scm} and works with {num} other people.

	""".format(name=req['name'],email=req['email'],scm=req['scm'],num=req['teamSize'])
	server = init_mail_server()
	server.sendmail(os.environ.get("EMAIL"), os.environ.get("DEST_EMAIL"), message)
	server.quit()

# send thank you email to who what ever email address was posted 
def send_thanks_email(dest):
	message = """Subject: Thanks from codebox!

	Thank you for submitting your information to codebox!
	"""
	server = init_mail_server()
	server.sendmail(os.environ.get("EMAIL"), dest, message)
	server.quit()


