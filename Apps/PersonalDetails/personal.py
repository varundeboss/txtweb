import os, sys
import personal_config as perconf
from CustomError import AuthError, WelcomeError

CUR_DIR = os.path.abspath('')

class Personal:
    def __init__(self,msg):
        self.msg = ' '.join(msg.strip().split())
        self.reply = ""

        self.msg_list = self.msg.split(' ')
        try:self.keylist = ' '.join(self.msg_list[2:])
        except:self.keylist = ""
        try:self.code = self.msg_list[1]
        except:self.code = ""
        if self.keylist and '--' in self.keylist:
            self.key = "ADD"
            self.keyword_list = self.keylist.split('--',1)
            try:self.keyword = self.keyword_list[0].strip()
            except:self.keyword = ""
            try:self.content = self.keyword_list[1].strip()
            except:self.content = ""
        elif self.keylist and '--' not in self.keylist:
            self.key = "GET"
            self.keyword_list = self.keylist.strip().split(' ')
            try:self.keyword = self.keyword_list[0]
            except:self.keyword = ""
            self.content = ""
        
        #import pdb;pdb.set_trace()
        pass_flag = True
        if str(self.keyword).upper() == "HELP":
            self.key = "HELP"
            pers_dict = self.read_personal_file()
            if pers_dict.keys():
                self.reply = perconf.ERR_MSGS['HELP']%{'keywords':','.join(self.read_personal_file().keys())}
            else:
                self.reply = perconf.ERR_MSGS['EMPTYHELP']
            pass_flag = False
        elif not self.code and not self.keyword:
            self.reply = perconf.ERR_MSGS['WELCOME']
            pass_flag = False
            #raise WelcomeError(self.reply)
        elif self.key == "ADD" and (not self.keyword or not self.content):
            self.reply = perconf.ERR_MSGS['ADDERR']
            pass_flag = False
        elif self.key == "GET" and not self.keyword:
            self.reply = perconf.ERR_MSGS['GETERR']
            pass_flag = False

        #import pdb;pdb.set_trace()
        #auth_stat = self.auth() 
        auth_stat = True
        if auth_stat and pass_flag:
            if str(self.key).upper() == "ADD":
                self.add_details()
            elif str(self.key).upper() == "GET":
                self.get_details()
    
    def read_personal_file(self):
        pers_file = CUR_DIR + perconf.FILE_NAME_MAP['personalfile']
        if os.path.isfile(pers_file):
            per_keywords = {}
            fObj = open(pers_file,'r')
            for perdet in fObj:
                if perdet:per_keywords[str(perdet).strip().split(':::')[0]] = str(perdet).strip().split(':::')[1]
            fObj.close()
        else:
            per_keywords = {}
        return per_keywords

    def get_details(self):
        '''
        if self.keyword.upper() not in perconf.PERSONAL_DICT.keys():
            self.reply = perconf.ERR_MSGS['KEYERR']
        else:
            self.reply = perconf.PERSONAL_DICT[self.keyword.upper()]
        '''
        pers_file = CUR_DIR + perconf.FILE_NAME_MAP['personalfile']
        if os.path.isfile(pers_file):
            per_keywords = {}
            fObj = open(pers_file,'r')
            for perdet in fObj:
                if perdet:per_keywords[str(perdet).strip().split(':::')[0]] = str(perdet).strip().split(':::')[1]
            fObj.close()
        else:
            per_keywords = {}

        if self.keyword.upper() in per_keywords.keys():
            self.reply = per_keywords[self.keyword.upper()]
        else:
            self.reply = perconf.ERR_MSGS['KEYERR']

    def add_details(self):
        try:
            pers_file = CUR_DIR + perconf.FILE_NAME_MAP['personalfile']
            if os.path.isfile(pers_file):
                per_keywords = {}
                fObj = open(pers_file,'r')
                for perdet in fObj:
                    if perdet:per_keywords[str(perdet).strip().split(':::')[0]] = str(perdet).strip().split(':::')[1]
                fObj.close()
            else:
                per_keywords = {}
            
            if self.keyword.upper() in per_keywords.keys():
                operation = "UP"
            else:
                operation = "ADD"
            
            if operation == "ADD":
                if os.path.isfile(pers_file):
                    fObj = open(pers_file,'a')
                    fObj.write('\n'+str(self.keyword).upper() + ":::" + str(self.content))
                else:
                    fObj = open(pers_file,'w')
                    fObj.write(str(self.keyword).upper() + ":::" + str(self.content))
                fObj.close()
                self.reply = perconf.ERR_MSGS['ADDSUC']
            elif operation == "UP":
                fObj = open(pers_file,'r')
                text = fObj.read()
                fObj.close()
                
                fObj = open(pers_file,'w')
                source_text = str(self.keyword).upper() + ":::" + per_keywords[str(self.keyword).upper()]
                dest_text = str(self.keyword).upper() + ":::" + str(self.content)
                fObj.write(text.replace(source_text, dest_text))
                fObj.close()
                self.reply = perconf.ERR_MSGS['UPSUC']
        except Exception,e:
            self.reply = perconf.ERR_MSGS['ADDFAIL']

    def auth(self):
        codefile = CUR_DIR + perconf.FILE_NAME_MAP['codefile']
        if os.path.isfile(codefile):
            code_list = []
            fObj = open(codefile,'r')
            for code in fObj:
                if code:code_list.append(str(code))
            fObj.close()
        else:
            code_list = []

        if not self.code or not perconf.AUTH_CODE(self.code) or str(self.code) in code_list:
            self.reply = perconf.ERR_MSGS['AUTH']
            return False
        try:
            if os.path.isfile(codefile):
                fObj = open(codefile,'a')
                fObj.write('\n'+str(self.code))
            else:
                fObj = open(codefile,'w')
                fObj.write(str(self.code))
            fObj.close()
        except:
            pass
        return True

def handle_personal(msg):
    try:
        PObj = Personal(msg)
        return PObj.reply
    except:
        return perconf.ERR_MSGS['INERR']


if __name__ == "__main__":
    print handle_personal(sys.argv[1])

