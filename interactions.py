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

def getConn(dsn):
    return dbconn2.connect(dsn)

### database interaction FIND functions ###

def findUsersByName(name):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from users where name like %s", ["%" + name + "%"])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findUsersByEmail(email):
    try:
        # emails are unique, so we can require a unique match
        # e.g. al@wellesley.edu shouldn't return kkenneal@wellesley.edu
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from users where email=%s", [email])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findUsersByUsername(username):
    email = username + "@wellesley.edu" # just a wrapper around the next fn
    return findUsersByEmail(email)

def findCoursesByName(dept, courseNum):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from courses where dept like %s and courseNum like %s", ["%" + dept + "%", "%" + courseNum + "%"])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findCoursesByStudent(pid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "select * from courses inner join coursesTaken on courses.cid=coursesTaken.cid where pid=%s", [pid])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findAllSessions():
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions")
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findAllSessions2(): # want student name, course name, and session type. fix up later.
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select name, dept, courseNum, sessionType from sessions inner join courses on (cid=cid) inner join users on (userId=pid)")
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findSessionsByStudent(pid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions where userId=%s", [pid])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findSessionsByCourse(cid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions where cid=%s", [cid])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

### database interaction INSERT functions ###

def insertUser(data):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "insert into users (pid, name, email, password, permissions, year, bnumber, userType) values (%s, %s, %s, %s, %s, %s, %s, %s)", 
            [data['pid'], data['name'], data['email'], data['password'], data['permissions'], data['year'], data['bnumber'], data['userType']])
        return True
    except:
        return False

def insertCourse(data):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "insert into courses (cid, dept, courseNum, section, year, semester) values (%s, %s, %s, %s, %s, %s)", 
            [data['cid'], data['dept'], data['courseNum'], data['section'], data['year'], data['semester']])
        return True
    except Exception:
        return False

def insertStudentCourse(pid, cid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into coursesTaken (pid, cid) values (%s, %s)", [pid, cid])
        return True
    except Exception:
        return False

def insertProfCourse(pid, cid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into coursesTaught (pid, cid) values (%s, %s)", [pid, cid])
        return True
    except Exception:
        return False

def insertSession(data):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "insert into sessions (userId, cid, isTutor, sessionType) values (%s, %s, %s, %s)",
            [data['userId'], data['cid'], data['isTutor'], data['sessionType']])
#        curs.execute(
#            "insert into sessions (userId, cid, isTutor, beginTime, endTime, sessionType) values (%s, %s, %s, %s, %s, %s)", 
#            [data['userId'], data['cid'], data['isTutor'], data['beginTime'], data['endTime'], data['sessionType']])
        return True
    except Exception:
        print "insert session exception", Exception
        return False
