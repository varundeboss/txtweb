'''
Created on Sep 6, 2012

@author: varun
'''

import os
import sys

PROJECT = "Smsout" 

project_dir = os.path.abspath(__file__)
PROJECT_PATH = project_dir.replace(PROJECT+"/"+__file__.split("/")[-1],'')
#project_dir, handler = os.path.split(__file__)
#PROJECT_PATH = project_dir.replace(PROJECT,'')

sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, PROJECT))
sys.path.append(os.path.join(PROJECT_PATH, 'Apps'))

import Common
