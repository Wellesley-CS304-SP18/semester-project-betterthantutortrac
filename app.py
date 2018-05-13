"""
filename: app.py
authors: Angelina Li, Kate Kenneally
last modified: 05/13/2018
description: main module that will run app
"""

import os
from flask import Flask
from flask_cas import CAS

app = Flask(__name__)

# CAS configuration
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
    systemPort = os.getuid()
    availablePorts = {
        6251: 1943, 
        6352: 1944, 
        7277: 1948
    }
    # use unique port for each person
    # needed for CAS (1942 is scott's, 1943 and up is fine, stay in range of 1940s)
    port = availablePorts[systemPort] 
    app.run("0.0.0.0", port)
    print " * Key: " + app.secret_key  # print for debugging purposes
