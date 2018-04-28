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

if __name__ == "__main__":
    app.debug = True
    app.run()
