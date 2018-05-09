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
from flask_cas import CAS

CAS(app)
app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_AFTER_LOGIN'] = 'logged_in'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
app.config['CAS_AFTER_LOGOUT'] = 'https://cs.wellesley.edu:1943/index'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'

@app.route('/logged_in/')
def logged_in():
    flash('successfully logged in!')
    return redirect(url_for('index'))

@app.route('/logged_out/')
def logged_out():
    flash('successfully logged out!')
    return redirect(url_for('index'))

@app.route("/", methods=["GET"])
@app.route("/index/", methods=["GET"])
def index():
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
        is_logged_in = True
        username = session['CAS_USERNAME']
        print('CAS_USERNAME is: ', username)
    else:
        is_logged_in = False
        username = None
        print('CAS_USERNAME is not in the session')
    params = {"title": "Home", "username": username, "is_logged_in": is_logged_in}
    return render_template("index.html", **params)

# Note: login isn't quite working yet. Will make it into P4.
'''
@app.route("/login/", methods=["GET", "POST"])
def login():
    # edit the following to make it work
    params = {"title": "Login"}
    if "userid" in session:
        flash("Already logged in!")
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        session["userid"] = 1  # fill this in
        flash("Login successful")
    return render_template("login.html", **params)
'''

@app.route("/newSession/", methods=["GET", "POST"])
def newSession():
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
            "userId": userId,
            "courseId": courseId,
            "isTutor": 'n', # update this later
            "sessiontype": sType}
        insertData = interactions.insertSession(sessionData)
        if insertData:
            flash("Tutoring session entered successfully.")
        else:
            flash("Failed to enter tutoring sessions.")
    params = {"title": "Insert a Tutoring Session"}
    return render_template("newSession.html", **params)

@app.route("/viewSessions/", methods=["GET"])
def viewSessions():
    sessions = interactions.findAllSessions2()
    params = {"title": "View Tutoring Sessions",
                "sessions": sessions}
    print sessions
    return render_template("viewSessions.html", **params)

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

