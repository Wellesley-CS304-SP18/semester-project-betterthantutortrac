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
    if params["isLoggedIn"]:
        username = session['CAS_USERNAME']
        user = interactions.findUsersByUsername(conn, username)
        user["username"] = username
        user["firstName"] = user["name"].split()[0]

        if request.method == "GET":
            ## could replace this all if structuring schema differently
            # for tutors who tutor multiple sections of the same course,
            # the cid for their tutoring session will be for one section
            # of the course (order unspecified)
            tutorCourses = interactions.findCurrentCoursesByTutor(conn, user["pid"])
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
            userData = interactions.findUsersByUsername(conn, username)

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
    pid = interactions.findUsersByUsername(conn, username)['pid']
    if status == 'PROFESSOR':
        
        profCourses = interactions.findCoursesByProf(conn, pid)
        sessions = []
        # find all sessions for any taught courses,
        # since professors should have access to all such session data
        for courseData in profCourses:
            cid = courseData['cid']
            pSessions = list(interactions.findSessions(conn, "cid", cid))
            sessions += pSessions

    elif status == 'STUDENT':
        # first, get all sessions in which the student is a tutee
        sessions = list(interactions.findSessions(conn, "pid", pid))

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
        tutorSessions = list(interactions.getSessions(conn, "pid", pid))
        sessions += tutorSessions

    # add tutor names to sessions
    for sessionData in sessions:
        tid = sessionData['tid']
        tutor = interactions.getUserName(conn, tid)
        if len(tutor) != 0:
            sessionData['tutor'] = tutor[0]['name']

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

    usersData = interactions.findUsersByUsername(conn, username)
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
    userData = interactions.findUsersByUsername(conn, username)
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
    # grab the session
    session = interactions.findSessionById(conn, sid)
    return jsonify(session)
