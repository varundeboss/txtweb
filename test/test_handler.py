'''
Created on Sep 5, 2012

@author: varun
'''

import urllib, urllib2, urlparse
from bs4 import BeautifulSoup

URL_MAP = {
            'SET_USER_LOC' : {
                              'URL':'http://api.txtweb.com/v1/location/set',
                              'REQ_PARAMS':['txtweb-location','txtweb-appurl','txtweb-appname'],
                              'RES_CODE':['code','message'],
                              'SUC_RES_PARAMS':['location','default','userlocationtext','city','province','country','postalcode'],
                              'ERR_RES_PARAMS':[],
                              'ERR_CODE_MAP':{
                                              '-101':'No such mobile',
                                              '-3':'Invalid input',
                                             },
                              'METHOD':'POST',
                             },
            'GET_USER_LOC' : {
                              'URL':'http://api.txtweb.com/v1/location/get',
                              'REQ_PARAMS':['txtweb-mobile'],
                              'RES_CODE':['code','message'],
                              'SUC_RES_PARAMS':['location','default','userlocationtext','city','province','country','postalcode'],
                              'ERR_RES_PARAMS':[],
                              'ERR_CODE_MAP':{
                                              '-101':'No such mobile',
                                              '-3':'Invalid input',
                                             },
                              'METHOD':'GET',
                             },
           'VERIFY_MSG_SOURCE' : {
                              'URL':'http://api.txtweb.com/v3/verify',
                              'REQ_PARAMS':['txtweb-verifyid','txtweb-message','txtweb-mobile','txtweb-protocol'],
                              'RES_CODE':['code','message'],
                              'SUC_RES_PARAMS':['url'],
                              'ERR_RES_PARAMS':[],
                              'ERR_CODE_MAP':{
                                              '-200':'Invalid verify ID',
                                              '-3':'Invalid input',
                                              '-201':'Verification period has expired',
                                             },
                              'METHOD':'GET',
                             },
           'PUSH_USER_MSG' : {
                              'URL':'http://api.txtweb.com/v1/push',
                              'REQ_PARAMS':['txtweb-mobile','txtweb-message','txtweb-pubkey'],
                              'RES_CODE':['code','message'],
                              'SUC_RES_PARAMS':[],
                              'ERR_RES_PARAMS':[],
                              'ERR_CODE_MAP':{
                                              '-1':'Unknown Exception(Usually Server side). Have a retry logic in place to call the API again in case such an error code is received or wait till the APIs are back to being functional.',
                                              '-3':'Invalid input. Incorrect format for calling the API. Check the right syntax for making the API call',
                                              '-101':'No such mobile. Mobile number does not exist',
                                              '-103':'MAX Publisher Allocation exceeded. No more than 250 messages per 5 minutes per mobile number. No more than 20 messages per 10 seconds per mobile number',
                                              '-104':'Number registered with NCPR',
                                              '-300':'Missing publisher key. Get your publisher key under "Build and Manage my apps section" on txtWeb.com and include it in the parameter list of the API call',
                                              '-301':'Incorrect publisher key. Check and verify your publisher key under "Build and Manage my apps section" on txtWeb.com against the one you have sent in the API request call',
                                              '-400':'Missing application key. Get the application key of the app under "Build and Manage my apps section" on txtWeb.com and include it in the message body list of the API call',
                                              '-401':'Incorrect application key. Check and verify the application key for the app under "Build and Manage my apps section" on txtWeb.com against the one you have sent in the API request call',
                                              '-402':'Maximum Throttle exceeded. No more than 5,000 API calls in a single day',
                                              '-500':'Mobile opted out. A mobile number has opted out from receiving any message from the app',
                                              '-600':'Missing message. Check if you have included the message to be sent in the right format',
                                              '-700':'Not a sandbox user. You are trying to push through an unpublished app. You need to register the mobile number in your txtweb.com account and then try the PUSH API.',
                                             },
                              'METHOD':'POST',
                             },
          }

SERVICE_LIST = ['GET_USER_LOC', 'PUSH_USER_MSG']

DEFAULT_VALUES = {
                  'txtweb-appkey':'b8a0e901-8ef6-4beb-bb7c-90536c887b76',
                  'txtweb-mobile':'72a556c2-c3fd-4a9a-aff8-922452acb335',
                  'txtweb-message-body':'Hello World',
                  'txtweb-message':"""<html><head><title> txtWeb Message </title><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><meta name='txtweb-appkey' content='%(txtweb-appkey)s' /></head><body>%(txtweb-message-body)s</body></html>""",
                  'txtweb-pubkey':'c5d909c0-9fba-4a27-8250-589bd55bcd13',
                  'txtweb-location':'Enter location : ',
                  'txtweb-appurl':'http://10.27.218.247/',
                  'txtweb-appname':'TestApp',
                  'txtweb-verifyid':'123456',
                  'txtweb-protocol':'1000',
                 }

def txtweb_handler(request):
    print dict(urlparse.parse_qsl(request))
    return "SUCCESS"

if __name__ == '__main__':
    service_name = 'PUSH_USER_MSG' # 'PUSH_USER_MSG' 'GET_USER_LOC' 'VERIFY_MSG_SOURCE' 'SET_USER_LOC'  
    service_dict = URL_MAP[service_name]
    params = {}
    for param in service_dict['REQ_PARAMS']:
        params[param] = DEFAULT_VALUES[param]%{'txtweb-appkey':DEFAULT_VALUES['txtweb-appkey'], 'txtweb-message-body':DEFAULT_VALUES['txtweb-message-body']}
        
    txtweb_reqt = urllib.urlencode(params)
    import pdb;pdb.set_trace()
    if service_dict['METHOD'] == 'GET':
        try:
            txtweb_resp = urllib2.urlopen(str(service_dict['URL']) + "?" + str(txtweb_reqt)).read()
        except:
            txtweb_resp = urllib2.urlopen(str(service_dict['URL']), txtweb_reqt).read()
    elif service_dict['METHOD'] == 'POST':
        try:
            txtweb_resp = urllib2.urlopen(str(service_dict['URL']), txtweb_reqt).read()
        except:
            txtweb_resp = urllib2.urlopen(str(service_dict['URL']) + "?" + str(txtweb_reqt)).read()
    soap = BeautifulSoup(txtweb_resp)
    print soap
    
    code = soap.find('code').text
    message = soap.find('message').text
    if str(code) == '0' and str(message) == 'success':
        print message
    else:
        print 'error : ',message