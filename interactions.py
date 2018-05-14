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

database = 'kkenneal_db' # for testing; update with project db later

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
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query, params)
    if fetchall:
        return curs.fetchall()
    return curs.fetchone()

def getUserName(conn, pid):
    query = "SELECT name from users where pid=%s"
    params = [pid]
    return getSqlQuery(conn, query, params)

def findUsersByName(conn, name):
    query = "SELECT * FROM users WHERE name LIKE %s"
    params = ["%" + name + "%"]
    return getSqlQuery(conn, query, params)

def findUsersByEmail(conn, email):
    # emails are unique, so we can require a unique match
    # e.g. ali@wellesley.edu shouldn't return kkenneal@wellesley.edu
    query = "SELECT * FROM users WHERE email=%s"
    params = [email]
    return getSqlQuery(conn, query, params)

def findUsersByUsername(conn, username):
    email = username + "@wellesley.edu" # a wrapper around the last fn
    return findUsersByEmail(conn, email)

def findCourseById(conn, cid):
    query = "SELECT * FROM courses WHERE cid=%s"
    params = [cid]
    return getSqlQuery(conn, query, params)

def findCoursesByName(conn, dept, courseNum):
    query = "SELECT * FROM courses WHERE dept LIKE %s AND courseNum LIKE %s"
    params = ["%" + dept + "%", "%" + courseNum + "%"]
    return getSqlQuery(conn, query, params)

def findCoursesByStudent(conn, pid):
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findDeptCoursesByStudent(conn, pid, dept):
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s AND dept=%s"""
    params = [pid, dept]
    return getSqlQuery(conn, query, params)

def findCoursesByProf(conn, pid):
    query = """SELECT * FROM courses INNER JOIN coursesTaught USING (cid) 
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findCoursesByTutor(conn, pid):
    query = """SELECT * FROM courses INNER JOIN tutors USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findAllSessions(conn): 
    # want student name, course name, and session type. fix up later.
    query = """
        SELECT *
        FROM sessions 
        INNER JOIN courses USING (cid) 
        INNER JOIN users USING (pid)"""
    return getSqlQuery(conn, query)

def findSessionByTimeTutor(conn, beginTime, tid):
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE beginTime=%s AND pid=%s AND isTutor=1"""
    params = [beginTime, tid]
    return getSqlQuery(conn, query, params)

def findMatchingSessions(conn, searchTerm):
    query = """SELECT * FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE name LIKE %s OR courseNum LIKE %s OR dept LIKE %s"""
    params = ["%" + searchTerm + "%" for _ in range(len(3))]
    return getSqlQuery(conn, query, params)

def findSessionsByStudent(conn, pid):
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE pid=%s"""
    params = [pid]
    return getSqlQuery(conn, query, params)

def findSessionsByCourse(conn, cid):
    query = """SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE cid=%s"""
    params = [cid]
    return getSqlQuery(conn, query, params)

### database interaction INSERT functions ###

def insertData(conn, query, params):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(query, params)
        return True
    except Exception as e:
        print "Exception:", e
        return False

def insertUser(conn, data):
    paramOrder = ["pid", "name", "email", "password", "permissions", "year",
        "bnumber", "userType"]
    query = "INSERT INTO users ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)

def insertCourse(conn, data):
    paramOrder = ["cid", "dept", "courseNum", "section", "year", "semester"]
    query = "INSERT INTO courses ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)

def insertStudentCourse(conn, data):
    query = "INSERT INTO coursesTaken (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertProfCourse(conn, data):
    query = "INSERT INTO coursesTaught (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertTutorCourse(conn, data):
    query = "INSERT INTO tutors (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return insertData(conn, query, params)

def insertSession(conn, data):
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

### update interactions ###

def updateData(conn, query, params):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(query, params)
        return True
    except Exception as e:
        print "Exception:", e
        return False

def updateSessionEndTime(conn, sid, endTime):
    query = "UPDATE sessions SET endTime=%s WHERE sid=%s"
    params = [endTime, sid]
    return updateData(conn, query, params)
