#!/usr/bin/env python

import os
from datetime import datetime

import pdb;pdb.set_trace()

print os.path.dirname(__file__)

PROJECT = "AppBuilder"
project_dir, handler = os.path.split(__file__)
PROJECT_PATH = project_dir.replace(PROJECT,'')

APPS_PATH = os.path.join(PROJECT_PATH, "Apps")

try:
    from optparse import OptionParser
except ImportError:
    print "Error importing optparse module"
    sys.exit(1)

class AppCreator():
    def __init__(self,options):
        self.options = options
        self.today   = datetime.now().strftime('%b %d, %Y') 

    def write_to_file(self,category,fileName):
        def header():
            tmpl = "'''"
            tmpl += "\nCreated on %(today)s\n\n@author: %(author)s\n"%{'today':self.today,'author':self.options.author}
            tmpl += "'''"
            return tmpl
        def footer():
            tmpl = "\n"
            tmpl += "if __name__ == '__main__':\n"
            tmpl += "    pass\n"
            return tmpl
        def write_file(lines):
            fObj = open(fileName,'w')
            fObj.write(lines)
            fObj.close()

        if category == "file":
            write_file(header() + footer())
        elif category == "init":
            write_file(header())
        elif category == "conf":
            write_file("")
        elif category == "models":
            write_file(header())
        else:
            write_file("")

    def create_app(self):
        FullAppName = os.path.join(APPS_PATH, self.options.application.upper())
        FullAppFile = os.path.join(FullAppName, self.options.application.lower() + ".py")
        FullAppInit = os.path.join(FullAppName, "__init__.py")
        FullAppConf = os.path.join(FullAppName, self.options.application.lower() + "_config.py")
        FullAppModel = os.path.join(FullAppName, self.options.application.lower() + "_models.py")
        if not os.path.isdir(FullAppName):
            try:
                os.system("mkdir -p %s"%(FullAppName))
                self.write_to_file('file', FullAppFile)
                self.write_to_file('init', FullAppInit)
                self.write_to_file('conf', FullAppConf)
                self.write_to_file('models', FullAppModel)
                return "App created Successfully : %s"%(FullAppName)
            except Exception,e:
                print e
                if os.path.isdir(FullAppName):os.system("rm -rf %s"%(FullAppName))
                return "Error while creating App : %s"%(FullAppName)
        else:
            return "App already exists. Please try someother app name."

def main():
    parser = OptionParser()
    usage = "Usage: %prog -a [Author] -A [AppName]"
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-a", "--author",  action="store", type="string",dest="author",  help="Name of the author creating the application")
    parser.add_option("-A", "--application", action="store", type="string", dest="application", help="Application to be created")
    (options, args) = parser.parse_args()
    if options.author and options.application:
        AppObj = AppCreator(options)
        return AppObj.create_app()
    else:
        print "Fatal: Required arguments are missing!"
        print "Use: -h / --help to get help."
        sys.exit(1)

if __name__ == "__main__":
    print main()
