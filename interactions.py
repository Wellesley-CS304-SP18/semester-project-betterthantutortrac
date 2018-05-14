#!/user/local/bin/python2.7
"""
filename: interactions.py
authors: Kate Kenneally, Angelina Li, Priscilla Lee
last modified: 05/13/2018
description: python to SQL interactions
"""

import datetime
import dbconn2
import MySQLdb
import sys

database = 'kkenneal_db' # we'll use Kate's database

### database connection functions ###

def getDsn(db):
    dsn = dbconn2.read_cnf()
    dsn['db'] = db
    return dsn

def getConn(dsn=None):
    if dsn == None:
        dsn = getDsn(database)
    return dbconn2.connect(dsn)

### helper functions ###

def getSqlDate(dt):
    """
    Given a datetime.datetime object, this function will return a string
    formatted date in a format understandable by MySQL database.
    """
    sqlFormat = "%Y-%m-%d %H:%M:%S"
    return dt.strftime(sqlFormat)

def getCourseName(courseData):
    return "{dept} {courseNum}-{section}".format(**courseData)

def findAllSessionTypes():
    """
    This function returns a list of all possible valid session types.
    """
    sessionTypes = [
        "ASC (Academic Success Coordinator)",
        "Help Room",
        "PLTC Assigned Tutoring",
        "Public Speaking Tutoring",
        "SI (Supplemental Instruction)"
    ]
    return sessionTypes

### database interaction FIND functions ###

def getSqlQuery(conn, query, params=[], fetchall=True):
    """
    This function executes a given SELECT SQL query and
    returns either all results or one result.
    """
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query, params)
    if fetchall:
        return curs.fetchall()
    return curs.fetchone()

def getUserName(conn, pid):
    """
    Given a user's (unique) pid, this function returns the user's name.
    """
    query = "SELECT name from users where pid=%s"
    params = [pid]
    return getSqlQuery(conn, query, params) # False?

def findUsersByName(conn, name):
    """
    Given a name, this function returns data for all matching users.
    """
    query = "SELECT * FROM users WHERE name LIKE %s"
    params = ["%" + name + "%"]
    return getSqlQuery(conn, query, params)

def findUsersByEmail(conn, email):
    """
    Given a user's (unique) email, this function returns the user's data.
    """
    query = "SELECT * FROM users WHERE email=%s"
    params = [email]
    return getSqlQuery(conn, query, params) # False?

def findUsersByUsername(conn, username):
    """
    Given a user's (unique) username, this function returns the user's data.
    """
    email = username + "@wellesley.edu" # a wrapper around the last fn
    return findUsersByEmail(conn, email)

def findCourseById(conn, cid):
    """
    Given a course's (unique) cid, this function returns the course's data.
    """
    query = "SELECT * FROM courses WHERE cid=%s"
    params = [cid]
    return getSqlQuery(conn, query, params) # False?

def findCoursesByName(conn, dept, courseNum):
    """
    Given a course's name (department + course number), this function returns
    data for all matching courses.
    """
    query = "SELECT * FROM courses WHERE dept LIKE %s AND courseNum LIKE %s"
    params = ["%" + dept + "%", "%" + courseNum + "%"]
    return getSqlQuery(conn, query, params)

def findCoursesByStudent(conn, pid):
    """
    Given a student's (unique) pid, this function returns data on all courses
    taken by the student.
    """
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findDeptCoursesByStudent(conn, pid, dept):
    """
    Given a student's (unique) pid and a department, this function returns
    data on all courses taken by the student in the specified department.
    """
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s AND dept=%s"""
    params = [pid, dept]
    return getSqlQuery(conn, query, params)

def findCoursesByProf(conn, pid):
    """
    Given a professor's (unique) pid, this function returns data on all courses
    taught by the professor.
    """
    query = """SELECT * FROM courses INNER JOIN coursesTaught USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findCoursesByTutor(conn, pid):
    """
    Given a tutor's (unique) pid, this function returns data on all courses
    tutored by the tutor.
    """
    query = """SELECT * FROM courses INNER JOIN tutors USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findAllSessions(conn):
    """
    This function returns data on all tutoring sessions.
    """
    # want student name, course name, and session type. fix up later.
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)"""
    return getSqlQuery(conn, query)

def findSessionByTimeTutor(conn, beginTime, tid):
    """
    Given a time and a tutor's (unique) tid, this function returns
    data on all tutoring sessions held by the tutor at the specified time.
    """
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE beginTime=%s AND pid=%s AND isTutor=1"""
    params = [beginTime, tid]
    return getSqlQuery(conn, query, params)

def findMatchingSessions(conn, searchTerm):
    """
    Given a search term, this function returns data on all tutoring sessions
    that match the search term.
    """
    query = """SELECT * FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE name LIKE %s OR courseNum LIKE %s OR dept LIKE %s"""
    params = ["%" + searchTerm + "%" for _ in range(len(3))]
    return getSqlQuery(conn, query, params)

def findSessionsByStudent(conn, pid):
    """
    Given a student's (unique) pid, this function returns data on all
    tutoring sessions the student has attended.
    """
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findSessionsByCourse(conn, cid):
    """
    Given a course's (unique) cid, this function returns data on all
    tutoring sessions for the course.
    """
    query = """SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE cid=%s"""
    params = [cid]
    return getSqlQuery(conn, query, params)

### database interaction INSERT functions ###

def insertData(conn, query, params):
    """
    This function executes a given SQL INSERT query and
    returns True if the query is successful and False otherwise.
    """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(query, params)
        return True
    except Exception as e:
        print "Exception:", e
        return False

def insertUser(conn, data):
    """
    Given the appropriate data, this function inserts a user into
    the users table in our database.
    """
    paramOrder = ["pid", "name", "email", "password", "permissions", "year",
        "bnumber", "userType"]
    query = "INSERT INTO users ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)

def insertCourse(conn, data):
    """
    Given the appropriate data, this function inserts a course into
    the courses table in our database.
    """
    paramOrder = ["cid", "dept", "courseNum", "section", "year", "semester"]
    query = "INSERT INTO courses ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)

def insertStudentCourse(conn, data):
    """
    Given the appropriate data, this function inserts a student/course
    relationship into the coursesTaken table in our database.
    """
    query = "INSERT INTO coursesTaken (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertProfCourse(conn, data):
    """
    Given the appropriate data, this function inserts a professor/course
    relationship into the coursesTaught table in our database.
    """
    query = "INSERT INTO coursesTaught (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertTutorCourse(conn, data):
    """
    Given the appropriate data, this function inserts a tutor/course
    relationship into the tutors table in our database.
    """
    query = "INSERT INTO tutors (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertSession(conn, data):
    """
    Given the appropriate data, this function inserts a tutoring session
    into the sessions table in our database.
    """
    paramOrder = ["pid", "cid", "isTutor", "sessionType"]
    optionalParams = ["tid", "beginTime", "endTime"]
    for p in optionalParams:
        if p in data:
            paramOrder.append(p)
    query = "INSERT INTO sessions ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)

### database interaction UPDATE functions ###

def updateData(conn, query, params):
    """
    This function executes a given SQL UPDATE query and
    returns True if the query is successful and False otherwise.
    """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(query, params)
        return True
    except Exception as e:
        print "Exception:", e
        return False

def updateSessionEndTime(conn, sid, endTime):
    """
    Given a session's (unique) sid and an end time, this function
    updates the session's end time in the sessions table.
    """
    query = "UPDATE sessions SET endTime=%s WHERE sid=%s"
    params = [endTime, sid]
    return updateData(conn, query, params)
