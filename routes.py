"""
filename: routes.py
author: Angelina Li, 
last modified: 04/28/2018
description: routes for app
"""

from flask import render_template, flash, request, redirect, url_for, session
from app import app

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

@app.route("/test/", methods=["GET"])
def test():
    params = {"title": "Test"}
    return render_template("test.html", **params)
