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

def get_dsn(db):
    dsn = dbconn2.read_cnf()
    dsn['db'] = db
    return dsn

def getConn(dsn):
    return dbconn2.connect(dsn)

### database interaction FIND functions ###

def findUsersByName(name):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from users where name like %s", ["%" + name + "%"])
        rows = curs.fetchall()
        return rows
    except:
        return []

def findUsersByEmail(email):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from users where email like %s", ["%" + email + "%"])
        rows = curs.fetchall()
        return rows
    except:
        return []

def findCoursesByName(dept, coursenum):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from courses where dept like %s and coursenum like %s", 
                     ["%" + dept + "%", "%" + coursenum + "%"])
        rows = curs.fetchall()
        return rows
    except:
        return []

def findCoursesByStudent(pid):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from courses_taken where student_id=%s", [pid])
        rows = curs.fetchall()
        return rows
    except:
        return []

def findAllSessions():
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions")
        rows = curs.fetchall()
        return rows
    except:
        return []

def findSessionsByStudent(pid):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions where user_id=%s", [pid])
        rows = curs.fetchall()
        return rows
    except:
        return []

def findSessionsByCourse(cid):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select * from sessions where course_id=%s", [cid])
        rows = curs.fetchall()
        return rows
    except:
        return []

### database interaction INSERT functions ###

def insertUser(data):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into users (pid, name, email, password, permissions, year, bnumber, usertype values (%s, %s, %s, %s, %s, %s, %s, %s" [data['pid'], data['name'], data['email'], data['password'], data['permissions'], data['year'], data['bnumber'], data['usertype']])
        return True
    except:
        return False

def insertCourse(data):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into courses (cid, dept, coursenum, section, year, semester) values (%s, %s, %s, %s, %s, %s" [data['cid'], data['dept'], data['coursenum'], data['section'], data['year'], data['semester']])
        return True
    except:
        return False

def insertStudentCourse(pid, cid):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into courses_taken (student_id, course_id) values (%s, %s)" [pid, cid])
        return True
    except:
        return False

def insertProfCourse(pid, cid):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into courses_taught (prof_id, course_id) values (%s, %s)" [pid, cid])
        return True
    except:
        return False

def insertSession(data):
    try:
        conn = getConn(get_dsn(database))
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("insert into sessions (user_id, course_id, is_tutor, begin_time, end_time, sessiontype values (%s, %s, %s, %s, %s, %s)" [data['user_id'], data['course_id'], data['is_tutor'], data['begin_time'], data['end_time'], data['sessiontype']])
        return True
    except:
        return False
