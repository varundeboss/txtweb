import os, sys
import personal_config as perconf
from CustomError import AuthError, WelcomeError

CUR_DIR = os.path.abspath('')

class Personal:
    def __init__(self,msg):
        self.msg = msg
        self.reply = ""
        self.msg_list = self.msg.split(' ')
        try:self.keyword = self.msg_list[1]
        except:self.keyword = ""
        try:self.code = self.msg_list[2]
        except:self.code = ""
        
        auth_stat = self.auth()

        if not self.code and not self.keyword:
            self.reply = perconf.ERR_MSGS['WELCOME']
            #raise WelcomeError(self.reply)

        if auth_stat:
            self.get_details()
        
    def get_details(self):
        if self.keyword.upper() not in perconf.PERSONAL_DICT.keys():
            self.reply = perconf.ERR_MSGS['KEYERR']
        else:
            self.reply = perconf.PERSONAL_DICT[self.keyword.upper()]

    def add_details(self):
        pass

    def auth(self):
        if not self.code or not perconf.AUTH_CODE(self.code):
            self.reply = perconf.ERR_MSGS['AUTH']
            return False
        return True

def handle_personal(msg):
    PObj = Personal(msg)
    return PObj.reply


if __name__ == "__main__":
    print handle_personal('prl gaaddr a')

