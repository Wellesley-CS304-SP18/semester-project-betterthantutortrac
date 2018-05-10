"""
filename: app.py
authors: Angelina Li,
last modified: 04/28/2018
description: main module that will run app
"""

import os
from flask import Flask

app = Flask(__name__)

# placed after defining app to prevent circular dependencies
from routes import *

app.secret_key = "secretKey123"

if __name__ == "__main__":
    app.debug = True
    # port = os.getuid()
    port = 1943
    app.run("0.0.0.0", port)
    print " * Key: " + app.secret_key  # print for debugging purposes
