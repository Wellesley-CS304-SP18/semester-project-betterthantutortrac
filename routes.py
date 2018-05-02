"""
filename: routes.py
author: Angelina Li, 
last modified: 04/28/2018
description: routes for app
"""

import interactions
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

@app.route("/new_session/", methods=["GET", "POST"])
def new_session():
    if request.method == "POST":
        username = request.form.get("username")
        course = request.form.get("class")
        s_type = request.form.get("type")
        begin_time = str(datetime.now())
        end_time = str(datetime.now()) # need to update this
        interactions.insertSession(username, course, s_type, begin_time, end_time)
        flash("Tutoring session entered successfully.")
    params = {"title": "Insert a Tutoring Session"}
    return render_template("tutor_session.html", **params)

@app.route("/view_sessions/", methods=["GET"])
def view_sessions():
    params = {"title": "View Tutoring Sessions"}
    return render_template("view_sessions.html", **params)

@app.route("/test/", methods=["GET"])
def test():
    params = {"title": "Test"}
    return render_template("test.html", **params)
