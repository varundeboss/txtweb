import Common

if Common.TXTWEB_MYSQL in Common.MYSQL_NORMAL:
    from Common.utils.db.webpy.web import db as mysql_db
if Common.TXTWEB_MYSQL in Common.MYSQL_GOOGLE:
    from google.appengine.ext import db as google_db
from Common.config import MysqlConf
from Common import TXTWEB_HOSTNAME, TXTWEB_MYSQL

import os

_dbTXT = None

def get_db(DB=None):
    global _dbTXT 
    mysql_conf = MysqlConf.MYSQL_CONF[TXTWEB_MYSQL]
    if DB is 'TXW':
        if _dbTXT is None:
            _dbTXT = mysql_db.database(
                        host=mysql_conf['MYSQL_HOST'], 
                        dbn = 'mysql', 
                        db=mysql_conf['DB'][DB], 
                        user=mysql_conf['MYSQL_USER'], 
                        pw=mysql_conf['MYSQL_PASS'],
                        #pooling=True,
                    )
        return _dbTXT

def get_gql(DB='TXW',action="",table_obj="",query="",val_dict={}):
    if action == "select":
        #select_obj = google_db.GqlQuery(query)
        result_list = []
        for row in table_obj.run():
            result_list.append(row._entity)
        return result_list
    
    if action == "insert":
        for value in val_dict.keys():
            setattr(table_obj,value,val_dict[value])
        insert_info = table_obj.put()
        return insert_info.id()
 
    if action == "update":
        up_list = []
        for row in table_obj.run():
            for value in val_dict.keys():
                setattr(row,value,val_dict[value])
            up_list.append(row.put())
        return len(up_list)

if __name__ == '__main__':
    pass
