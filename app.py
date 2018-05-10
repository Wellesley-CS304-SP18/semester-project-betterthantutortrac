"""
filename: app.py
authors: Angelina Li,
last modified: 04/28/2018
description: main module that will run app
"""

import os
from flask import Flask
from flask_cas import CAS

app = Flask(__name__)

CAS(app)
app.config["CAS_SERVER"] = "https://login.wellesley.edu:443"
app.config["CAS_AFTER_LOGIN"] = "logged_in"
app.config["CAS_LOGIN_ROUTE"] = "/module.php/casserver/cas.php/login"
app.config["CAS_LOGOUT_ROUTE"] = "/module.php/casserver/cas.php/logout"
app.config["CAS_AFTER_LOGOUT"] = "https://cs.wellesley.edu:1943/index"
app.config["CAS_VALIDATE_ROUTE"] = "/module.php/casserver/serviceValidate.php"

# placed after defining app to prevent circular dependencies
from routes import *

app.secret_key = "secretKey123"

if __name__ == "__main__":
    app.debug = True
    # port = os.getuid()
    port = 1943
    app.run("0.0.0.0", port)
    print " * Key: " + app.secret_key  # print for debugging purposes
