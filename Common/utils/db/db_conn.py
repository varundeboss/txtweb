#from Common.utils.db.webpy.web import db
from libs.mysql import connector
from Common.config import MysqlConf
from Common import TXTWEB_HOSTNAME

import os

_dbTXT = None

def get_db(DB=None):
    global _dbTXT 
    mysql_conf = MysqlConf.MYSQL_CONF[TXTWEB_HOSTNAME]
    if DB is 'TXW':
        if _dbTXT is None:
            _dbTXT = connector.connect(
                        host=mysql_conf['MYSQL_HOST'], 
                        #dbn = 'mysql', 
                        database=MysqlConf.MYSQL_DB_MAP[DB], 
                        user=mysql_conf['MYSQL_USER'], 
                        password=mysql_conf['MYSQL_PASS'],
                    )
        return _dbTXT

if __name__ == '__main__':
    pass
