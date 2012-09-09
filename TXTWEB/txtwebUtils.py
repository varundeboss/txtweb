'''
Created on Sep 8, 2012

@author: varun
'''

import txtwebConf
#from importlib import import_module

import os

def import_app(post_url):
    try:
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
    except Exception,e:
        # Send error mail
        app_import = False
    
    return app_import
        