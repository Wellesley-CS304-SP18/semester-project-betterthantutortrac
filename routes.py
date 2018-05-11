"""
filename: routes.py
author: Angelina Li, 
last modified: 04/28/2018
description: routes for app
"""

import interactions
import dbconn2
from app import app
from datetime import datetime
from flask import render_template, flash, request, redirect, url_for, session, jsonify

@app.route('/logged_in/')
def logged_in():
    flash('Successfully logged in!')
    return redirect(url_for('index'))

@app.route('/logged_out/')
def logged_out():
    flash('Successfully logged out!')
    return redirect(url_for('index'))

@app.route("/", methods=["GET"])
@app.route("/index/", methods=["GET"])
def index():
    params = {"title": "Home"}
    
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
    
    if 'CAS_USERNAME' in session:
        isLoggedIn = True
        username = session['CAS_USERNAME']
        print('CAS_USERNAME is: ', username)
    else:
        isLoggedIn = False
        username = None
        print('CAS_USERNAME is not in the session')
    
    params["username"] = username
    params["isLoggedIn"] = isLoggedIn
    return render_template("index.html", **params)

@app.route("/newSession/", methods=["GET", "POST"])
def newSession():
    params = {"title": "Insert a Tutoring Session"}
    if 'CAS_USERNAME' in session:
        if request.method == "POST":
            username = request.form.get("username")
            course = request.form.get("course")
            sType = request.form.get("type")

            userData = interactions.findUsersByUsername(username)[0]
            userId = userData.get("pid")

            dept = course.split()[0]
            coursenum = course.split()[1][0:3] # clean this up later
            courseData = interactions.findCoursesByName(dept, coursenum)[0]
            courseId = courseData.get("cid")
            
            print "the cid for", dept, coursenum, "is", courseId

            sessionData = { # add begin and end times later
                "pid": userId,
                "cid": courseId,
                "isTutor": 'n', # update this later
                "sessionType": sType}
            insertData = interactions.insertSession(sessionData)
            if insertData:
                flash("Tutoring session entered successfully.")
            else:
                flash("Failed to enter tutoring sessions.")
        
        params["isLoggedIn"] = True
        return render_template("newSession.html", **params)
    else:
        flash("Please log in to insert a session.")
        return redirect(url_for('index'))
        
@app.route("/viewSessions/", methods=["GET"])
def viewSessions():
    params = {"title": "View Tutoring Sessions"}
    if 'CAS_USERNAME' in session:
        sessions = interactions.findAllSessions2()
        params["sessions"] = sessions
        params["isLoggedIn"] = True
        return render_template("viewSessions.html", **params)
    else:
        flash("Please log in to view sessions.")
        return redirect(url_for('index'))


# javascript routes for async requests

@app.route("/validateUser/", methods=["POST"])
def validateUser():
    username = request.form.get("username")
    usersData = interactions.findUsersByUsername(username)
    return jsonify({"validate": len(usersData) == 1})

@app.route("/getUserClasses/", methods=["POST"])
def getUserClasses():
    username = request.form.get("username")
    userData = interactions.findUsersByUsername(username)[0]
    userCourses = interactions.findCoursesByStudent(userData["pid"])
    formattedCourses = []
    for course in userCourses:
        courseData = {
            "cid": course.get("cid"),
            "name": "{dept} {num}-{section}".format(
                dept=course.get("dept"),
                num=course.get("coursenum"),
                section=course.get("section"))
        }
        formattedCourses.append(courseData)
    sortedCourses = sorted(formattedCourses, key=lambda c: c.get("name"))
    return jsonify({"courses": sortedCourses})

@app.route("/getSessionTypes/", methods=["POST"])
def getSessionTypes():
    sessionTypes = [
        "ASC (Academic Success Coordinator)", 
        "Help Room", 
        "PLTC Assigned Tutoring",
        "Public Speaking Tutoring",
        "SI (Supplemental Instruction)"
    ]
    return jsonify({"types": sessionTypes})

