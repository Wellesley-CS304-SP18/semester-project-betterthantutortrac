import interactions

user_data = [
{'pid': 1, 'name': 'Kate Kenneally', 'email': 'kkenneal@wellesley.edu', 
'password': 'secret', 'permissions': 'admin', 'year': 2018, 
'bnumber': 'B20746088', 'usertype': 'student'},
{'pid': 2, 'name': 'Angelina Li', 'email': 'ali6@wellesley.edu',
'password': 'secret', 'permissions': 'admin', 'year': 2019,
'bnumber': None, 'usertype': 'student'},
{'pid': 3, 'name': 'Priscilla Lee', 'email': 'plee3@wellesley.edu',
'password': 'secret', 'permissions': 'admin', 'year': 2018,
'bnumber': None, 'usertype': 'student'},
{'pid': 4, 'name': 'Scott Anderson', 'email': 'sanderso@wellesley.edu',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'},
{'pid': 5, 'name': 'Lyn Turbak', 'email': 'fturbak@wellesley.edu',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'},
{'pid': 6, 'name': 'Andy Schultz', 'email': 'andrew.c.schultz@gmail.com',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'},
{'pid': 7, 'name': 'Ellen Hildreth', 'email': 'ehildret@wellesley.edu',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'},
{'pid': 8, 'name': 'Ann Trenk', 'email': 'atrenk@wellesley.edu',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'},
{'pid': 9, 'name': 'Fred Shultz', 'email': 'fshultz@wellesley.edu',
'password': 'secret', 'permissions': 'prof', 'year': None,
'bnumber': None, 'usertype': 'professor'}
]

course_data = [
{'cid': 1, 'dept': 'CS', 'coursenum': '304', 'section': '01',
'year': 2018, 'semester': 'Spring'},
{'cid': 2, 'dept': 'CS', 'coursenum': '251', 'section': '01', 
'year': 2018, 'semester': 'Spring'},
{'cid': 3, 'dept': 'MATH', 'coursenum': '305', 'section': '01',
'year': 2018, 'semester': 'Spring'},
{'cid': 4, 'dept': 'MATH', 'coursenum': '206', 'section': '02',
'year': 2018, 'semester': 'Spring'},
{'cid': 5, 'dept': 'CS', 'coursenum': '307', 'section': '01',
'year': 2017, 'semester': 'Fall'},
{'cid': 6, 'dept': 'MATH', 'coursenum': '326', 'section': '01',
'year': 2017, 'semester': 'Fall'},
{'cid': 7, 'dept': 'CS', 'coursenum': '111', 'section': '02',
'year': 2018, 'semester': 'Spring'},
{'cid': 8, 'dept': 'CS', 'coursenum': '111', 'section': '03',
'year': 2018, 'semester': 'Spring'}
]

for d in user_data:
    print interactions.insertUser(d)

for d in course_data:
    print interactions.insertCourse(d)

interactions.insertStudentCourse(1, 1)
interactions.insertStudentCourse(1, 2)
interactions.insertStudentCourse(1, 3)
interactions.insertStudentCourse(1, 5)
interactions.insertStudentCourse(1, 6)
interactions.insertStudentCourse(2, 1)
interactions.insertStudentCourse(2, 4)
interactions.insertStudentCourse(3, 1)
interactions.insertStudentCourse(3, 3)

interactions.insertProfCourse(4, 1)
interactions.insertProfCourse(4, 8)
interactions.insertProfCourse(5, 2)
interactions.insertProfCourse(5, 7)
interactions.insertProfCourse(6, 3)
interactions.insertProfCourse(9, 4)
interactions.insertProfCourse(7, 5)
interactions.insertProfCourse(8, 6)

session_data = [
{'userId': 1, 'courseId': 1, 'isTutor': 'n',
'beginTime': None, 'endTime': None,
'sessiontype': 'help room'},
{'userId': 1, 'courseId': 8, 'isTutor': 'y',
'beginTime': None, 'endTime': None,
'sessiontype': 'help room'},
{'userId': 2, 'courseId': 7, 'isTutor': 'y',
'beginTime': None, 'endTime': None,
'sessiontype': 'individual tutoring'},
{'userId': 1, 'courseId': 2, 'isTutor': 'n',
'beginTime': None, 'endTime': None,
'sessiontype': 'individual tutoring'}
]

for d in session_data:
    print interactions.insertSession(d)
