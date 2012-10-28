'''
The common module where all the utils, configs and settings that are common to all the modules are kept
'''

SVN_VERSION = "0000"
RELEASE_VERSION = "0.0.1"

import os
import sys
import time
import socket

#os.environ['TXTWEB_HOSTNAME'] = 'dev' #dev | prod 
TXTWEB_HOSTNAME = 'dev' # dev | prod 
TXTWEB_MYSQL    = 'dev' # dev | freemysql

PROJECT = "Common"

project_dir = os.path.abspath(__file__)
PROJECT_PATH = project_dir.replace(PROJECT+"/"+__file__.split("/")[-1],'')
#project_dir, handler = os.path.split(__file__)
#PROJECT_PATH = project_dir.replace(PROJECT,'')

PROJECT_LIST = ["libs","Apps","Smsout"]
PROJECT_LIST.append(PROJECT)

sys.path.append(PROJECT_PATH)
for PROJ in PROJECT_LIST:
    sys.path.append(os.path.join(PROJECT_PATH, PROJ))


# Setting python egg cache and timezone
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
os.environ['TZ'] = "Asia/Kolkata"
time.tzset()

#HOSTNAME = socket.gethostname()
