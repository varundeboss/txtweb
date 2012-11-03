'''
Created on Sep 8, 2012

@author: varun
'''

import txtwebConf
#from importlib import import_module

from Common.utils.db.db_conn import get_db
from Common.utils.MailUtil import send_mail

from Common.config.MailConf import mail_config

import os
import random
from optparse import OptionParser
from datetime import datetime
import traceback

_logdata  = None
_userdata = None
_lastdata = None

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

def check_expiry(log_info):
    now  = datetime.now().replace(microsecond=0)
    then = log_info['LoggedOn']
    #then = datetime.strptime(log_info['LoggedOn'],'%Y-%m-%d %H-%M-%S')
    session = int(log_info['LogValidity'])
    diff = now - then
    return ((diff.seconds/60) + (diff.days*24*60)) < session

def check_credentials(cust_info, txtwebObj):
    msg_list = txtwebObj.txtweb_msg.split(' ')
    if len(msg_list) > 2:
        return msg_list[1] == cust_info['Username'] and msg_list[2] == cust_info['Password']
    return False

def gen_user_id():
    while 1:
        userid = random.randrange(100000,1000000)
        userid_info = get_db('TXW').query("select * from cust_account where UserID='%(userid)s'"%{'userid':userid}).list()
        if not userid_info:
            return userid

def gen_verify_id():
    return random.randrange(100000,1000000)

def send_verify_id(firstname,email,verify_id,username):
    try:
        subject = "%(keyword)s verification code"%{'keyword':txtwebConf.TXTWEB_KEYWORD.upper()}
        body = "Greetings %(firstname)s,\n\n\tThank you for choosing %(keyword)s.\n\n\tTo verify your account please send @%(keyword)s ver [username] [password] %(verifyid)s"%{'firstname':firstname, 'keyword':txtwebConf.TXTWEB_KEYWORD.upper(), 'verifyid':verify_id}
        send_mail(mail_config, txtwebConf.FROM_EMAIL, [email], subject, body,files=[])
        get_db('TXW').update("cust_account", vars={'Username':username},where="Username=$Username",**{'EmailFlag':1})
        print "Verification code ",verify_id," sent to email ",email," successfully"
    except:
        print "Verification code ",verify_id," sent to email ",email," failed"

