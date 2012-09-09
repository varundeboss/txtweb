from Common.utils.db.webpy.web import db
from Common.config import MysqlConf

import os

_dbTXT = None

def get_db(DB=None):
    global _dbTXT 
    mysql_conf = MysqlConf.MYSQL_CONF[os.environ['TXTWEB_HOSTNAME']]
    if DB is 'TXT':
        if _dbTXT is None:
            _dbTXT = db.database(
                        host=mysql_conf['MYSQL_HOST'], 
                        dbn = 'mysql', 
                        db=MysqlConf.MYSQL_DB_MAP[DB], 
                        user=mysql_conf['MYSQL_USER'], 
                        pw=mysql_conf['MYSQL_PASS'],
                    )
        return _dbTXT

if __name__ == '__main__':
    pass
