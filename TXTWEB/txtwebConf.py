'''
Created on Sep 6, 2012

@author: varun
'''

WAY2SMSFLAG = False

URL_APP_MAP = {
               'dev' : {
                          "10.27.218.247/mymap" : "mymap",
                       },
               'prod' : {
                          "test.ws.zebit.com/mymap" : "mymap",
                        },
              }

KEY_APP_MAP = {
                "PRL" : {'mod':"Apps.PersonalDetails.personal", 'func':"handle_personal"}, 
              }

TXTWEB_PARAMS = {
                    'pub_key' : 'c5d909c0-9fba-4a27-8250-589bd55bcd13',
                    'app_key' : 'b8a0e901-8ef6-4beb-bb7c-90536c887b76', # @mymap
                    #'app_key' : 'd6a6ea84-9871-4593-966e-83eec0526a3c', # @varundeboss
                }

TXTWEB_OUT_MSG = """<html><head><title>txtWeb Message</title><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><meta name='txtweb-appkey' content='%(txtweb-appkey)s' /></head><body>%(txtweb-message-body)s</body></html>"""

DEF_ERR = {
               "app_err" : "Thanks for trying out our App. We are in beta mode. Please try back after sometimes. Sorry for the inconvenience caused.",
               "txtweb_url_err" : """<?xml version="1.0"?><txtWeb>\n  <status>\n    <code>-999</code>\n    <message>Error while posting outbound SMS to txtweb</message>\n  </status>\n</txtWeb>\n""",               
          }

TXTWEB_URL_MAP = {
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
