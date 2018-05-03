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

def findCoursesByName(dept, coursenum):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from courses where dept like %s and coursenum like %s", ["%" + dept + "%", "%" + coursenum + "%"])
        rows = curs.fetchall()
        return rows
    except Exception:
        return []

def findCoursesByStudent(pid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "select * from courses inner join coursesTaken on courses.cid=coursesTaken.courseId where studentId=%s", [pid])
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
        curs.execute("select * from sessions where courseId=%s", [cid])
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
            "insert into users (pid, name, email, password, permissions, year, bnumber, usertype) values (%s, %s, %s, %s, %s, %s, %s, %s)", 
            [data['pid'], data['name'], data['email'], data['password'], data['permissions'], data['year'], data['bnumber'], data['usertype']])
        return True
    except:
        return False

def insertCourse(data):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "insert into courses (cid, dept, coursenum, section, year, semester) values (%s, %s, %s, %s, %s, %s)", 
            [data['cid'], data['dept'], data['coursenum'], data['section'], data['year'], data['semester']])
        return True
    except Exception:
        return False

def insertStudentCourse(pid, cid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into coursesTaken (studentId, courseId) values (%s, %s)", [pid, cid])
        return True
    except Exception:
        return False

def insertProfCourse(pid, cid):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into coursesTaught (profId, courseId) values (%s, %s)", [pid, cid])
        return True
    except Exception:
        return False

def insertSession(data):
    try:
        conn = getConn(getDsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            "insert into sessions (userId, courseId, isTutor, beginTime, endTime, sessiontype) values (%s, %s, %s, %s, %s, %s)", 
            [data['userId'], data['courseId'], data['isTutor'], data['beginTime'], data['endTime'], data['sessiontype']])
        return True
    except Exception:
        return False
