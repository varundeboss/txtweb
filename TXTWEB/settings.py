'''
Created on Sep 6, 2012

@author: varun
'''

import os
import sys

PROJECT = "TXTWEB" 
project_dir, handler = os.path.split(__file__)

PROJECT_PATH = project_di.replace(PROJECT,'')

sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, PROJECT))
sys.path.append(os.path.join(PROJECT_PATH, 'Apps'))

import Common
