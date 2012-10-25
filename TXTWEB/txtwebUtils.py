'''
Created on Sep 8, 2012

@author: varun
'''

import txtwebConf
#from importlib import import_module

from Common.utils.db.db_conn import get_db

import os

def import_app(txtweb_msg):
    try:
        '''
        app = txtwebConf.URL_APP_MAP.get(os.environ['TXTWEB_HOSTNAME'],{}).get(post_url,'').lower()
        if app:
            app_module = app + "." + app + "_handler"
            #app_import = import_module(app_module)
            par_app_import = __import__(app_module)
            child_app_str = str(app) + "_handler" 
            app_import = getattr(par_app_import, child_app_str)
        else:
            # Send error mail
            app_import = False
        '''
        if txtweb_msg and txtweb_msg.split(' ')[0].upper() in txtwebConf.KEY_APP_MAP.keys():
            mod_dict = txtwebConf.KEY_APP_MAP[txtweb_msg.split(' ')[0].upper()]
            return getattr(__import__(mod_dict['mod'], fromlist=['']), mod_dict['func'])
        else:
            return False
    except Exception,e:
        # Send error mail
        return False
    
def check_auth(txtwebObj):
    try:
        data = get_db('TXW').query("show databases;").list()
    except Exception,e:
        pass
