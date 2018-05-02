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
from program import get_random_key

app.secret_key = get_random_key()

if __name__ == "__main__":
    print " * Key: " + app.secret_key  # print for debugging purposes
    app.debug = True
    app.run()
