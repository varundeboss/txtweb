#!/usr/local/python2.7/bin/python
import sys
import os

project_dir, handler = os.path.split(__file__)
sys.path.append(project_dir)

import Common

from TXTWEB.txtweb_handler import process_txtweb_request
 
def handler(req, start_response):
    if req['REQUEST_METHOD'] == 'GET':
        try:
            request = req['QUERY_STRING']
            #request = req['wsgi.input'].read(int(req['CONTENT_LENGTH']))
            #post_url = req.get('SERVER_ADDR','') + req.get('REQUEST_URI','')
            print request
            response = process_txtweb_request(request)
            print response
            response_headers = [('Content-type', 'text/xml'), ('Content-Length', str(len(response)))]
            status = "200 OK"
            start_response(status, response_headers)
            return [response]
        except Exception, e:
            raise
    elif req['REQUEST_METHOD'] == 'POST':
        try:
            request = req['wsgi.input'].read(int(req['CONTENT_LENGTH']))
            #post_url = req.get('SERVER_ADDR','') + req.get('REQUEST_URI','')
            print request
            response = process_txtweb_request(request)
            print response
            response_headers = [('Content-type', 'text/xml'), ('Content-Length', str(len(response)))]
            status = "200 OK"
            start_response(status, response_headers)
            return [response]
        except Exception, e:
            raise
    else:
        response = """<html><head><title>404</title></head><body>The page you are looking for is not present on the server.</body></html>"""
        response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(response)))]
        status = "403 FORBIDDEN"
        start_response(status, response_headers)
        return [response]

application = handler
