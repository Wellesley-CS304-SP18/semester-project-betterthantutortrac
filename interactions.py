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

def getCurrentTime():
    """
    Will return a dictionary containing the current year and semester.
    This is based on the Academic Calendar for Summer 2018 - Spring 2019.
    Eventually we may want to update this function to more closely
    peg to the actual Wellesley Academic Calendar.
    """
    now = datetime.date.today()
    year = now.year
    semesters = [
        {"name": "Summer I",
        "startDate": datetime.date(year=year, month=6, day=4),
        "endDate": datetime.date(year=year, month=6, day=29)},
        {"name": "Summer II",
        "startDate": datetime.date(year=year, month=7, day=2),
        "endDate": datetime.date(year=year, month=7, day=27)},
        {"name": "Fall", 
        "startDate": datetime.date(year=year, month=9, day=4),
        "endDate": datetime.date(year=year, month=12, day=20)},
        {"name": "Winter",
        "startDate": datetime.date(year=year, month=1, day=3),
        "endDate": datetime.date(year=year, month=1, day=24)},
        {"name": "Spring",
        "startDate": datetime.date(year=year, month=1, day=28),
        "endDate": datetime.date(year=year, month=5, day=21)}
    ]
    semester = None
    for s in semesters:
        if s["startDate"] <= now <= s["endDate"]:
            semester = s["name"]
            break
    return {"year": year, "semester": semester}

def getCourseName(courseData, includeSection=True):
    nameFormat = "{dept} {courseNum}"
    if includeSection:
        nameFormat += "-{section}"
    return nameFormat.format(**courseData)

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

def findUser(conn, searchTerm, searchValue):
    """
    Given a user's (unique) searchTerm and searchValye, this function
    returns the specified user's data.
    """
    if searchTerm == "username":
        # just a wrapper around email searching
        return findUser(conn, "email", searchValue + "@wellesley.edu")
    query = "SELECT * FROM users WHERE {}=%s".format(searchTerm)
    params = [searchValue]
    return getSqlQuery(conn, query, params, fetchall=False)

def findUsersByName(conn, name):
    """
    Given a name, this function returns data for all matching users.
    """
    query = "SELECT * FROM users WHERE name LIKE %s"
    params = ["%" + name + "%"]
    return getSqlQuery(conn, query, params)

def findCourseById(conn, cid):
    """
    Given a course's (unique) cid, this function returns the course's data.
    """
    query = "SELECT * FROM courses WHERE cid=%s"
    params = [cid]
    return getSqlQuery(conn, query, params, fetchall=False)

def findCoursesByName(conn, dept, courseNum):
    """
    Given a course's name (department + course number), this function returns
    data for all matching courses.
    """
    query = "SELECT * FROM courses WHERE dept LIKE %s AND courseNum LIKE %s"
    params = ["%" + dept + "%", "%" + courseNum + "%"]
    return getSqlQuery(conn, query, params)

def findCoursesByStudent(conn, pid, dept=None):
    """
    Given a student's (unique) pid and optionally a dept name, this function 
    returns data on all courses taken by the student.
    """
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    if dept:
        query += " AND dept=%s"
        params += [dept]
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

def findCurrentCoursesByStudent(conn, pid, dept=None):
    timeNow = getCurrentTime()
    # when the semester is not specified, classes are not in session.
    if timeNow["semester"] == None:
        return None

    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s AND courses.year=%s AND semester=%s"""
    params = [pid, timeNow["year"], timeNow["semester"]]
    if dept:
        query += " AND dept=%s"
        params += [dept]
    return getSqlQuery(conn, query, params)

def findCurrentCoursesByTutor(conn, pid):
    timeNow = getCurrentTime()
    # when the semester is not specified, classes are not in session.
    if timeNow["semester"] == None:
        return None

    query = """SELECT * FROM courses INNER JOIN tutors USING (cid)
        WHERE pid=%s AND courses.year=%s AND semester=%s"""
    params = [pid, timeNow["year"], timeNow["semester"]]
    return getSqlQuery(conn, query, params)

def findMatchingCourseSectionsByStudent(conn, pid, cid):
    """
    Given a course, will find all matching sections of that course in the
    same time period that a specified student is attending.
    """
    courseData = findCourseById(conn, cid)
    courseParams = ["year", "semester", "dept", "courseNum"]
    query = """SELECT * FROM courses INNER JOIN coursesTaken USING (cid)
        WHERE pid=%s"""
    params = [pid]
    for p in courseParams:
        params.append(courseData[p])
        query += " AND {p}=%s".format(p=p)
    print "params:", params
    print "query:", query
    return getSqlQuery(conn, query, params)

def findAllSessions(conn):
    """
    This function returns data on all tutoring sessions.
    """
    query = """
        SELECT *
        FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)"""
    return getSqlQuery(conn, query)

def findSessions(conn, searchTerm, searchValue):
    """
    Given a search term and a search value, this function returns data on
    all of the sessions that the user is searching over.
    """
    query = """SELECT * FROM sessions
        INNER JOIN courses USING (cid)
        INNER JOIN users USING (pid)
        WHERE {}=%s""".format(searchTerm)
    params = [searchValue]
    return getSqlQuery(conn, query, params)

def findSessionById(conn, sid):
    """
    Given a session's (unique) sid, this function returns particular pieces of
    information about the session (i.e. the information needed to display the
    sessions table on the viewSessions page.
    """
    query = """SELECT * FROM 
        (SELECT s.sid, s.tid, s.sessionType, u.name as student, c.dept, c.courseNum, c.section, s.beginTime, s.endTime 
        FROM sessions AS s 
        INNER JOIN users AS u USING (pid) 
        INNER JOIN courses AS c USING (cid) 
        WHERE sid=%s) AS temp 
        INNER JOIN users WHERE (tid=pid);"""
    params = [sid]
    return getSqlQuery(conn, query, params, fetchall=False)

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

### database interaction INSERT functions ###

def executeQuery(conn, query, params):
    """
    This function executes a given SQL query and
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
    return executeQuery(conn, query, params)

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
    return executeQuery(conn, query, params)

def insertStudentCourse(conn, data):
    """
    Given the appropriate data, this function inserts a student/course
    relationship into the coursesTaken table in our database.
    """
    query = "INSERT INTO coursesTaken (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return executeQuery(conn, query, params)

def insertProfCourse(conn, data):
    """
    Given the appropriate data, this function inserts a professor/course
    relationship into the coursesTaught table in our database.
    """
    query = "INSERT INTO coursesTaught (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return executeQuery(conn, query, params)

def insertTutorCourse(conn, data):
    """
    Given the appropriate data, this function inserts a tutor/course
    relationship into the tutors table in our database.
    """
    query = "INSERT INTO tutors (pid, cid) VALUES (%s, %s)"
    params = [data["pid"], data["cid"]]
    return executeQuery(conn, query, params)

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
    return executeQuery(conn, query, params)

### database interaction UPDATE functions ###

def updateSessionEndTime(conn, sid, endTime):
    """
    Given a session's (unique) sid and an end time, this function
    updates the session's end time in the sessions table.
    """
    query = "UPDATE sessions SET endTime=%s WHERE sid=%s"
    params = [endTime, sid]
    return executeQuery(conn, query, params)

### database interaction DELETE functions ###

def deleteSession(conn, sid):
    """
    Given a session's (unique) sid, this function will delete the session
    data associated with this sid.
    """
    query = "DELETE FROM sessions WHERE sid=%s"
    params = [sid]
    return executeQuery(conn, query, params)
