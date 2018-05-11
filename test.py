import interactions

userData = [
    {'pid': 1, 'name': 'Kate Kenneally', 'email': 'kkenneal@wellesley.edu', 
    'password': 'secret', 'permissions': 'admin', 'year': 2018, 
    'bnumber': 'B20746088', 'userType': 'student'},
    {'pid': 2, 'name': 'Angelina Li', 'email': 'ali6@wellesley.edu',
    'password': 'secret', 'permissions': 'admin', 'year': 2019,
    'bnumber': "B20809164", 'userType': 'student'},
    {'pid': 3, 'name': 'Priscilla Lee', 'email': 'plee3@wellesley.edu',
    'password': 'secret', 'permissions': 'admin', 'year': 2018,
    'bnumber': None, 'userType': 'student'},
    {'pid': 4, 'name': 'Scott Anderson', 'email': 'sanderso@wellesley.edu',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'},
    {'pid': 5, 'name': 'Lyn Turbak', 'email': 'fturbak@wellesley.edu',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'},
    {'pid': 6, 'name': 'Andy Schultz', 'email': 'andrew.c.schultz@gmail.com',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'},
    {'pid': 7, 'name': 'Ellen Hildreth', 'email': 'ehildret@wellesley.edu',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'},
    {'pid': 8, 'name': 'Ann Trenk', 'email': 'atrenk@wellesley.edu',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'},
    {'pid': 9, 'name': 'Fred Shultz', 'email': 'fshultz@wellesley.edu',
    'password': 'secret', 'permissions': 'prof', 'year': None,
    'bnumber': None, 'userType': 'professor'}
]

courseData = [
    {'cid': 1, 'dept': 'CS', 'courseNum': '304', 'section': '01',
    'year': 2018, 'semester': 'Spring'},
    {'cid': 2, 'dept': 'CS', 'courseNum': '251', 'section': '01', 
    'year': 2018, 'semester': 'Spring'},
    {'cid': 3, 'dept': 'MATH', 'courseNum': '305', 'section': '01',
    'year': 2018, 'semester': 'Spring'},
    {'cid': 4, 'dept': 'MATH', 'courseNum': '206', 'section': '02',
    'year': 2018, 'semester': 'Spring'},
    {'cid': 5, 'dept': 'CS', 'courseNum': '307', 'section': '01',
    'year': 2017, 'semester': 'Fall'},
    {'cid': 6, 'dept': 'MATH', 'courseNum': '326', 'section': '01',
    'year': 2017, 'semester': 'Fall'},
    {'cid': 7, 'dept': 'CS', 'courseNum': '111', 'section': '02',
    'year': 2018, 'semester': 'Spring'},
    {'cid': 8, 'dept': 'CS', 'courseNum': '111', 'section': '03',
    'year': 2018, 'semester': 'Spring'},
    {"cid": 9, "dept": "CS", "courseNum": "230", "section": "01",
    "year": 2018, "semester": "Spring"},
    {'cid': 10, 'dept': 'CS', 'courseNum': '111', 'section': '03',
    'year': 2017, 'semester': 'Spring'}
]

studentCourseData = [
    {"pid": 1, "cid": 1},
    {"pid": 1, "cid": 2},
    {"pid": 1, "cid": 3},
    {"pid": 1, "cid": 5},
    {"pid": 1, "cid": 6},
    {"pid": 2, "cid": 1},
    {"pid": 2, "cid": 4},
    {"pid": 3, "cid": 1},
    {"pid": 3, "cid": 3}
]

profCourseData = [
    {"pid": 4, "cid": 1},
    {"pid": 4, "cid": 8},
    {"pid": 5, "cid": 2},
    {"pid": 5, "cid": 7},
    {"pid": 6, "cid": 3},
    {"pid": 9, "cid": 4},
    {"pid": 7, "cid": 5},
    {"pid": 8, "cid": 6}
]

tutorCourseData = [
    {"pid": 1, "cid": 7},
    {"pid": 1, "cid": 8},
    {"pid": 2, "cid": 7},
    {"pid": 2, "cid": 8},
    {"pid": 3, "cid": 9}
]

sessionData = [
    {'pid': 1, 'cid': 1, 'isTutor': 'n', 'beginTime': None, 'endTime': None, 'sessionType': 'help room'},
    {'pid': 1, 'cid': 8, 'isTutor': 'y', 'beginTime': None, 'endTime': None, 'sessionType': 'help room'},
    {'pid': 2, 'cid': 7, 'isTutor': 'y', 'beginTime': None, 'endTime': None, 'sessionType': 'individual tutoring'},
    {'pid': 1, 'cid': 2, 'isTutor': 'n', 'beginTime': None, 'endTime': None, 'sessionType': 'individual tutoring'}
]

def checkResults(results, insertLabel):
    if not all(results):
        print("Error when:", insertLabel)
    else:
        print("Finished:", insertLabel)

def insertData():
    results = []
    for d in userData:
        r = interactions.insertUser(d)
        results.append(r)
    checkResults(results, "inserting users")
    
    results = []
    for d in courseData:
        r = interactions.insertCourse(d)
        results.append(r)
    checkResults(results, "inserting courses")

    results = []
    for d in studentCourseData:
        r = interactions.insertStudentCourse(**d)
        results.append(r)
    checkResults(results, "inserting student courses")

    results = []
    for d in profCourseData:
        r = interactions.insertProfCourse(**d)
        results.append(r)
    checkResults(results, "inserting prof courses")

    results = []
    for d in sessionData:
        r = interactions.insertSession(d)
        results.append(r)
    checkResults(results, "inserting sessions")
