"""
filename: testData.py
author: Kate Kenneally, Angelina Li, Priscilla Lee
last modified: 05/13/2018
description: module to define and insert some test data into our database.
"""

import interactions as i
import program as p

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
    'bnumber': None, 'userType': 'professor'},
    {'pid': 10, 'name': 'Test1 Student1', 'email': 'tstudent1@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2019,
     'bnumber': 'B11111111', 'userType': 'student'},
    {'pid': 11, 'name': 'Test2 Student2', 'email': 'tstudent2@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2019,
     'bnumber': 'B22222222', 'userType': 'student'},
    {'pid': 12, 'name': 'Test3 Student3', 'email': 'tstudent3@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2020,
     'bnumber': 'B33333333', 'userType': 'student'},
    {'pid': 13, 'name': 'Test4 Student4', 'email': 'tstudent4@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2020,
     'bnumber': 'B44444444', 'userType': 'student'},
    {'pid': 14, 'name': 'Test5 Student5', 'email': 'tstudent5@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2021,
     'bnumber': 'B55555555', 'userType': 'student'},
    {'pid': 15, 'name': 'Test6 Student6', 'email': 'tstudent6@wellesley.edu',
     'password': 'secret', 'permissions': 'student', 'year': 2021,
     'bnumber': 'B66666666', 'userType': 'student'}
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
    {"pid": 1, "cid": 8},
    {"pid": 2, "cid": 1},
    {"pid": 2, "cid": 4},
    {"pid": 3, "cid": 1},
    {"pid": 3, "cid": 3},
    {"pid": 10, "cid": 1},
    {"pid": 10, "cid": 2},
    {"pid": 10, "cid": 3},
    {"pid": 10, "cid": 4},
    {"pid": 11, "cid": 3},
    {"pid": 11, "cid": 4},
    {"pid": 11, "cid": 7},
    {"pid": 11, "cid": 9},
    {"pid": 12, "cid": 3},
    {"pid": 12, "cid": 4},
    {"pid": 12, "cid": 8},
    {"pid": 12, "cid": 9},
    {"pid": 13, "cid": 1},
    {"pid": 13, "cid": 2},
    {"pid": 13, "cid": 3},
    {"pid": 14, "cid": 2},
    {"pid": 14, "cid": 9},
    {"pid": 14, "cid": 10},
    {"pid": 15, "cid": 1},
    {"pid": 15, "cid": 9},
    {"pid": 15, "cid": 10}
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
    {"pid": 2, "cid": 4},
    {"pid": 2, "cid": 7},
    {"pid": 2, "cid": 8},
    {"pid": 3, "cid": 9},
    {"pid": 4, "cid": 1},
    {"pid": 4, "cid": 7},
    {"pid": 4, "cid": 8},
    {"pid": 4, "cid": 10}
]

sessionData = [
    {'pid': 1, 'tid': 2, 'cid': 1, 'isTutor': 0, 'beginTime': None, 'endTime': None, 'sessionType': 'Help Room'},
    {'pid': 1, 'cid': 8, 'isTutor': 1, 'beginTime': None, 'endTime': None, 'sessionType': 'Help Room'},
    {'pid': 2, 'cid': 7, 'isTutor': 1, 'beginTime': None, 'endTime': None, 'sessionType': 'PLTC Assigned Tutoring'},
    {'pid': 1, 'tid': 3, 'cid': 2, 'isTutor': 0, 'beginTime': None, 'endTime': None, 'sessionType': 'PLTC Assigned Tutoring'},
    {'pid': 2, 'tid': None, 'cid': 1, 'isTutor': 0, 'beginTime': None, 'endTime': None, 'sessionType': 'Help Room'}
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
    c = i.getConn()
    insertData(c, userData, i.insertUser, "inserting users")
    insertData(c, courseData, i.insertCourse, "inserting courses")
    insertData(c, tutorCourseData, i.insertTutorCourse,
        "inserting tutor courses")
    insertData(c, studentCourseData, i.insertStudentCourse,
        "inserting student courses")
    insertData(c, profCourseData, i.insertProfCourse,
        "inserting prof courses")
    insertData(c, sessionData, i.insertSession, "inserting sessions")

if __name__ == "__main__":
    insertAllData()
