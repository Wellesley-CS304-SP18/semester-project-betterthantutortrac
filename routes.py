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

    # empty cookie jar from any tutoring sessions that were not logged out
    cookieNames = ["tid", "sid", "sessionType", "cid", "autoPopulate"]
    for c in cookieNames:
        session.pop(c, None)

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
                sess = interactions.findSessionByTimeTutor(conn, beginTime, userId)
                if len(sess) == 1:
                    session["sid"] = sess[0]["sid"]

                session["tid"] = userId
                session["sessionType"] = sType
                session["cid"] = courseId
                session["autoPopulate"] = bool(populate)
                return redirect(url_for("newSession"))
            else:
                flash("An error occured while starting the session.")
        
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
        print 'CAS_USERNAME is: ', username
    else:
        print 'CAS_USERNAME is not in the session'
    
    params["isLoggedIn"] = isLoggedIn
    return render_template("index.html", **params)

@app.route("/newSession/", methods=["GET", "POST"])
def newSession():
    params = {}

    # user needs to be logged in to insert a session
    if 'CAS_USERNAME' in session:
        conn = interactions.getConn()

        tid = session.get("tid")
        sid = session.get("sid")
        sType = session.get("sessionType")
        tutorCourseId = session.get("cid")
        autoPop = session.get("autoPopulate")

        if any([x == None for x in [tid, sType, tutorCourseId, autoPop]]):
            flash("Please start a tutoring session before entering students!")
            return redirect(url_for("index"))
        
        tutorCourse = interactions.findCourseById(conn, tutorCourseId)[0]
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

            if request.form["submit"] == "newSession":
                username = request.form.get("username")
                # if autoPop, then cid given by hidden input 'cid'; else, cid
                # given by select object with name 'course'
                courseIdName = "cid" if autoPop else "course"
                courseId = request.form.get(courseIdName)

                userData = interactions.findUsersByUsername(conn, username)[0]
                userId = userData.get("pid")

                now = datetime.now()
                beginTime = interactions.getSqlDate(now)

                # add begin and end times later
                sessionData = { 
                    "tid": tid,
                    "pid": userId,
                    "cid": courseId,
                    "isTutor": 0,
                    "beginTime": beginTime,
                    "sessionType": sType}
                insertData = interactions.insertSession(conn, sessionData)
                if insertData:
                    flash("{} logged in!".format(username))
                else:
                    flash("An error occured while entering session.")
            
            else:
                if sid:
                    now = datetime.now()
                    endTime = interactions.getSqlDate(now)
                    updateData = interactions.updateSessionEndTime(
                        conn, sid, endTime)
                
                cookieNames = ["tid", "sid", "sessionType", "cid", "autoPopulate"]
                for c in cookieNames:
                    session.pop(c, None)

                flash("Goodbye!")
                return redirect(url_for("index"))

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

        # add tutor names to sessions
        for sessionData in sessions:
            tid = sessionData['tid']
            tutor = interactions.getUserName(conn, tid)
            if len(tutor) == 0:
                sessionData['tutor'] = "None"
            else:
                sessionData['tutor'] = tutor[0]['name']

        params["sessions"] = sessions
        params["isLoggedIn"] = True
        return render_template("viewSessions.html", **params)
    else:
        flash("Please log in to view sessions.")
        return redirect(url_for('index'))


## javascript routes for async requests ##

@app.route("/validateUser/", methods=["POST"])
def validateUser():
    data = {}
    conn = interactions.getConn()
    username = request.form.get("username")
    autoPop = request.form.get("autoPop")
    cid = request.form.get("cid")

    usersData = interactions.findUsersByUsername(conn, username)
    data["validUsername"] = len(usersData) == 1

    if data["validUsername"] and autoPop:
        pid = usersData[0].get("pid")
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
    userData = interactions.findUsersByUsername(conn, username)[0]
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

