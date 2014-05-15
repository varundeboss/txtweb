from math import sin

AUTH_CODE = lambda code : True if code and str(code).isdigit() and str(code)[0] + str(code)[1:int(str(code)[0] or 0)+1] + str(sin(int(str(code)[1:int(str(code)[0])+1] or 0))).split('.')[1][:4] == str(code) and int(str(code)[1:int(str(code)[0])+1] or 0) != 0 else False

FILE_NAME_MAP = {
                    'codefile' : "/codelist.txt", 
                    'personalfile' : "/personal.txt"
                }

PERSONAL_DICT = {
                    "GAADDR" : "GA",
                }

ERR_MSGS = { 
            "AUTH" : "The auth code is invalid. Please try again with a valid auth code.",
            "KEYERR" : "The keyword is invalid. Send @varundeboss |code| help for existing keywords",
            "WELCOME" : "Welcome Varun. For getting your personal details send '@varundeboss prl |authcode| |keyword|'",
            "ADDERR" : "For adding a new personal detail send @varundeboss plr |code| |keyword--content|. Sending existing keyword updates existing content",
            "GETERR" : "For getting your personal detail send @varundeboss plr |code| |keyword|",
            "HELP" : "Existing Keywords : %(keywords)s",
            "ADDSUC" : "Your personal details has been added successfully",
            "ADDFAIL" : "Failed to add your personal detail. Please try again later",
            "UPSUC" : "Your personal details has been updated successfully",
            "EMPTYHELP" : "No existing keywords found. For adding a new personal detail send @varundeboss plr |code| |keyword--content|.",
            "INERR" : "Sorry we are facing some technical issue. Please try again later.",
           }                    
