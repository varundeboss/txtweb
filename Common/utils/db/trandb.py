"""Transactional MySQL Database implementation 

"""


import MySQLdb
import ConfigParser
import traceback

from utils.misc.customexception import TMSCustomException
from utils.misc.customlogger import basiclogger

from tms.paymentcalendar.globalvars import GlobalVars

db_logger = basiclogger("DB_Logger", "DB")
configfile = '/public/gdp/trunk/src/Zebit/sms/config/db.config'


class TranDB:
    """Transactional Database
    
    """
    conn = None
    def __init__(self, config=configfile, section="DEFAULT", logger=db_logger,
                 charset='utf8'):
        """Initialize

        Reads the database details from the configuration file and creates the
        connection attribute.

        @param configfile: string, absolute path to the configuration file

        """
        key = GlobalVars()
        key_id = key.getkeyid()
        
        self.logger = logger
        self.config = config
        self.section = section
        self.charset = charset
        
        if not TranDB.conn or TranDB.conn.open == 0:
            self.logger.info(str(key_id)+" :: Going to TranDB.getmysqlconnection")
            TranDB.conn = self.getmysqlconnection()
            self.logger.info(str(key_id)+" :: Thread_id::"+str(TranDB.conn.thread_id()))
            self.logger.info(str(key_id)+" :: Status::\n"+str(TranDB.conn.stat()))
        else:
            TranDB.conn = TranDB.conn
            self.logger.info(str(key_id)+" :: Using the old existing connection")
            self.logger.info(str(key_id)+" :: Thread_id::"+str(TranDB.conn.thread_id()))
            self.logger.info(str(key_id)+" :: Status::"+str(TranDB.conn.stat()))
                
    def getmysqlconnection(self):
        """Getting MySQL Connection
        
        @param section: Configuration section to be used
        
        """
        key = GlobalVars()
        key_id = key.getkeyid()
        self.logger.info(str(key_id)+" :: Inside TranDB.getmysqlconnection")
        self.logger.info(str(key_id)+" :: Trying to get new connection")
        
        # Getting Configuration Parameters 
        config = ConfigParser.ConfigParser()
        config.read(self.config)

        database = config.get(self.section,'database')
        host = config.get(self.section,'host')
        try:
            port = config.getint(self.section,'port')
        except ConfigParser.NoOptionError:
            port = 3306
        user = config.get(self.section,'username')
        passwd = config.get(self.section,'password')
        for i in range(2):
            try:
                # Creating MySQL Connection
                conn = MySQLdb.connect(host=host, user=user, passwd=passwd, 
                                       db=database, port=port,
                                       charset=self.charset)
                
                self.logger.info(str(key_id)+" :: Returning connection")
                return conn
            except MySQLdb.OperationalError, e:
                self.logger.debug(str(key_id)+" :: Exception Occurred in creating Connection::\n"+traceback.format_exc())
                self.logger.debug(str(key_id)+" :: Attempt Count:: "+str(i))
                
                # Creating MySQL Connection
                conn = MySQLdb.connect(host=host, user=user, passwd=passwd, 
                                       db=database, port=port,
                                       charset=self.charset)
                
                self.logger.info(str(key_id)+" :: Returning connection")
                return conn
            except Exception , e:
                self.logger.debug(str(key_id)+" :: Exception Occurred in creating Connection::\n"+traceback.format_exc())
                self.logger.debug(str(key_id)+" :: Attempt Count:: "+str(i))
                self.logger.debug(str(key_id)+" :: Cannot get connection")
                break
        
        self.logger.critical(str(key_id)+" :: Raising runtime error => Failed getting connection")                
        raise RuntimeError("Failed Getting Connection!!!")
    
    def getcursor(self , type=1):
        """Getting Cursor Object
        
        @param type: int, Type of Cursor
                        0 - Normal Cursor
                        1 - Dictionary Cursor
        
        """
        key = GlobalVars()
        key_id = key.getkeyid()
        self.logger.info(str(key_id)+" :: Inside TranDB.getcursor")
        
        if type:
            self.logger.info(str(key_id)+" :: Returning DictCursor")
            return TranDB.conn.cursor(MySQLdb.cursors.DictCursor)
        self.logger.info(str(key_id)+" :: Returning NormalCursor")
        return TranDB.conn.cursor()
    
    def commit(self):
        """Committing the changes
        
        """
        key = GlobalVars()
        key_id = key.getkeyid() 
        self.logger.info(str(key_id)+" :: Inside TranDB.commit")

        self.logger.info(str(key_id)+" :: Committing the changes for conn="+str(TranDB.conn.thread_id()))
        TranDB.conn.commit()
        self.logger.info(str(key_id)+" :: Returning from TranDB.commit")
        
    def rollback(self):
        """Rollbacking the chnages
        
        """
        key = GlobalVars()
        key_id = key.getkeyid()
        self.logger.info(str(key_id)+" :: Inside TranDB.rollback")
        
        self.logger.info(str(key_id)+" :: RollBacking the changes for conn="+str(TranDB.conn.thread_id()))
        TranDB.conn.rollback()
        self.logger.info(str(key_id)+" :: Returning from TranDB.rollback")
        
    def close(self):
        """Closing the Connection
        
        """
        key = GlobalVars()
        key_id = key.getkeyid()
        self.logger.info(str(key_id)+" :: Inside TranDB.close")
        
        self.logger.info(str(key_id)+" :: Closing the connection for conn="+str(TranDB.conn.thread_id()))
        TranDB.conn.close()
        self.logger.info(str(key_id)+" :: Returning from TranDB.close")
    
    def processquery(self , query , curs , count=0 , args=None , 
                     fetch=True):
        """Process query
        
        @param query: str, Query to be executed
        @param count: int, How many records to be returned
                        0 - All records to be returned
                        1 - One record to be returned
                        N - N number of records to be returned
        @param curs: MySQL cursor object
        @param args: Sequence passed if any to be used in the query
        @param fetch: bool, Whether to fetch the record or insert/update the 
        record
                        True - Select Query
                        False - Insert/update Query
                        
        """
        key = GlobalVars()
        key_id = key.getkeyid() 
        self.logger.info(str(key_id)+" :: Inside TranDB.processquery")
        
        try:
            self.logger.info(str(key_id)+" :: Trying to execute queries")
            self.logger.info(str(key_id)+" :: Query::\n"+query)
            self.logger.info(str(key_id)+" :: Arguments::"+str(args))
            
            curs.execute(query , args)
            if fetch:
                if count == 1:
                    self.logger.info(str(key_id)+" :: Returning one result")
                    res = curs.fetchone()
                    self.logger.info(str(key_id)+" :: Result set::\n"+str(res))
                    return res
                elif count > 1:
                    self.logger.info(str(key_id)+" :: Returning %s results" % (count))
                    res = curs.fetchmany(count)
                    self.logger.info(str(key_id)+" :: Result set::\n"+str(res))
                    return res
                else:
                    self.logger.info(str(key_id)+" :: Returning all results")
                    res = curs.fetchall()
                    self.logger.info(str(key_id)+" :: Result set::\n"+str(res))
                    return res
            else:
                self.logger.info(str(key_id)+" :: Returning after Insert/Update Query")
                return
        except MySQLdb.Warning, e:
            log = traceback.format_exc()
            self.logger.warning(str(key_id)+" :: MySQL Warning::"+str(e.args))
#            raise TMSCustomException(str(key_id), "WXQ", "Warning Executing query", 
#                                     query+"\n"+log, mail=1, excobj=e)
        except MySQLdb.OperationalError, e:
            log = traceback.format_exc()
            self.logger.critical(str(key_id)+" :: Raising exception => "+log)
            if e.args[0] == 2006:
                self.logger.critical(str(key_id)+" :: Recreating connection")
                TranDB.conn = self.getmysqlconnection()
                self.processquery(query, curs, count, args, fetch)
            else:
                raise TMSCustomException(str(key_id), "EXQ", "Error Executing query", 
                                         query+"\n"+log, mail=1, excobj=e)
        except MySQLdb.MySQLError, e:
            log = traceback.format_exc()
            self.logger.critical(str(key_id)+" :: Raising exception => "+log)
            raise TMSCustomException(str(key_id), "EXQ", "Error Executing query", 
                                     query+"\n"+log, mail=1, excobj=e) 
        except Exception, e:
            log = traceback.format_exc()
            self.logger.critical(str(key_id)+" :: Raising exception = > "+log)
            raise TMSCustomException(str(key_id), "SQLSE", "SQL Software Exception", 
                                     query+"\n"+log, mail=1, excobj=e)
        