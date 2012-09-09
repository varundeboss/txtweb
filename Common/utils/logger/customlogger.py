"""Custom Logger

This module provides custom loggers.

"""

__author__="parthan"
__date__ ="$May 21, 2010 2:28:14 PM$"

import os
import logging
import logging.handlers
import ConfigParser

from Common import PROJECT_PATH
from MasterConf import LOGGER_CONFIG_PATH

LEVELS = {'DEBUG':logging.DEBUG,
          'INFO':logging.INFO,
          'WARNING':logging.WARNING,
          'ERROR':logging.ERROR,
          'CRITICAL':logging.CRITICAL
          }

LOGCONFIGFILE = os.path.join(PROJECT_PATH, LOGGER_CONFIG_PATH)
def getconfig(section='DEFAULT'):
    config = ConfigParser.ConfigParser()
    config.read(LOGCONFIGFILE)
#    if 'TROTATING' in section:
#        return (config.get(section, 'logfile'),
#                config.get(section, 'defaultlevel'),
#                config.get(section, 'logmode'),
#                config.get(section, 'rotatetime')
#                )
    if 'ROTATING' in section:
        return (config.get(section, 'logfile'),
                config.get(section, 'defaultlevel'),
                config.get(section, 'logmode'),
                config.get(section, 'maxbytes'),
                config.get(section, 'backupcnt'),
                 )
    return (config.get(section, 'logfile'),
            config.get(section, 'defaultlevel'),
            config.get(section, 'logmode'),
            )

def basiclogger(logname, section='DEFAULT'):
    logfile, deflevel, logmode = getconfig(section)
    logger = logging.getLogger(logname)
    logger.setLevel(LEVELS[deflevel])
    mode = {'append':'a', 'overwrite':'w'}[logmode]
    handler = logging.handlers.RotatingFileHandler(filename=logfile,
                                                   mode=mode,
                                                   maxBytes=0,
                                                   backupCount=0,
                                                   )
    #formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(module)s :: %(message)s')
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def rotatinglogger(logname, section='ROTATING'):
    logfile, deflevel, logmode, maxbytes, backupcnt = getconfig(section)
    logger = logging.getLogger(logname)
    logger.setLevel(LEVELS[deflevel])
    mode = {'append':'a', 'overwrite':'w'}[logmode]
    if not logger.handlers:
        # BUG FIX
        # this check prevents multiple handlers being added if the logging
        # object already has a handler
        handler = logging.handlers.RotatingFileHandler(filename=logfile,
                                                       mode=mode,
                                                       maxBytes=maxbytes,
                                                       backupCount=backupcnt)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(module)s :: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

timedrotatinglogger = rotatinglogger

#def timedrotatinglogger(logname, section="TROTATING"):
#    logfile, deflevel, logmode, rotatetime = getconfig(section)
#    logger = logging.getLogger(logname)
#    logger.setLevel(LEVELS[deflevel])
#    mode = {'append': 'a', 'overwrite': 'w'}[logmode]
#    handler = logging.handlers.TimedRotatingFileHandler(filename=logfile,
#                                                        when = rotatetime)
#
#    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(filename)s :: %(message)s')
#    handler.setFormatter(formatter)
#    logger.addHandler(handler)
#    return logger
    
if __name__ == "__main__":
    print "Custom Loggin Module"
    blogger = basiclogger('default')
    blogger.debug('This is a debug message')
    rlogger = rotatinglogger('tms.utils.misc.customlogger')
    rlogger.debug('This is a debug message')
    rlogger.critical('This is a very critical information that needs to be logged')
    rlogger.info('This is a non critical information that needs to be logged')
    rlogger.warning('This is a non critical warning that can be safely ignored if you do not care')
