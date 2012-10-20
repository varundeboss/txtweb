'''
The common module where all the utils, configs and settings that are common to all the modules are kept
'''

SVN_VERSION = "0000"
RELEASE_VERSION = "0.0.1"

import os
import sys
import time
import socket

os.environ['TXTWEB_HOSTNAME'] = 'dev' #dev | prod 

PROJECT = "Common"
project_dir, handler = os.path.split(__file__)
PROJECT_PATH = project_dir.replace(PROJECT,'')

PROJECT_LIST = ["libs","Apps","Smsout"]
PROJECT_LIST.append(PROJECT)

sys.path.append(PROJECT_PATH)
for PROJ in PROJECT_LIST:
    sys.path.append(os.path.join(PROJECT_PATH, PROJ))


# Setting python egg cache and timezone
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
os.environ['TZ'] = "Asia/Kolkata"
time.tzset()

HOSTNAME = socket.gethostname()
