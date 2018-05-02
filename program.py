"""
filename: program.py
last modified: 5/1/2018
author/s: Angelina Li,
description: module for main program files
"""

import random, string

def getRandomKey():
    """Returns a string of random alphanumeric chars to act as a secret key"""
    return "".join([random.choice(string.ascii_letters + 
        string.digits) for _ in xrange(25)])
