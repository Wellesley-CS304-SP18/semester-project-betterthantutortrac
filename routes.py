"""
filename: routes.py
author: Angelina Li, Kate Kenneally, Priscilla Lee
last modified: 05/13/2018
description: routes for app
"""

import interactions
import dbconn2
from app import app
from datetime import datetime
from flask import render_template, flash, request, redirect, url_for, session, jsonify

## logged_in/logged_out routes for CAS ##

@app.route('/logged_in/')
def logged_in():
    flash('Successfully logged in!')
    return redirect(url_for('index'))

@app.route('/logged_out/')
def logged_out():
    flash('Successfully logged out!')
    return redirect(url_for('index'))

@app.route("/", methods=["GET", "POST"])
@app.route("/index/", methods=["GET", "POST"])
def index():
    params = {}

    # start CAS debugging
    print 'Session keys: ', session.keys()
    for k in session.keys():
        print k, ' => ', session[k]
    if '_CAS_TOKEN' in session:
        token = session['_CAS_TOKEN']
    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        print 'CAS_attributes: '
        for k in attribs:
            print '\t', k, ' => ', attribs[k]
    # end CAS debugging
    
    # check if user is logged in via CAS
    isLoggedIn = False
    if 'CAS_USERNAME' in session:
        isLoggedIn = True
        
        conn = interactions.getConn()
        username = session['CAS_USERNAME']
        user = interactions.findUsersByUsername(conn, username)[0]
        user["username"] = username
        user["firstName"] = user["name"].split()[0]

        if request.method == "POST":
            userId = user.get("pid")
            courseId = request.form.get("course")
            sType = request.form.get("type")
            populate = request.form.get("autoPopulate")
            now = datetime.now()
            beginTime = interactions.getSqlDate(now)

            sessionData = { 
                "pid": userId,
                "cid": courseId,
                "isTutor": 1,
                "beginTime": beginTime,
                "sessionType": sType}
            insertData = interactions.insertSession(conn, sessionData)
            
            if insertData:
                session["tid"] = userId
                session["sessionType"] = sType
                session["cid"] = courseId
                session["autoPopulate"] = bool(populate)
                return redirect(url_for("newSession"))
            else:
                flash("An error occured while starting the session.")

        tutorCourses = interactions.findCoursesByTutor(conn, user["pid"])
        for c in tutorCourses:
            c["name"] = interactions.getCourseName(c)

        user["isTutor"] = len(tutorCourses) > 0
        if user["isTutor"]:
            user["tutorCourses"] = tutorCourses
            user["sessionTypes"] = interactions.findAllSessionTypes()
        
        params["user"] = user
        print('CAS_USERNAME is: ', username)
    else:
        print('CAS_USERNAME is not in the session')
    
    params["isLoggedIn"] = isLoggedIn
    return render_template("index.html", **params)

@app.route("/newSession/", methods=["GET", "POST"])
def newSession():
    params = {}

    # user needs to be logged in to insert a session
    if 'CAS_USERNAME' in session:
        conn = interactions.getConn()

        tid = session.get("tid")
        sType = session.get("sessionType")
        tutorCourseId = session.get("cid")
        tutorCourse = interactions.findCourseById(conn, tutorCourseId)[0]
        autoPop = session.get("autoPopulate")
        courseId = None

        if any([x == None for x in [tid, sType, tutorCourseId, autoPop]]):
            print "tid:", tid, "sType:", sType, "tutorCourseId:", tutorCourseId, "autoPop:", autoPop
            flash("Please start a tutoring session before entering students!")
            return redirect(url_for("index"))

        if autoPop:
            name = interactions.getCourseName(tutorCourse)
            params["title"] = "{name} Session".format(name=name, sType=sType)
        else:
            dept = tutorCourse["dept"]
            params["title"] = "{dept} Session".format(dept=dept, sType=sType)

        if request.method == "POST":
            username = request.form.get("username")
            courseId = request.get("cid")
            if courseId == None:
                # if the courseId wasn't pre-set
                courseId = request.form.get("course")

            userData = interactions.findUsersByUsername(conn, username)[0]
            userId = userData.get("pid")

            now = datetime.now()
            beginTime = interactions.getSqlDate(now)

            # add begin and end times later
            sessionData = { 
                "pid": userId,
                "cid": courseId,
                "isTutor": 0,
                "beginTime": beginTime,
                "sessionType": sType}
            insertData = interactions.insertSession(conn, sessionData)
            if insertData:
                flash("{} logged in!".format(userData["username"]))
            else:
                flash("An error occured while entering session.")
        
        params["isLoggedIn"] = True
        return render_template("newSession.html", **params)
    
    else:
        flash("Please log in to insert a session.")
        return redirect(url_for('index'))


## route for viewing tutoring sessions ##

@app.route("/viewSessions/", methods=["GET"])
def viewSessions():
    params = {"title": "View Tutoring Sessions"}

    # user needs to be logged in to view sessions
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
        status = session['CAS_ATTRIBUTES']['cas:widmCode']

        conn = interactions.getConn()
        pid = interactions.findUsersByUsername(conn, username)[0]['pid']
        if status == 'PROFESSOR':
            # get all courses that the professor teaches
            profCourses = interactions.findCoursesByProf(conn, pid)
            sessions = []
            # find all sessions for any taught courses,
            # since professors should have access to all such session data
            for courseData in profCourses:
                cid = courseData['cid']
                sessions.extend(list(interactions.findSessionsByCourse(conn, cid)))
        elif status == 'STUDENT':
            # first, get all sessions in which the student is a tutee
            sessions = list(interactions.findSessionsByStudent(conn, pid))
            # next, in case the student is a tutor, find all courses that they tutor for
            tutorCourses = interactions.findCoursesByTutor(conn, pid)
            # find all sessions for any tutored courses,
            # since tutors should have access to all such session data
            for courseData in tutorCourses:
                cid = courseData['cid']
                sessions.extend(list(interactions.findSessionsByCourse(conn, cid)))
        params["sessions"] = sessions
        params["isLoggedIn"] = True
        return render_template("viewSessions.html", **params)
    else:
        flash("Please log in to view sessions.")
        return redirect(url_for('index'))


## javascript routes for async requests ##

@app.route("/validateUser/", methods=["POST"])
def validateUser():
    conn = interactions.getConn()
    username = request.form.get("username")
    usersData = interactions.findUsersByUsername(conn, username)
    return jsonify({"validate": len(usersData) == 1})

@app.route("/getUserClasses/", methods=["POST"])
def getUserClasses():
    conn = interactions.getConn()
    username = request.form.get("username")
    # find user data and courses by username
    userData = interactions.findUsersByUsername(conn, username)[0]
    userCourses = interactions.findCoursesByStudent(conn, userData["pid"])
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

@app.route("/getSessionTypes/", methods=["POST"])
def getSessionTypes():
    # types of tutoring sessions
    sessionTypes = interactions.findAllSessionTypes()
    return jsonify({"types": sessionTypes})

