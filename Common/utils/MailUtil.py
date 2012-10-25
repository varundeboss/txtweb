import os
import fcntl
import socket
import struct
import smtplib
import datetime
import commands

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate, parseaddr
from email.MIMEImage import MIMEImage
from email import Charset
Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')


#HOSTNAME = commands.getoutput("hostname")
LOGOS = {'LS' :'/public/gdp/ukl/images/logo.jpg',
         'MDL':'/public/gdp/ukl/images/mdl-logo.jpg',
         }
CID = {'LS' :'<logo.jpg>',
       'MDL':'<mdl-logo.jpg>',
       }

def dictadd(*dicts):
    """
    Returns a dictionary consisting of the keys in the argument dictionaries.
    If they share a key, the value from the last argument is used.

        >>> dictadd({1: 0, 2: 0}, {2: 1, 3: 1})
        {1: 0, 2: 1, 3: 1}
    """
    result = {}
    for dct in dicts:
        result.update(dct)
    return result

def send_mail(config, frm_addr, to_addr, Subject, text, headers = None, files=[], html_body=False, **kw):
    """
    sending a mail using and without using SSL.
    config is a dictionary that have key, value pairs to connect mail server. We can get config dictionary from UE_config file. 
    
    frm_addr - (string) id from which we send mails
    to_addr  - (string or list) all the to addresses to send mail
    kw - In keywords you can give cc and bcc also.
    headers - It will have all the extra headers to add to mail
    """
    #In headers we send type of data, cc, Subjects
    if headers is None: headers = {}
    
    #with Default settings it works without using SSL and without login.
    server = config.get('server')
    port = config.get('port', 25)
    startSSL = config.get('startSSL', False)
    startTLS = config.get('startTLS', False)
    username = config.get('username', None)
    password = config.get('password', None)
    cc = kw.get('cc', [])
    bcc = kw.get('bcc', [])

    def listify(x):
        if not isinstance(x, list):
            return [x]
        return x
   
    #Here are all the recepients. 
    cc = listify(cc)
    bcc = listify(bcc)
    to_addr = listify(to_addr)
    recipients = to_addr+cc+bcc

    frm_addr = str(frm_addr)

    files = listify(files)
    
    #Here are the headers to send message..
    if cc:
        headers['Cc'] = ", ".join(cc)
    
    headers = dictadd({
      'MIME-Version': '1.0',
      'Content-Type': 'text/plain; charset=UTF-8',
      'Content-Disposition': 'inline',
      'From': frm_addr,
      'To': ", ".join(to_addr),
      'Subject': Subject
    }, headers)

    #parsing the to and from addresses
    import email.Utils
    from_address = email.Utils.parseaddr(frm_addr)[1]
    recipients = [email.Utils.parseaddr(r)[1] for r in recipients]

    #Creating a message to send from server
    message = MIMEMultipart()
    for k, v in headers.items():
        message.add_header(k, v)

    if html_body == True:
        txt_msg = MIMEText(text,'html','UTF-8')
    else:
        txt_msg = MIMEText(text,'plain','UTF-8')
    message.attach(txt_msg)
    #message.attach(MIMEText(text))
    
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f).read()) 
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        message.attach(part)

    #making a connection with server
    if startSSL:
        con = smtplib.SMTP_SSL(server, port)
    else:
        con = smtplib.SMTP(server)
    if startTLS:
            con.starttls()

    # Logging into server 
    if username and password:
        con.login(username, password)
    
    #Now we are ready to send the data..
    con.sendmail(from_address, recipients, message.as_string())

    #Closing the connection
    con.quit()

if __name__ == "__main__":
    config = {'server': 'smtps.global-analytics.com', 'port':465, 'startSSL':True, 'username': 'leela@global-analytics.com', 'password':'gai.mail'}
    #send_mail(config, 'leela@global-analytics.com', ['leela@global-analytics.com'], '....Testing By attaching a file and some text....', '######Test######')
    send_mail(config, 'varun.r@global-analytics.com', ['varun.r@global-analytics.com'],\
              '....Testing By attaching a file and some text....', '######Test######',\
              files=[])
