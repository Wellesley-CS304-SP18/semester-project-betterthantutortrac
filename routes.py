"""
filename: routes.py
author: Angelina Li, Kate Kenneally, Priscilla Lee
last modified: 05/13/2018
description: routes for app
"""

import interactions
import dbconn2
import program
from app import app
from datetime import datetime
from flask import render_template, flash, request, redirect, \
    url_for, session, jsonify
from functools import wraps

## decorator ##

def loginRequired(f):
    """
    Decorator will require the user to login before accessing specified route
    Code from: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if "CAS_USERNAME" not in session:
            flash("Please login before accessing this page!", 
                category="warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decoratedFunction

## logged_in/logged_out routes for CAS ##

@app.route('/loggedIn/')
def loggedIn():
    flash('Successfully logged in!', category="success")
    return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
@app.route("/index/", methods=["GET", "POST"])
def index():
    params = {"isLoggedIn": "CAS_USERNAME" in session}
    conn = interactions.getConn()

    # if tutor forgot to log out, log them out and warn them
    # empty cookie jar from any tutoring sessions that were not logged out
    loggedOut = program.logOutTutorSession(conn)
    if not loggedOut:
        flash("You were automatically logged out of a tutoring session. " + 
            "Please remember to log out next time before you leave!", 
            category="warning")

    # check if user is logged in via CAS
    # additionally, verify that there are currently classes occuring
    if params["isLoggedIn"]:
        username = session['CAS_USERNAME']
        user = interactions.findUser(conn, "username", username)
        user["username"] = username
        user["firstName"] = user["name"].split()[0]

        # tutorCourses is None if no current courses
        tutorCourses = interactions.findCurrentCoursesByTutor(conn, user["pid"])
        if request.method == "GET" and tutorCourses:
            # for tutors who tutor multiple sections of the same course,
            # the cid for their tutoring session will be for one section
            # of the course (order unspecified)
            uniqueCourseNames = []
            uniqueTutorCourses = []
            for c in tutorCourses:
                name = interactions.getCourseName(c, includeSection=False)
                if name not in uniqueCourseNames:
                    c["name"] = name
                    uniqueTutorCourses.append(c)
                    uniqueCourseNames.append(name)
            
            user["isTutor"] = len(uniqueTutorCourses) > 0
            if user["isTutor"]:
                user["tutorCourses"] = uniqueTutorCourses
                user["sessionTypes"] = interactions.findAllSessionTypes()
            
            params["user"] = user
        
        else:
            userId = user.get("pid")
            courseId = request.form.get("course")
            sType = request.form.get("type")
            beginTime = interactions.getSqlDate(datetime.now())

            sessionData = { 
                "pid": userId,
                "cid": courseId,
                "isTutor": 1,
                "beginTime": beginTime,
                "sessionType": sType}
            insertData = interactions.insertSession(conn, sessionData)
            
            if not insertData:
                flash("An error occured while starting the session.", 
                    category="warning")
            else:
                # if successful, start new session
                sess = interactions.findSessionByTimeTutor(
                    conn, beginTime, userId)
                if len(sess) == 1:
                    session["sid"] = sess[0]["sid"]

                session["tid"] = userId
                session["sessionType"] = sType
                session["cid"] = courseId
                session["autoPopulate"] = bool(request.form.get("autoPopulate"))
                return redirect(url_for("newSession"))
     
    return render_template("index.html", **params)

@app.route("/newSession/", methods=["GET", "POST"])
@loginRequired
def newSession():
    params = {"isLoggedIn": True}

    conn = interactions.getConn()
    tid = session.get("tid")
    sid = session.get("sid")
    sType = session.get("sessionType")
    tutorCourseId = session.get("cid")
    autoPop = session.get("autoPopulate")

    # require you to start a session first before enterring student data
    notStartedSession = any([x == None for x in 
        [tid, sType, tutorCourseId, autoPop]])
    if notStartedSession:
        flash("Please start a tutoring session before entering students!",
            category="warning")
        return redirect(url_for("index"))
    
    tutorCourse = interactions.findCourseById(conn, tutorCourseId)
    params["autoPop"] = autoPop
    if autoPop:
        name = interactions.getCourseName(tutorCourse, includeSection=False)
        params["title"] = "{name} Tutoring".format(name=name, sType=sType)
        params["cid"] = tutorCourseId
    else:
        dept = tutorCourse["dept"]
        params["title"] = "{dept} Tutoring".format(dept=dept, sType=sType)
        params["dept"] = dept

    if request.method == "POST":
        submitType = request.form["submit"]
        
        if submitType == "newSession":
            username = request.form.get("username")
            # if autoPop, then cid given by hidden input 'cid'; else, cid
            # given by select object with name 'course'
            # this seems sort of a hassle - can fix this later
            courseIdName = "cid" if autoPop else "course"
            userData = interactions.findUser(conn, "username", username)

            sessionData = { 
                "tid": tid,
                "pid": userData.get("pid"),
                "cid": request.form.get(courseIdName),
                "beginTime": interactions.getSqlDate(datetime.now()),
                "isTutor": 0,
                "sessionType": sType}
            insertData = interactions.insertSession(conn, sessionData)
            
            if insertData:
                flash("{} logged in!".format(username), category="success")
            else:
                flash("An error occured while entering session.", 
                    category="error")
        
        elif submitType == "exitSession":
            program.logOutTutorSession(conn)
            flash("Goodbye!")
            return redirect(url_for("index"))

    return render_template("newSession.html", **params)

## route for viewing tutoring sessions ##

@app.route("/viewSessions/", methods=["GET"])
@loginRequired
def viewSessions():
    params = {"title": "View Tutoring Sessions", "isLoggedIn": True}

    username = session['CAS_USERNAME']
    status = session['CAS_ATTRIBUTES']['cas:widmCode']
    
    conn = interactions.getConn()
    pid = interactions.findUser(conn, "username", username)['pid']
    sessions = []

    ## SCOTT TESTING NOTES ##
    # It seems as though Scott's cas:widmCode is neither student nor
    # professor. For now, we'll assume such people should be treated
    # as *both* students and professors for ease of testing.
    # In the future we may want to further investigate what the possible
    # values this code can take on are and think about what we would
    # like our program to do in those cases.
    ## END SCOTT TESTING NOTES ##

    # anyone except for students should be treated as professors
    if status != 'STUDENT':
        profcourses = interactions.findcoursesbyprof(conn, pid)
        # find all sessions for any taught courses,
        # since professors should have access to all such session data
        for coursedata in profcourses:
            cid = coursedata['cid']
            psessions = list(interactions.findsessions(conn, "cid", cid))
            sessions += psessions

    # anyone except for professors should be treated as students
    elif status != 'PROFESSOR':
        # first, get all sessions in which the student is a tutee
        sessions += list(interactions.findSessions(conn, "pid", pid))

        # next, find all courses that they tutor for
        tutorCourses = interactions.findCoursesByTutor(conn, pid)
        # find all sessions for any tutored courses,
        # since tutors should have access to all such session data
        for courseData in tutorCourses:
            cid = courseData['cid']
            cSessions = list(interactions.findSessions(conn, "cid", cid))
            sessions += cSessions

        # finally, find all sessions they tutored
        # this could be different from the above, since department tutors
        # come attached to one specific class, but can tutor students
        # from different classes within the same department
        tutorSessions = list(interactions.findSessions(conn, "tid", pid))
        sessions += tutorSessions

    # add tutor names to sessions
    for sessionData in sessions:
        tid = sessionData['tid']
        tutor = interactions.findUser(conn, "pid", tid)
        if tutor != None:
            sessionData['tutor'] = tutor['name']

    # get unique sessions - this is inefficient, might want to change
    # in the future
    setTupItems = set(tuple(item.items()) for item in sessions)
    uniqueSessions = [dict(tupItems) for tupItems in setTupItems]
    params["sessions"] = uniqueSessions
    return render_template("viewSessions.html", **params)

## javascript routes for async requests ##

@app.route("/validateUser/", methods=["POST"])
def validateUser():
    data = {}
    conn = interactions.getConn()
    username = request.form.get("username")
    autoPop = request.form.get("autoPop") == "true"
    cid = request.form.get("cid")

    usersData = interactions.findUser(conn, "username", username)
    data["validUsername"] = usersData != None

    if data["validUsername"] and autoPop:
        pid = usersData.get("pid")
        userCourses = interactions.findMatchingCourseSectionsByStudent(
            conn, pid, cid)

        # can a student can only ever be enrolled in one section of a course?
        # if so, we can test if len == 1
        data["validCourse"] = len(userCourses) > 0
        
        if data["validCourse"]:
            data["studentCid"] = userCourses[0]["cid"]

    return jsonify(data)

@app.route("/getUserCourses/", methods=["POST"])
def getUserCourses():
    conn = interactions.getConn()
    username = request.form.get("username")
    dept = request.form.get("dept")
    # find user data and courses by username
    userData = interactions.findUser(conn, "username", username)
    userCourses = interactions.findCurrentCoursesByStudent(
        conn, userData["pid"], dept=dept)
    # format data for front-end use
    formattedCourses = []
    for course in userCourses:
        courseData = {
            "cid": course.get("cid"),
            "name": interactions.getCourseName(course)
        }
        formattedCourses.append(courseData)
    # sort courses and send data to front end
    sortedCourses = sorted(formattedCourses, key=lambda c: c.get("name"))
    return jsonify({"courses": sortedCourses})

@app.route("/getSession/", methods=["POST"])
def getSession():
    conn = interactions.getConn()
    sid = request.form.get("sid")

    # grab the current session information
    # and populate 4 options (tutors, students, courses, sessionTypes)
    # indicate current option using "selected" html tag
    session = interactions.findSessionById(conn, sid)

    # tutors
    tutors = []
    for item in interactions.findAllStudents(conn):
        if (item["pid"] == session["tid"]):
            item["selected"] = "selected"
        else:
            item["selected"] = ""
        tutors.append(item)
    if session["tid"] is None:
        tutors.append({"pid": -1, "name": "Select a tutor", "selected": "selected"})

    # students
    students = []
    for item in interactions.findAllStudents(conn):
        if (item["pid"] == session["pid"]):
            item["selected"] = "selected"
        else:
            item["selected"] = ""
        students.append(item)

    # courses
    courses = []
    for item in interactions.findCurrentCourses(conn):
        if (item["cid"] == session["cid"]):
            item["selected"] = "selected"
        else:
            item["selected"] = ""
        courses.append(item)

    # sessionTypes
    sessionTypes = []
    for item in interactions.findAllSessionTypes():
        if item == session["sessionType"]:
            sessionTypes.append({"sessionType": item, "selected": "selected"})
        else: 
            sessionTypes.append({"sessionType": item, "selected": ""})

    result = {
        "tutors": tutors, 
        "students": students, 
        "courses": courses, 
        "sessionTypes": sessionTypes}
    
    return jsonify(result)

@app.route("/deleteSession/", methods=["POST"])
def deleteSession():
    conn = interactions.getConn()
    sid = request.form.get("sid")
    interactions.deleteSession(conn, sid)
    flash("Session successfully deleted")
    return jsonify({"sid": sid})

@app.route("/updateSession/", methods=["POST"])
def updateSession():
    conn = interactions.getConn()
    sid = request.form.get("sid")
    tid = request.form.get("tid")
    pid = request.form.get("pid")
    cid = request.form.get("cid")
    sessionType = request.form.get("sessionType")
    interactions.updateSession(conn, sid, tid, pid, cid, sessionType)
    flash("Session successfully updated")
    return jsonify({"sid": sid})

