# face-recog-app

This web application is an Attendance system using Face Recognition. This was created as a solution to the Microsoft Engage 2022 Face Recognition Challenge.


Features:
- Professors and Student Login
- Sign up feature
- Option for Student to view courses, daywise attendance report, course wise attendance report, attendance percentage, raise queries regarding attendance.
- Professors can automatically take attendance by uploading an image of the class onto the attendance page on their dashboard.
- Option for Professors to view courses, view attendance history on a particular date, view attendance history of current date, view and update queries raised by the students.


Tech Stack:
- Backend: Python Django Framework
- Frontend: HTML, CSS, JS
- API: FacePlusPlus Face Recognition (https://www.faceplusplus.com/)


Steps to Run:
1. Install Python

2. Install Django
  This project needs django to run. To install, please run : sudo pip install -r requirements.txt

3. Enter the following commands:
  cd trialproject
  python manage.py runserver

If you are running the app for the first time, you may need to run:   
python manage.py makemigrations auth_module stud_module prof_module   
python manage.py migrate  

Go to the following website on your browser:   
http://127.0.0.1:8000/  


You can use the following credentials to login to the Professor's Module:  
  username: professor@gmail.com   
  password: prof123@   

You can use the following credentials to login to the Student's Module:   
  username: f20191404@hyderabad.bits-pilani.ac.in   
  password: 123567   

You can use the following credentials to login to the Django Admin Dashboard:   
  website: http://127.0.0.1:8000/admin   
  username: bhavyatibrewala   
  password: bhavyadjango   


Unfortunately, due to the API malfunctioning, the Take Attendance module is currently not functional. However, all the other modules are fully functional. I am working on changing the API to make the project complete. This will take another week.