def login(username,mobile,session):
    try:
        login_dict = {
                        "LogFlag"     : "1",
                        "LoggedOn"    : datetime.now(),
                        "LogValidity" : session,
                        "LastMobile"  : mobile,
                        "UpdatedOn"   : datetime.now(),
                     }
        get_db('TXW').update("cust_account", vars={'Username':username},where="Username=$Username",**login_dict)
        return False, txtwebConf.AUTH_ERR['LIN_SUC'] + txtwebConf.AUTH_ERR['WELCOME'] # Logged in successfully. Send welcome tmpl
    except:
        return False, txtwebConf.AUTH_ERR['LIN_FAIL'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Problem while logging in. Send login tmpl

def logout(username):
    try:
        logout_dict = {
                        "LogFlag" : "0", 
                      }
        get_db('TXW').update("cust_account", vars={'Username':username},where="Username=$Username",**logout_dict)
        print "Logged out successfully"
        return False, txtwebConf.AUTH_ERR['LOUT_SUC'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Logged out successfully. Send login tmpl
    except:
        return False, txtwebConf.AUTH_ERR['LOUT_FAIL'] + txtwebConf.AUTH_ERR['LOUT_TMPL'] # Problem while logging out. Send logout tmpl

def register(txtwebObj):
    global _userdata
    try:
        usage = "reg -u [username] -p [password] -f [firstname] -l [lastname] -e [email] -s [sex] -a [age] -c [city] -d [dob] -t[session]"
        parser = OptionParser(usage=usage, version="%prog 1.0")
        parser.add_option("-u", "", action="store", type="string", dest="username", help="")
        parser.add_option("-p", "", action="store", type="string", dest="password", help="")
        parser.add_option("-f", "", action="store", type="string", dest="firstname", help="")
        parser.add_option("-l", "", action="store", type="string", dest="lastname", help="")
        parser.add_option("-e", "", action="store", type="string", dest="email", help="")
        parser.add_option("-s", "", action="store", type="string", dest="sex", help="")
        parser.add_option("-a", "", action="store", type="string", dest="age", help="")
        parser.add_option("-c", "", action="store", type="string", dest="city", help="")
        parser.add_option("-d", "", action="store", type="string", dest="dob", help="")
        parser.add_option("-t", "", action="store", type="string", dest="session", help="")
        options, args = parser.parse_args(txtwebObj.txtweb_msg.split(' '))
       
        if not _userdata:
            user_det = get_db('TXW').select("cust_account", vars={'Username':options.username},where="Username=$Username").list()
        else:
            user_det = _userdata

        if user_det:
            return False, txtwebConf.AUTH_ERR['USER_EXIST'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Username already exist. Send registration tmpl

        for field in txtwebConf.MAND_REGISTER:
            if not getattr(options,field):
                return False, txtwebConf.AUTH_ERR['REG_MAND'] + txtwebConf.AUTH_ERR['REG_TMPL'] # One of the mandatory field is missing. Send registration tmpl

        try:session = int(options.session)
        except:session = txtwebConf.SESSION_TIME
        
        verify_id = gen_verify_id()

        register_dict = {
                            "Username" : options.username,
                            "Password" : options.password,
                            "Firstname" : options.firstname,
                            "Lastname" : options.lastname,
                            "Email" : options.email,
                            "Sex" : options.sex[0].upper(),
                            "Age" : options.age,
                            "City" : options.city,
                            "DOB" : options.dob,
                            "LogValidity" : session,
                            "UserID" : gen_user_id(),
                            "Mobile" : txtwebObj.txtweb_mobile,
                            "LastMobile" : txtwebObj.txtweb_mobile,
                            "LogFlag" : "1",
                            "LoggedOn" : datetime.now(),
                            "VerifyID" : verify_id,
                        }
        get_db('TXW').insert("cust_account",**register_dict)
        #Send verification ID in registered email
        send_verify_id(options.firstname, options.email, verify_id, options.username)
        return False, txtwebConf.AUTH_ERR['REG_SUC'] + txtwebConf.AUTH_ERR['VER_SENT']%{'email':options.email} # Registered successfully. Tell to verify
    except Exception,e:
        return False, txtwebConf.AUTH_ERR['REG_FAIL'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Problem while registering. Send registration tmpl

def update_details(txtwebObj,log_info):
    global _userdata
    try:
        usage = "set -f [firstname] -l [lastname]-e [email] -s [sex] -a [age] -c [city] -d [dob]"
        parser = OptionParser(usage=usage, version="%prog 1.0")
        parser.add_option("-f", "", action="store", type="string", dest="firstname", help="")
        parser.add_option("-l", "", action="store", type="string", dest="lastname", help="")
        parser.add_option("-e", "", action="store", type="string", dest="email", help="")
        parser.add_option("-s", "", action="store", type="string", dest="sex", help="")
        parser.add_option("-a", "", action="store", type="string", dest="age", help="")
        parser.add_option("-c", "", action="store", type="string", dest="city", help="")
        parser.add_option("-d", "", action="store", type="string", dest="dob", help="")
        options, args = parser.parse_args(txtwebObj.txtweb_msg.split(' '))

        update_dict = {}
        op_dict = options.__dict__
        for field in op_dict:
            if op_dict[field]:
                update_dict[field] =  op_dict[field]

        if not op_dict or not update_dict:
            return False, txtwebConf.AUTH_ERR['UP_NTNG'] + txtwebConf.AUTH_ERR['UP_TMPL'] # Nothing given to update. Send update tmpl.

        if not _userdata:
            user_det = get_db('TXW').select("cust_account", vars={'Username':log_info['Username']},where="Username=$Username").list()
        else:
            user_det = _userdata

        if options.email and options.email != user_det[0]['Email']:
            verify_id = gen_verify_id()
            update_dict.update({"VerifyID":verify_id, "UpdatedOn":datetime.now()})

        up_flag = get_db('TXW').update("cust_account", vars={'Username':log_info['Username']},where="Username=$Username",**update_dict)
        if up_flag:
            if options.email and options.email != user_det[0]['Email']:
                #Send verification ID in registered email
                send_verify_id(log_info['Firstname'], options.email, verify_id, log_info['Username'])
                logout(log_info['Username'])
                get_db('TXW').update("cust_account", vars={'Username':log_info['Username']},where="Username=$Username",**{'VerifyFlag':'0',"UpdatedOn":datetime.now()})
                return False, txtwebConf.AUTH_ERR['UP_SUCC'] + txtwebConf.AUTH_ERR['VER_NEW']%{'email':options.email} # Account details updated successfully. Check your new emailID for verification instructions
            else:
                get_db('TXW').update("cust_account", vars={'Username':log_info['Username']},where="Username=$Username",**{"UpdatedOn":datetime.now()})
            return False, txtwebConf.AUTH_ERR['UP_SUCC'] + txtwebConf.AUTH_ERR['WELCOME'] # Account details updated successfully. Send welcome tmpl
        else:
            return False, txtwebConf.AUTH_ERR['UP_SAME'] + txtwebConf.AUTH_ERR['WELCOME'] # Same account details sent. Nothing to update. Send welcome tmpl

    except Exception,e:
        print  traceback.print_exc()
        return False, txtwebConf.AUTH_ERR['UP_FAIL'] + txtwebConf.AUTH_ERR['UP_TMPL'] # Error while updating details. Send update tmpl

def get_details(txtwebObj,log_info):
    return False, txtwebConf.AUTH_ERR['GET_TMPL']%{'Firstname':log_info['Firstname'],'Lastname':log_info['Lastname'],'Email':log_info['Email'],'Sex':log_info['Sex'],'Age':log_info['Age'],'DOB':log_info['DOB'],'City':log_info['City']} + txtwebConf.AUTH_ERR['UP_TMPL']

def verify_account(log_info,txtwebObj):
    try:
        msg_list = txtwebObj.txtweb_msg.split(' ')
        if len(msg_list) < 4:
            return False, txtwebConf.AUTH_ERR['VER_MISS'] + txtwebConf.AUTH_ERR['VER_TMPL'] # VerifyID missing. Send ver tmpl

        verify_id = msg_list[3]
        if str(log_info['VerifyID']) == verify_id:
            get_db('TXW').update("cust_account", vars={'Username':log_info['Username']},where="Username=$Username",**{'VerifyFlag':'1','UpdatedOn':datetime.now()})
            return False, txtwebConf.AUTH_ERR['VER_SUC'] + txtwebConf.AUTH_ERR['WELCOME'] # Verified successfully. Send welcome tmpl
        return False, txtwebConf.AUTH_ERR['VER_WRNG']%{'email':log_info['Email']} # Verifyid wrong. Check email for correct ID
    except Exception,e:
        return False, txtwebConf.AUTH_ERR['VER_FAIL'] + txtwebConf.AUTH_ERR['VER_TMPL'] # Error while verifying account. Send verify tmpl

def update_obj_account(txtwebObj,log_info):
    cust_dict = {}
    for field in txtwebConf.APP_CUST_LIST:
        if field in log_info.keys():
            cust_dict[field] = log_info[field]
    txtwebObj.cust_account = cust_dict
    txtwebObj.keyword = txtwebConf.TXTWEB_KEYWORD

def check_auth(txtwebObj):
    global _userdata
    try:
        if not _userdata:
            cust_info = get_db('TXW').select("cust_account", vars={'Mobile':txtwebObj.txtweb_mobile}, where="Mobile=$Mobile").list()
        else:
            cust_info = _userdata

        log_info  = get_db('TXW').select("cust_account", vars={'Mobile':txtwebObj.txtweb_mobile}, where="LastMobile=$Mobile").list()
        app_name = txtwebObj.txtweb_msg.split(' ')[0].upper()

        # Register the account if not already and send the verification ID to registered EmailID or ask to login using credentials.
        if app_name == "REG":
            if cust_info:
                return False, txtwebConf.AUTH_ERR['REG_DONE'] + txtwebConf.AUTH_ERR['UP_TMPL'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Already registered.Send tmpl for login and update
            else:
                # Register and send verification ID to EmailID
                return register(txtwebObj)
        
        # Update the account by checking if exists, VerifyFlag and LogFlag,LogValidity and if new EmailID is given verify it again and LogOut.
        if app_name in ["SET", "GET"]:
            if not log_info:
                if not cust_info:
                    return False, txtwebConf.AUTH_ERR['REG_NOT'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Not registered. Send tmpl for registration
                return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not Loggedin.Send tmpl for login

            if not log_info[0]['VerifyFlag']:
                return False, txtwebConf.AUTH_ERR['VER_NOT']%{'email':log_info[0]['Email']} # Not verified. please verify

            if not int(log_info[0]['LogFlag']):
                return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not logged in. Send login tmpl

            if not check_expiry(log_info[0]):
                return False, txtwebConf.AUTH_ERR['LIN_EXP'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Expired. Please login by sending tmpl
            
            if app_name == "SET":
                # Update details    
                return update_details(txtwebObj,log_info[0])

            if app_name == "GET":
                # Get account details
                return get_details(txtwebObj,log_info[0])
        
        # Login by checking if exists, Credentials and then VerifyFlag else return corresponding error messages
        if app_name == "LOGIN":
            msg_list = txtwebObj.txtweb_msg.split(' ')
            if len(msg_list) > 1:
                username = msg_list[1] 
            else:
                return False, txtwebConf.AUTH_ERR['CRED_MISS'] + txtwebConf.AUTH_ERR['LIN_TMPL'] #Username and password missing. Send login tmpl

            if not _userdata:
                user_info  = get_db('TXW').select("cust_account", vars={'Username':username}, where="Username=$Username").list()
            else:
                user_info = _userdata

            if not user_info:
                return False, txtwebConf.AUTH_ERR['USER_MISS'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Username not found. Send tmpl for registration

            if not check_credentials(user_info[0],txtwebObj):
                return False, txtwebConf.AUTH_ERR['CRED_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Credentials wrong. Send tmpl to login

            if not user_info[0]['VerifyFlag']:
                return False, txtwebConf.AUTH_ERR['VER_NOT']%{'email':user_info[0]['Email']} # Not verified. please verify 

            if len(msg_list) > 3:
                try:session = int(msg_list[3])
                except:session = txtwebConf.SESSION_TIME
            else:
                session = txtwebConf.SESSION_TIME

            # Login
            return login(username,txtwebObj.txtweb_mobile,session)

        # Logout by checking if exists, Credentials and LogFlag else return corresponding error messages
        if app_name == "LOGOUT":
            if not log_info:
                if not cust_info:
                    return False, txtwebConf.AUTH_ERR['REG_NOT'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Not registered. Send tmpl for registration
                return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not Loggedin.Send tmpl for login

            if not check_credentials(log_info[0],txtwebObj):
                return False, txtwebConf.AUTH_ERR['CRED_NOT'] + txtwebConf.AUTH_ERR['LOUT_TMPL'] # Credentials wrong. Send tmpl to logout

            #if not log_info[0]['LogFlag']:
            #    return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not Loggedin. Send tmpl for login

            # Logout
            return logout(log_info[0]['Username'])

        if app_name == "VER":
            if not log_info:
                if not cust_info:
                    return False, txtwebConf.AUTH_ERR['REG_NOT'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Not registered. Send tmpl for registration
                return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not Loggedin.Send tmpl for login

            if log_info[0]['VerifyFlag']:
                return False, txtwebConf.AUTH_ERR['VER_ALDY'] + txtwebConf.AUTH_ERR['WELCOME'] # Already verified. Send welcome tmpl

            if not check_credentials(log_info[0],txtwebObj):
                return False, txtwebConf.AUTH_ERR['CRED_NOT'] # Credentials wrong.

            # Verify
            return verify_account(log_info[0],txtwebObj)

        # Check if AppName is available else send available appname message.
        if app_name in txtwebConf.KEY_APP_MAP.keys():
            # If APP doesn't need user to be loggedin then don't authenticate and don't send any userdetails related to the mobile to the APP
            if not txtwebConf.KEY_APP_MAP[app_name]['LogFlag']:
                return True, "Authenticated"
        else:
            return False, txtwebConf.AUTH_ERR['WELCOME'] # Send welcome tmpl

        if not log_info:
            if not cust_info:
                return False, txtwebConf.AUTH_ERR['REG_NOT'] + txtwebConf.AUTH_ERR['REG_TMPL'] # Not Registered. Send Registration tmpl
            return False, txtwebConf.AUTH_ERR['LIN_NOT'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Not logged in. Send logging tmpl
        
        # Check VerifyFlag and LogFlag,LogValidity and logout if LogFlag=1 and LogValidity expired else autheticate
        if not log_info[0]['VerifyFlag']:
            return False, txtwebConf.AUTH_ERR['VER_NOT']%{'email':log_info[0]['Email']} # Not verified. Pls verify
        
        if log_info[0]['LogFlag']:
            if check_expiry(log_info[0]):
                update_obj_account(txtwebObj,log_info[0])
                return True, "Authenticated"
            else:
                return False, txtwebConf.AUTH_ERR['LIN_EXP'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # Session expired. Send login tmpl
        else:
            return False, txtwebConf.AUTH_ERR['LOUT_SUC'] + txtwebConf.AUTH_ERR['LIN_TMPL'] # You are logged out. Send login tmpl
    except Exception,e:
        print  traceback.print_exc()
        return False, txtwebConf.DEF_ERR['app_err']
