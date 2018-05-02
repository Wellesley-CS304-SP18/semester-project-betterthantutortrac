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
from flask import render_template, flash, request, redirect, url_for, session

@app.route("/", methods=["GET"])
@app.route("/index/", methods=["GET"])
def index():
    params = {"title": "Home"}
    return render_template("index.html", **params)

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
        course = request.form.get("class")
        sType = request.form.get("type")
        beginTime = str(datetime.now())
        endTime = str(datetime.now()) # need to update this
        conn = dbconn2.connect(DSN)
        interactions.insertSession(conn, username, course, sType, beginTime, endTime)
        flash("Tutoring session entered successfully.")
    params = {"title": "Insert a Tutoring Session"}
    return render_template("newSession.html", **params)

@app.route("/viewSessions/", methods=["GET"])
def viewSessions():
    conn = dbconn2.connect(DSN)
    sessions = interactions.findAllSessions(conn)
    params = {"title": "View Tutoring Sessions",
                "sessions": sessions}
    return render_template("viewSessions.html", **params)
