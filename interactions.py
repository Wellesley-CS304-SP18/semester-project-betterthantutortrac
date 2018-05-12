#!/user/local/bin/python2.7

"""
filename: interactions.py
author: Kate Kenneally
last modified: 05/01/2018
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

def getSQLQuery(conn, query, params, fetchall=False):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute(query, params)
    if fetchall:
        return curs.fetchall()
    return curs.fetchone()

def findUsersByName(conn, name):
    query = "SELECT * FROM users WHERE name LIKE %s"
    params = ["%" + name + "%"]
    return getSQLQuery(conn, query, params, fetchall=True)

def findUsersByEmail(conn, email):
    # emails are unique, so we can require a unique match
    # e.g. al@wellesley.edu shouldn't return kkenneal@wellesley.edu
    query = "SELECT * FROM users WHERE email=%s"
    params = [email]
    return getSQLQuery(conn, query, params, fetchall=True)

def findUsersByUsername(conn, username):
    email = username + "@wellesley.edu" # just a wrapper around the last fn
    return findUsersByEmail(conn, email)

def findCoursesByName(conn, dept, courseNum):
    query = "SELECT * FROM courses WHERE dept LIKE %s AND courseNum LIKE %s"
    params = ["%" + dept + "%", "%" + courseNum + "%"]
    return getSQLQuery(conn, query, params, fetchall=True)

def findCoursesByStudent(conn, pid):
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    return getSQLQuery(conn, query, params, fetchall=True)

def findAllSessions(conn):
    return getSQLQuery(conn, "SELECT * FROM sessions", [], fetchall=True)

def findAllSessions2(conn): # want student name, course name, and session type. fix up later.
    query = """SELECT name, dept, courseNum, sessionType FROM sessions
        INNER JOIN courses USING (cid) INNER JOIN users USING (pid)"""
    params = []
    return getSQLQuery(conn, query, params, fetchall=True)

def findSessionsByStudent(conn, pid):
    query = "SELECT * FROM sessions WHERE pid=%s"
    params = [pid]
    return getSQLQuery(conn, query, params, fetchall=True)

def findSessionsByCourse(conn, cid):
    query = "SELECT * FROM sessions WHERE cid=%s"
    params = [cid]
    return getSQLQuery(conn, query, params, fetchall=True)

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
