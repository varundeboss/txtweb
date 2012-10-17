AUTH_CODE = lambda code:code

PERSONAL_DICT = {
                    "CHNHADDR" : "R.Varun Kumar, Ground Floor plot no 20, 3rd street, Kumaraguru Avenue, Metukuppam. Near ASV SunTechPark. Chennai-600097. Mobile-8870435477.",
                    "TVLHADDR" : "R.Varun Kumar, 216 Shenbagam pillai double street, Tirunelveli-Town. Pin-627006. Mobile-8870435477. LandLine-04622620619",
                    "GAADDR" : "GA",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                    "" : "",
                }

ERR_MSGS = { 
            "AUTH" : "The auth code is invalid. Please try again with a valid auth code.",
            "KEYERR" : "The keyword is invalid. Available keywords are : "+str(PERSONAL_DICT.keys()),
            "WELCOME" : "Welcome Varun. For getting your personal details send '@varun prl <keyword> <authcode>'",
           }                    
