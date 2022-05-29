# -*- coding: utf-8 -*-
import urllib3
import urllib
import time
import binascii
import urllib.request
from urllib import request
from bs4 import BeautifulSoup
import pip._vendor.requests 
import json
import urllib.parse
from multipart_sender import MultiPartForm
import requests

api_key = "d0zjqANDSL-90rHPBNu9wKTGpB222r1v"	# API Key to use Face++ services
api_secret = "dDOIEtsi8FjXUhUHPO70E6MYND02K6mb"	# API secret to use Face++ services
from prof_module.models import *
import ast

""" List of URLs for the API calls	"""
faceset_create_url = "https://api-us.faceplusplus.com/facepp/v3/faceset/create"
faceset_add_url = "https://api-us.faceplusplus.com/facepp/v3/faceset/addface"
detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
search_url = "https://api-us.faceplusplus.com/facepp/v3/search"

""" End of URLs for API calls 	"""

"""
Usage
#createFaceSet("CS3410")
#detectFace("../images/images/CS14B0XX.jpg")
#addFaceSet("CS3410", ["a7b1d6c7baa05ef7043e0d11cd32da12", "e34875caf029ebb55b2d1351c25453e3", "2019b7bba5e794ac94073aac96adebed", "cf4c11367a775f3f9c5fb9515f190e2c"])
#searchFace("CS3410",image_path="../images/images2/CS14B0YY.jpg") or searchFace("CS3410",face_token="2019b7bba5e794ac94073aac96adebed")
"""

# This function is to be called when a new course is created by the admin. The faceset will later contain the face tokens of all the students in the course.
def createFaceSet(course_number):
	global api_key
	global api_secret
	global faceset_create_url
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s--\n' % boundary)
	
	try:
		response = make_request(faceset_create_url,data,boundary)
		#response = ast.literal_eval(response)
		response = json.loads(response)
		if "faceset_token" in response:
			c = Facesets(faceset_token=response["faceset_token"],outer_id=response["outer_id"])
			c.save()
			print ("Created faceset for course " + response["outer_id"])
		else:
			print ("Could not create faceset for course "+course_number)
	except Exception as e:
		print(e)
		raise Exception("Something went wrong")
	

# This function is to be called during upload training data, after getting the face tokens. We can add atmost 5 face tokens to a faceset at a time. The input argument 'face_tokens' should be a list.
# Cupping for some reason, try with postman
def addFaceSet(course_number,face_tokens):
	global api_key
	global api_secret
	global faceset_add_url
	if len(face_tokens) > 5:
		raise Exception("At most 5 faces can be added at a time")
	face_token_string = ",".join(face_tokens)
	#print face_token_string
	
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'face_tokens')
	data.append(face_token_string)
	data.append('--%s--\n' % boundary)
	
	try:
		response = make_request(faceset_add_url,data,boundary)
		#response = ast.literal_eval(response)
		response = json.loads(response)
		print (response)
	except:
		print ("Something went wrong")
	
# This function is to be called during take attendance. We can pass either of "image_path" or "face_token". We get the facetoken in the faceSet that matches this face. So, we need to store roll number - face token mapping.
def searchFace(course_number,image_path=None,face_token=None):
	global api_key
	global api_secret
	global search_url
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'outer_id')
	data.append(course_number)
	data.append('--%s' % boundary)
	if image_path:
		data.append('Content-Disposition: form-data; name="%s"; filename="face.jpg"' % 'image_file')
		data.append('Content-Type: %s\n' % 'application/octet-stream')
		fp = open(image_path,'rb')
		if fp:
			data.append(fp.read())
			fp.close()
		else:
			raise Exception("Image not found")
	elif face_token:		
		data.append('Content-Disposition: form-data; name="%s"\n' % 'face_token')
		data.append(face_token)
	else:
		raise Exception("Enter a face_token or image_path")
	data.append('--%s--\n' % boundary)
	
	#print "Making request"
	try:
		response = make_request(search_url,data,boundary)
		#response = ast.literal_eval(response)
		response = json.loads(response)
		#print response
		return response
	except:
		print ("Something went wrong1")

