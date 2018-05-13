#!/user/local/bin/python2.7

"""
filename: interactions.py
authors: Kate Kenneally, Angelina Li
last modified: 05/13/2018
description: python to SQL interactions
"""

import sys
import MySQLdb
import dbconn2

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

### database interaction FIND functions ###

def getSQLQuery(conn, query, params=[], fetchall=True):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query, params)
    if fetchall:
        return curs.fetchall()
    return curs.fetchone()

def findUsersByName(conn, name):
    query = "SELECT * FROM users WHERE name LIKE %s"
    params = ["%" + name + "%"]
    return getSQLQuery(conn, query, params)

def findUsersByEmail(conn, email):
    # emails are unique, so we can require a unique match
    # e.g. ali@wellesley.edu shouldn't return kkenneal@wellesley.edu
    query = "SELECT * FROM users WHERE email=%s"
    params = [email]
    return getSQLQuery(conn, query, params)

def findUsersByUsername(conn, username):
    email = username + "@wellesley.edu" # a wrapper around the last fn
    return findUsersByEmail(conn, email)

def findCoursesByName(conn, dept, courseNum):
    query = "SELECT * FROM courses WHERE dept LIKE %s AND courseNum LIKE %s"
    params = ["%" + dept + "%", "%" + courseNum + "%"]
    return getSQLQuery(conn, query, params)

def findCoursesByStudent(conn, pid):
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSQLQuery(conn, query, params)

def findAllSessions(conn): 
    # want student name, course name, and session type. fix up later.
    query = """
        SELECT name, dept, courseNum, section, sessionType, 
               isTutor, beginTime, endTime
        FROM sessions 
        INNER JOIN courses USING (cid) 
        INNER JOIN users USING (pid)"""
    return getSQLQuery(conn, query)

def findMatchingSessions(conn, searchTerm):
    query = """
        SELECT name, dept, courseNum, section, sessionType,
               isTutor, beginTime, endTime
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE name LIKE %s OR courseNum LIKE %s OR dept LIKE %s"""
    params = ["%" + searchTerm + "%" for _ in range(len(3))]
    return getSQLQuery(conn, query, params)

def findSessionsByStudent(conn, pid):
    query = "SELECT * FROM sessions WHERE pid=%s"
    params = [pid]
    return getSQLQuery(conn, query, params)

def findSessionsByCourse(conn, cid):
    query = "SELECT * FROM sessions WHERE cid=%s"
    params = [cid]
    return getSQLQuery(conn, query, params)

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
    query = "INSERT INTO sessions ({pNames}) VALUES ({pVals})".format(
        pNames=", ".join(paramOrder),
        pVals=", ".join(["%s" for _ in range(len(paramOrder))])
    )
    params = [data[p] for p in paramOrder]
    return insertData(conn, query, params)
