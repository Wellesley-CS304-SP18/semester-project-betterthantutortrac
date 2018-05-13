from interactions import *

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
    {'pid': 1, 'tid': 2, 'cid': 1, 'isTutor': 0, 'beginTime': None, 'endTime': None, 'sessionType': 'Help Room'},
    {'pid': 1, 'cid': 8, 'isTutor': 1, 'beginTime': None, 'endTime': None, 'sessionType': 'Help Room'},
    {'pid': 2, 'cid': 7, 'isTutor': 1, 'beginTime': None, 'endTime': None, 'sessionType': 'PLTC Assigned Tutoring'},
    {'pid': 1, 'tid': 3, 'cid': 2, 'isTutor': 0, 'beginTime': None, 'endTime': None, 'sessionType': 'PLTC Assigned Tutoring'}
]

def insertData(conn, dataList, insertFunc, insertLabel):
    results = []
    for d in dataList:
        r = insertFunc(conn, d)
        results.append(r)

    if not all(results):
        print "Error while:", insertLabel
    else:
        print "Finished:", insertLabel

def insertAllData():
    c = getConn()
    insertData(c, userData, insertUser, "inserting users")
    insertData(c, courseData, insertCourse, "inserting courses")
    insertData(c, tutorCourseData, insertTutorCourse,
        "inserting tutor courses")
    insertData(c, studentCourseData, insertStudentCourse, 
        "inserting student courses")
    insertData(c, profCourseData, insertProfCourse, 
        "inserting prof courses")
    insertData(c, sessionData, insertSession, "inserting sessions")

if __name__ == "__main__":
    insertAllData()
