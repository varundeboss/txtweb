'''
Created on Aug 26, 2012

@author: VARUN
'''
#!/usr/bin/env python 

import sys
import time
try:
    import mechanize
except ImportError:
    print "Please install mechanize module for python"
    print "Install python-mechanize, if you are on a Ubuntu/Debian machine"
    sys.exit(1)
try:
    from optparse import OptionParser
except ImportError:
    print "Error importing optparse module"
    sys.exit(1)

def SendSMS(mobile,text):
    print ">>> initializing.."
    br = mechanize.Browser()
    print ">>> connecting to way2sms..."
    try:
        br.open("http://site3.way2sms.com/entry.jsp")
        br.select_form(name="loginform")
        br["username"] = "111"  #YOUR MOBILE NUMBER HERE
        br["password"] = "111"  #YOUR PASSWORD HERE
        br.form.method="POST"
        br.form.action="http://site1.way2sms.com/Login1.action"
        print ">>> " + br.title()
        response = br.submit()
        response.get_data()
        print ">>> logged in.."
    except:
        print ">>> FATAL: Error occured while login process!"
        sys.exit(1)
    try:
        print ">>> sending message..."
        br.open("http://site1.way2sms.com/jsp/InstantSMS.jsp")
        br.select_form(name="InstantSMS")
        br["MobNo"]      = mobile
        br["textArea"]   = text
        br.form.method="POST"
        br.form.action="http://site1.way2sms.com/quicksms.action"
        response = br.submit()
        print ">>> submitting..."
        print ">>> logging out..."
        br.open("http://site1.way2sms.com/jsp/logout.jsp")
        br.close()
    except:
        print ">>> html seems to be changed!"
        print ">>> please modify the program to work with newly modified website!"
        sys.exit(1)

def main():
    PH_MAP = {'varun':'111', 'vishnu':'111'}
    parser = OptionParser()
    usage = "Usage: %prog -m [number] -t [text]"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-m", "--number",  action="store", type="string",dest="number",  help="Mobile number to send sms")
    parser.add_option("-t", "--text", action="store", type="string", dest="text", help="Text to send")
    (options, args) = parser.parse_args()
    #import pdb;pdb.set_trace()
    if options.number and options.text:
        number = PH_MAP[options.number] if options.number in PH_MAP.keys() else options.number 
        SendSMS(number,options.text)
    else:
        print "Fatal: Required arguments are missing!"
        print "Use: -h / --help to get help."

if __name__ == "__main__":
   main()