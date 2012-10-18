'''
Created on Sep 6, 2012

@author: varun
'''

import txtwebConf
import urllib, urllib2, urlparse

try:
    import bs4
except ImportError:
    from libs import bs4
    
from Common.utils.db.db_conn import get_db

class txtWeb():
    '''
    txtWeb class that initiates and provides the services related to txtWeb
    '''
    def __init__(self,txtweb_req):
        '''        
        '''
        self.txtweb_req       = txtweb_req
        self.txtweb_id        = self.txtweb_req['txtweb-id']
        self.txtweb_vid       = self.txtweb_req['txtweb-verifyid']
        self.txtweb_mobile    = self.txtweb_req.get('txtweb-mobile','')
        self.txtweb_msg       = self.txtweb_req['txtweb-message']
        self.txtweb_protocol  = self.txtweb_req['txtweb-protocol']
        self.txtweb_pubkey    = txtwebConf.TXTWEB_PARAMS['pub_key']
        self.txtweb_appkey    = txtwebConf.TXTWEB_PARAMS['app_key']
    
    def put_in_db(self):
        try:
            pass
        except Exception, e:
            # Send error mail and log
            pass
    
    def put_out_db(self):
        # self.txtweb_out_resp_dict
        try:
            pass
        except Exception, e:
            # Send error mail and log
            pass
    
    def format_txtweb_resp(self, txtweb_out_resp):
        try:
            soup = bs4.BeautifulSoup(str(txtweb_out_resp))
            txtweb_out_resp_dict = {'code' : soup.code.string, 'message' : soup.message.string}
        except Exception, e:
            txtweb_out_resp_dict = {'code' : txtweb_out_resp, 'message' : txtweb_out_resp}
        
        return txtweb_out_resp_dict
    
    def format_txtweb_out(self, app_resp):
        out_msg_fmt = txtwebConf.TXTWEB_OUT_MSG
        fmt_dict = {
                    "txtweb-appkey" : self.txtweb_appkey,
                    "txtweb-message-body" : app_resp,  
                   }
        txtweb_out_msg = out_msg_fmt%fmt_dict
        return txtweb_out_msg
    
    def call_txtweb_service(self, txtweb_out_enc, url, method):
        try:
            if method == 'GET':
                try:
                    txtweb_out_resp = urllib2.urlopen(str(url) + "?" + str(txtweb_out_enc)).read()
                except:
                    txtweb_out_resp = urllib2.urlopen(str(url), txtweb_out_enc).read()
            elif method == 'POST':
                try:
                    txtweb_out_resp = urllib2.urlopen(str(url), txtweb_out_enc).read()
                except:
                    txtweb_out_resp = urllib2.urlopen(str(url) + "?" + str(txtweb_out_enc)).read()
        except Exception,e:
            # Send error mail
            txtweb_out_resp = txtwebConf.DEF_ERR['txtweb_url_err']
        return txtweb_out_resp
    
    def get_user_loc(self):
        pass
    
    def set_user_loc(self):
        pass
    
    def verify_txtweb_msg(self):
        pass
    
    def push_txtweb_msg(self, app_resp):
        service_dict = txtwebConf.TXTWEB_URL_MAP['PUSH_USER_MSG']
        txtweb_out = {
                        "txtweb-mobile" : self.txtweb_mobile, 
                        "txtweb-message" : app_resp,
                        "txtweb-pubkey" : self.txtweb_pubkey, 
                     }
        txtweb_out_enc = urllib.urlencode(txtweb_out)
        txtweb_out_resp = self.call_txtweb_service(txtweb_out_enc, service_dict['URL'], service_dict['METHOD'])
        
        self.txtweb_out_resp_dict = self.format_txtweb_resp(txtweb_out_resp)
        return self.txtweb_out_resp_dict
        
        
        
if __name__ == "__main__":
    pass
        
