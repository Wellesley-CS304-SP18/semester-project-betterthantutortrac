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

@app.route("/", methods=["GET"])
@app.route("/index/", methods=["GET"])
def index():
    params = {"title": "Home"}
    return render_template("index.html", **params)

# Note: login isn't quite working yet. Will make it into P4.
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

