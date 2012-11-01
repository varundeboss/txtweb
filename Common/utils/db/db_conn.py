from Common.utils.db.webpy.web import db
from Common.config import MysqlConf
from Common import TXTWEB_HOSTNAME, TXTWEB_MYSQL

import os

_dbTXT = None

def get_db(DB=None):
    global _dbTXT 
    mysql_conf = MysqlConf.MYSQL_CONF[TXTWEB_MYSQL]
    if DB is 'TXW':
        if _dbTXT is None:
            _dbTXT = db.database(
                        host=mysql_conf['MYSQL_HOST'], 
                        dbn = 'mysql', 
                        db=mysql_conf['DB'][DB], 
                        user=mysql_conf['MYSQL_USER'], 
                        pw=mysql_conf['MYSQL_PASS'],
                        #pooling=True,
                    )
        return _dbTXT

if __name__ == '__main__':
    pass