# This function is to be called to get a face token, prior to any operation that needs a face token(such as add face to faceset.	
def detectFace(image_path):
	#print("detect called")
	global api_key
	global api_secret
	global detect_url
	#print(image_path)
	"""
	myfile = open(image_path, 'rb')
	form = MultiPartForm()
	form.add_field('api_key', api_key)
	form.add_field('api_secret', api_secret)
	form.add_file('image_file', 'image.jpg', fileHandle=myfile)
	form.make_result()
	#url=detect_url
	"""
 
	"""
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"; filename="image.png"' % 'image_file')
	data.append('Content-Type: %s\n' % 'application/octet-stream')
	fp = open(image_path,'rb')
	if fp:
		#print(fp.decode('utf-8'))
		data.append(fp.read())
		fp.close()
	else:
		raise Exception("Image not found")
	data.append('--%s\n' % boundary)
	"""
	files = {
    'api_key': (None, 'd0zjqANDSL-90rHPBNu9wKTGpB222r1v'),
    'api_secret': (None, 'dDOIEtsi8FjXUhUHPO70E6MYND02K6mb'),
    'image_file': open(image_path, 'rb'),
    'return_landmark': 1,
	}

	response = requests.post('https://api-us.faceplusplus.com/facepp/v3/detect', files=files)
	try:
		#response = make_request(detect_url,data,boundary)
		#response = ast.literal_eval(response)
		#response = json.loads(response)
		#print response
		#print type(response)
		if "faces" in response:	# Assuming only 1 face in the training image
			token = response["faces"][0]["face_token"]
			#print token
			return token
		else:
			"No faces"
	except:
		print ("Something went wrong")
		
def detectMultipleFaces(image_path):
	global api_key
	global api_secret
	global detect_url
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_key')
	data.append(api_key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\n' % 'api_secret')
	data.append(api_secret)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"; filename="image.png"' % 'image_file')
	data.append('Content-Type: %s\n' % 'application/octet-stream')
	fp = open(image_path,'rb')
	if fp:
		data.append(fp.read())
		fp.close()
	else:
		raise Exception("Image not found")
	data.append('--%s\n' % boundary)
	
	try:
		response = make_request(detect_url,data,boundary)
		#print response
		#response = ast.literal_eval(response)
		response = json.loads(response)
		#print response
		#print type(response)
		if "faces" in response:	# Assuming only 1 face in the training image
			faces = response["faces"]
			return faces
		else:
			"No faces"
	except:
		print ("Something went wrong")
	
		
# Response part is currently here, we need to return values appropriately.		
def make_request(url,data,boundary):
	# From this part onward it is the same.
	print(data)
	#http_body = b''
	http_body = []
	for e in data:
		if isinstance(e,bytes):
			http_body.append(e.decode('utf-8'))
		else: http_body.append(e)
	print (http_body)
	enc_data = json.dumps(http_body).encode()
	#http_body='\n'.join(e.decode('utf-8') if isinstance(e, bytes) else e for e in data)
	#http_body = urllib.parse.urlencode(http_body)
	#http_body = http_body.encode('utf-8')
	#if isinstance(, unicode):
	#	myStr = encObject.encode('utf-8') 
	#print http_body
	print ("Building request")
	#build http request
	#http = urllib3.PoolManager()
	print("trying")
	#new
	#req=http.request(url, headers={'Content-Type':'multipart/form-data; boundary=%s' % boundary}, body=http_body) 
	#old
	#req=request.Request(url, headers={'Content-Type':'multipart/form-data; boundary=%s' % boundary}, body=http_body) 
	heads= {'Content-Type':'multipart/form-data; boundary=%s' % boundary}
	#resp=pip._vendor.requests.post(url, data=http_body, headers=hea)
	print("trying")
	#print(req.text)
	#req=urllib.request.Request(url)
	#req.add_header('Content-type', form.get_content_type())
	#req.add_header('Content-length', len(form.form_data))
	#req.add_data(form.form_data)
	req=urllib.request.Request(url, headers=heads, data=enc_data)
	#print(req.data)
	#old
	#req=urllib2.Request(url)
	#header
	#req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
	#req.add_data(http_body)
	#print("trying")
	#print(req.content)
	
	try:  
		#post data to server
		print("entered try block")
		resp = urllib.request.urlopen(req, timeout=120)
  		#old
		#resp = urllib2.urlopen(req, timeout=120)
		print("trying")
		#print (resp)
		#get response
		qrcont=resp.read()
		print(qrcont)
		print("trying")
		#new
  		#return qrcont.decode("utf-8")
		#old
		return qrcont

	except Exception as e:
		print(e)
		raise Exception("Something went wrong")

