import webapp2
from google.appengine.api import rdbms

import urllib

import sys
import os

project_dir, handler = os.path.split(__file__)
sys.path.append(project_dir)

import Common

from TXTWEB.txtweb_handler import process_txtweb_request

class MainPage(webapp2.RequestHandler):
    #import pdb;pdb.set_trace()
    #conn = rdbms.connect(instance='varunthyboss:varunthyboss', database='TXTWEB', **{'user':'varundeboss', 'password':'vArundebo0s', 'charset':'utf8'})
    def get(self):
        request = urllib.urlencode(getattr(self.request,self.request.method))
        print request
        response = process_txtweb_request(request)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(response)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
