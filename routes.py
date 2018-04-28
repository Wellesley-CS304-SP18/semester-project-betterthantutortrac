"""
filename: routes.py
author: Angelina Li, 
last modified: 04/28/2018
description: routes for app
"""

from flask import render_template

from app import app

@app.route("/", methods=["GET"])
@app.route("/index/", methods=["GET"])
def index():
    params = {"title": "Home"}
    return render_template("index.html", **params)

@app.route("/test/", methods=["GET"])
def test():
    params = {"title": "Test"}
    return render_template("test.html", **params)
