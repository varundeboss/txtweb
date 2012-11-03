'''
Created on Sep 6, 2012

@author: varun
'''

WAY2SMSFLAG = False

TXTWEB_KEYWORD = "aioa"
TXTWEB_KEYWORD = TXTWEB_KEYWORD.upper()

SESSION_TIME = 720

FROM_EMAIL = 'admin@%(keyword)s.txtweb.com'%{'keyword':TXTWEB_KEYWORD}

URL_APP_MAP = {
               'dev' : {
                          "10.27.218.247/mymap" : "mymap",
                       },
               'prod' : {
                          "test.ws.zebit.com/mymap" : "mymap",
                        },
              }

# Mandatory fields for registration

MAND_REGISTER = ['username','password','email','sex','age','dob','city','firstname','lastname']

APP_CUST_LIST = ['Firstname', 'Lastname', 'Email', 'Sex', 'Age', 'DOB', 'City', 'Mobile']

# Add the project and the function handling the txtWebObj object
KEY_APP_MAP = {
                "PRL" : {'mod':"Apps.PersonalDetails.personal", 'func':"handle_personal", "desc":"Personal Details Repo", "LogFlag":True}, 
              }

APPS = ','.join(KEY_APP_MAP.keys())

TXTWEB_PARAMS = {
                    'pub_key' : 'c5d909c0-9fba-4a27-8250-589bd55bcd13',
                    'app_key' : {
                                  "MYMAP" : 'b8a0e901-8ef6-4beb-bb7c-90536c887b76', # @mymap
                                  "VARUNDEBOSS" : 'd6a6ea84-9871-4593-966e-83eec0526a3c', # @varundeboss
                                  "AIOA" : '2c35525d-30a5-4fd4-9408-fa4ac5064a20', # @aioa
                                }
                }

TXTWEB_OUT_MSG = """<html><head><title>txtWeb Message</title><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><meta name='txtweb-appkey' content='%(txtweb-appkey)s' /></head><body>%(txtweb-message-body)s</body></html>"""

AUTH_ERR = {
             "WELCOME" : "Welcome to the All-In-One App. Send @%(txtweb_key)s [appname] for usage. Available appname(s) : %(apps)s. "%{'txtweb_key':TXTWEB_KEYWORD,'apps':APPS},
             "LIN_SUC"  : "Logged in successfully. ",
             "LIN_FAIL" : "Problem while logging in. ",
             "LIN_TMPL" : "To login send @%(txtweb_key)s LOGIN [username] [password] [session time(optional) in minutes. Default is %(session)s mins]. "%{'txtweb_key':TXTWEB_KEYWORD,'session':SESSION_TIME},
             "LOUT_SUC" : "Logged out successfully. ",
             "LOUT_FAIL" : "Problem while logging out. ",
             "LOUT_NORM" : "You are logged out. ",
             "LOUT_TMPL" : "To logout send @%(txtweb_key)s logout [username] [password]. "%{'txtweb_key':TXTWEB_KEYWORD},
             "REG_MAND" : "All the fields except city and session are mandatory. ",
             "REG_TMPL" : "To register your account send @%(txtweb_key)s reg -u [username] -p [password] -f[firstname] -l [lastname] -e [email] -s [sex M/F] -a [age] -c [city] -d [dob YYYY-MM-DD] -t[session]. "%{'txtweb_key':TXTWEB_KEYWORD},
             "REG_SUC" : "Successfully registered your account. ",
             "REG_FAIL" : "Problem while registering your account. ",
             "UP_NTNG" : "No field is given for updating account. ",
             "UP_TMPL" : "To update your account details send  @%(txtweb_key)s set -f[firstname] -l [lastname] -e [email] -s [sex M/F] -a [age] -c [city] -d [dob YYYY-MM-DD]. "%{'txtweb_key':TXTWEB_KEYWORD},
             "UP_SUCC" : "Successfully updated your account details. ",
             "UP_FAIL" : "Problem while updating your account details. ",
             "UP_SAME" : "Same account details provided. Nothing to update. ",
             "REG_DONE" : "The account is already registered. ",
             "REG_NOT" : "This mobile is not registered with us yet. ",
             "VER_NOT" : "This account is not yet verified. Please check your registered email - [%(email)s] for instructions to verify. ",
             "VER_NEW" : "Please check your updated registered email - [%(email)s] for instructions to verify. ",
             "VER_SENT" : "Please check your registered email - [%(email)s] for instructions to verify. ",
             "VER_ALDY" : "This account is verified already. ",
             "VER_SUC" : "Your account is verified successfully. ",
             "VER_FAIL" : "Problem while verifying account. ",
             "VER_TMPL" : "To verify account send @%(txtweb_key)s VER [username] [password] [6 digit verifyid sent to registered email]. "%{'txtweb_key':TXTWEB_KEYWORD},
             "VER_MISS" : "Verification ID is missing. ",
             "VER_WRNG" : "Verification ID is wrong. Please check your registered email - [%(email)s] for correct verifyID",
             "LOUT_NORM" : "You are logged out. ",
             "LIN_NOT" : "You need to login to your account to access certain apps. ",
             "LIN_EXP" : "Your login session has expired. ",
             "CRED_MISS" : "We need your username and password for login. ",
             "USER_MISS" : "The username sent is invalid. ",
             "USER_EXIST" : "The username is already taken. ",
             "CRED_NOT" : "The username and password sent are not matching. ",
             "GET_TMPL" : "Your account details : \nFirstname : %(Firstname)s\nLastname : %(Lastname)s\nEmail : %(Email)s\nSex : %(Sex)s\nAge : %(Age)s\nDOB : %(DOB)s\nCity : %(City)s. ",
           }

DEF_ERR = {
            "welcome" : "Welcome to the All-In-One App. Send @%(txtweb_key)s appname for usage. Available appname(s) : %(apps)s. "%{'txtweb_key':TXTWEB_KEYWORD,'apps':APPS},
            "app_not_found" : "The App name entered is invalid. Please try one of the following appname(s): %(apps)s. "%{'apps':APPS},
            "app_err" : "Thanks for trying out our App. We are in beta mode. Please try back after sometimes. Sorry for the inconvenience caused. ",
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
