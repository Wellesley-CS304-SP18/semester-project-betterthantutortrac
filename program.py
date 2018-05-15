"""
filename: program.py
last modified: 5/1/2018
author/s: Angelina Li,
description: module of helper functions to assist with main routes
"""

import random, string
import interactions
from app import app
from datetime import datetime
from flask import flash, request, redirect, url_for, session, jsonify

def logOutTutorSession(conn):
    """
    conn: A connection object to the currently used database.
    This function will check if the current tutor has logged out of a 
    tutoring session and if not, will log them out.
    Will return a boolean representing whether or not the current tutor
    has logged out.
    """
    loggedOut = True
    cookieNames = ["tid", "sid", "sessionType", "cid", "autoPopulate"]
    if "sid" in session:
        loggedOut = False
        sid = session["sid"]
        endTime = interactions.getSqlDate(datetime.now())
        update = interactions.updateSessionEndTime(conn, sid, endTime)
    for c in cookieNames:
        if c in session:
            loggedOut = False
            session.pop(c)
    return loggedOut
