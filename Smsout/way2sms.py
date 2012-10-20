'''
Created on Aug 26, 2012

@author: VARUN
'''
#!/usr/bin/env python 

import sys
import time
import settings

try:
    import mechanize
except ImportError:
    print "Please install mechanize module for python"
    print "Install python-mechanize, if you are on a Ubuntu/Debian machine"
    sys.exit(1)

class WayToSms:
    def __init__(self):
        print ">>> initializing.."
        self.br = mechanize.Browser()

    def LogIn(self):
        print ">>> connecting to way2sms..."
        try:
            self.br.open("http://site3.way2sms.com/entry.jsp")
            self.br.select_form(name="loginform")
            self.br["username"] = "8870435477"  #YOUR MOBILE NUMBER HERE
            self.br["password"] = "theboss"  #YOUR PASSWORD HERE
            self.br.form.method="POST"
            self.br.form.action="http://site1.way2sms.com/Login1.action"
            print ">>> " + self.br.title()
            response = self.br.submit()
            response.get_data()
            print ">>> logged in.."
        except:
            print ">>> FATAL: Error occured while login process!"
            sys.exit(1)

    def SendSMS(self,sms_data):
        try:
            print ">>> sending message..."
            self.br.open("http://site1.way2sms.com/jsp/InstantSMS.jsp")
            self.br.select_form(name="InstantSMS")
            self.br["MobNo"]      = sms_data['mobile']
            self.br["textArea"]   = sms_data['text']
            self.br.form.method="POST"
            self.br.form.action="http://site1.way2sms.com/quicksms.action"
            response = self.br.submit()
            print ">>> submitting..."
        except:
            print ">>> html seems to be changed!"
            print ">>> please modify the program to work with newly modified website!"
            sys.exit(1)

    def LogOut(self):
        print ">>> logging out..."
        self.br.open("http://site1.way2sms.com/jsp/logout.jsp")
        self.br.close()

def send_way2sms(sms_list):
    try:
        Obj = WayToSms()
        Obj.LogIn()
        for sms_data in sms_list:
            Obj.SendSMS(sms_data)
        Obj.LogOut
        return "SUCCESS"
    except Exception,e:
        return "Error : ",e

if __name__ == "__main__":
    sms_list = [
                {'mobile':'8870435477', 'text':'test 1'},
                {'mobile':'8870435477', 'text':'test 2'},
                {'mobile':'8870435477', 'text':'test 3'},
               ]
    print send_way2sms(sms_list)
