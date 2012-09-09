'''
Created on Sep 6, 2012

@author: varun
'''
import settings

from txtweb import txtWeb
import txtwebUtils
import txtwebConf

import sys
import urllib, urllib2, urlparse

def process_txtweb_request(querystring,post_url):
    try:
        txtweb_req = dict(urlparse.parse_qsl(querystring))
        print "txtWeb,App Reqt :: ",txtweb_req,"\n"
        txtWebObj = txtWeb(txtweb_req)
        
        txtWebObj.put_in_db()
                
        app_module = txtwebUtils.import_app(post_url)        
        if app_module:
            try:
                app_resp = app_module.process_in_request(txtWebObj)
            except Exception, e:
                # Send error mail
                app_resp = txtwebConf.DEF_ERR['app_err']
        else:
            # Send error mail
            app_resp = txtwebConf.DEF_ERR['app_err']
        print "App Resp :: ",app_resp,"\n"
        txtweb_out_msg = txtWebObj.format_txtweb_out(app_resp)
        txtweb_resp = txtWebObj.push_txtweb_msg(txtweb_out_msg)
        
        print "txtWeb Resp :: ",txtweb_resp,"\n"
        txtWebObj.put_out_db()
    except Exception,e:
        # Send error mail and log
        pass

if __name__ == '__main__':
    txtweb_inreq = "txtweb-message=Varun&txtweb-id=3e79bbb1-3e3c-4bbb-b867-39ed7ddf546e&txtweb-verifyid=81907f5d4295f90bf581999b7d9bcc5c0e5b8a822f1f5b02378b14e544115cd61afe8135bd8751e99c394da39c7603122e70ba54a6508ea8be94d3f2e252d6c4e643b674bea450f4bbc43adc3a8538a6dc25bd2c62343e81f2a2c1afca026997ed39ff6f765a3b5f&txtweb-mobile=72a556c2-c3fd-4a9a-aff8-922452acb335&txtweb-aggid=10000&txtweb-protocol=1000"
    process_txtweb_request(txtweb_inreq,"10.27.218.247/mymap")