from prof_module.api_wrappers import *
from prof_module.models import *
from django.contrib.auth.models import User
import os

# To run this script
# 1) python manage.py shell
# 2) execfile("<path>/functions.py")

""" 
Instructions to use this script
1) First, use the createFaceSetForCourses to create a new faceset for a course.
2) Use the UploadTrainingData providing the path to the folder that stores the training data 
to upload images and get the corresponding face tokens.
3) Use the addFacesToFaceset function to add all faces to the facesets of the corresponding courses. 
If a faceset doesn't exist, the api calls will be unsuccessful and you will get "Somethign went wrong" even 
though you have a good internet connection.

"""

# To create facesets for courses that do not already have a faceset.
def createFaceSetForCourses():
	courses = Course.objects.all()
	course_list = []
	for item in courses:
		course_list.append(item.course_id)
	facesets = Facesets.objects.all()
	outer_ids = []
	for item in facesets:
		outer_ids.append(item.outer_id)
	to_create = list(set(course_list) - set(outer_ids))
	print (to_create)
	for item in to_create:
		createFaceSet(item)
	print ("Created required facesets")

# Assumption is that the images will be stored in the TrainingData folder and the files will be named <roll_no.>.jpg. path is the path to the training data folder.
def UploadTrainingData(path):
	#print (path)
	images = os.listdir(path)
	#print (images)
	count = 0
	for image in images:
		#print (image)
		if "jpg" in image: 	# Only these 2 formats are allowed
			user = image.lower().replace(".jpg","") + "@smail.iitm.ac.in"
		elif "png" in image:
			user = image.lower().replace(".png","") + "@smail.iitm.ac.in"
			try:
				user_obj = User.objects.get(username=user)
				try:
					RollNumberToken.objects.get(roll_number=user_obj)	# If the face token is already there in the table, we don't do anything
					print ("Token for "+user+" already present")
				except Exception as e:
					#print(e)
					print ("Getting token for "+user)
					token = detectFace(path+"/"+image)
					r = RollNumberToken(roll_number=user_obj,face_token=token)
					r.save()
					print ("Token saved " + str(count))
					count += 1 
			except Exception as e:
				#print(e)
				print ("No user found for "+image)
				pass

# Add all face tokens for the roll numbers present in a course to the facesets of every course present in the Course tables. 
def addFacesToFaceSet():
	courses = Course.objects.all()
	for course in courses:
		students = course.taken_by.all()
		#print students
		count = 0
		for student in students:
			try:
				row = RollNumberToken.objects.get(roll_number=student)
				addFaceSet(course.course_id,[row.face_token])
				print ("Face added to faceset "+str(count))
				count += 1
			except Exception as e:
				print(e)
				print ("Student's face token not found")
				pass

# Add student whose email is 'stud_email' to the course with course ID 'courseId' which is taught by the prof whose email is 'prof_email'
# assuming that student, course and prof are present in the database. 
def studAddCourse(stud_email, courseId, prof_email):
	s = User.objects.get(email=stud_email)
	p = User.objects.get(email=prof_email)
	c = Course.objects.get(course_id=courseId, taught_by=p)
	try:
		c.taken_by.add(s)
		c.save()
	except:
		pass

# Create course which taken by the prof
# assuming that prof is present in the database. 
def profCreateCourse(prof_email, courseId, courseTitle):
	p = User.objects.get(email=prof_email)
	c = Course.objects.create(course_id=courseId,course_name=courseTitle,taught_by=p)

# Adds all CS14 batch students to a course. 
def addCS14studentsToCourse():
	for i in range(1,63):
		if i < 10:
			studAddCourse("cs14b00"+str(i)+"@smail.iitm.ac.in","CS1400","prof@iitm.ac.in")
		else:
			studAddCourse("cs14b0"+str(i)+"@smail.iitm.ac.in","CS1400","prof@iitm.ac.in")

# Creates a single user. 
def createUser(stud_name,stud_email):
	try:
		u = User.objects.create(first_name=stud_name,email=stud_email,username=stud_email,is_staff="0")
		u.set_password("123567")
		u.save()
	except:
		pass

# Creates user accounts for all CS14 batch students. 			
def createCS14Users():
	for i in range(1,63):
		if i < 10:
			createUser("CS14B00"+str(i),"cs14b00"+str(i)+"@smail.iitm.ac.in")
		else:
			createUser("CS14B0"+str(i),"cs14b0"+str(i)+"@smail.iitm.ac.in")
			
# Sample usage

#createFaceSet("CSF213")
#createFaceSet("CS3420")
# createFaceSetForCourses()
UploadTrainingData("./TrainingData")
#addFacesToFaceSet()

#createCS14Users()
#profCreateCourse('prof@iitm.ac.in','CS1400','CS new course')
#addCS14studentsToCourse()
# studAddCourse('stud1@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
# studAddCourse('stud2@smail.iitm.ac.in','CS1400', 'prof@iitm.ac.in')
