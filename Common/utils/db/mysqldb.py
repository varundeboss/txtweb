import ConfigParser
import MySQLdb

__author__="parthan <parthan@global-analytics.com>"
__date__ ="$Apr 26, 2010 2:50:27 PM$"

class MySQLWrapper(object):
    def __init__(self, configfile='/public/gdp/cms/src/config/db.config', 
                 section='DEFAULT', charset='utf8'):
        """Initialize

        Reads the database details from the configuration file and creates the
        connection attribute.

        @param configfile: string, absolute path to the configuration file

        """
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        self.charset = charset
        self.database = config.get(section,'database')
        self.host = config.get(section,'host')
        try:
            self.port = config.getint(section,'port')
        except ConfigParser.NoOptionError:
            self.port = 3306
        self.user = config.get(section,'username')
        self.passwd = config.get(section,'password')

        self.return_as_dict = True
        self.connection = None

    def _connect(self):
        """Connect to the MySQL Database.

        @return: MySQLdb connection object

        """
        return MySQLdb.connect(host=self.host, user=self.user,
                                passwd=self.passwd, db=self.database,
                                port=self.port, charset=self.charset)

    def unset_return_as_dict(self):
        """Unset Return As Dictionary.

        By default, the wrapper return the query results as a dictionary. This
        is managed by the attribute return_as_dict. In case the query result is
        not required as dictionary but as tupple(s), this method can be used to
        set the attribute to False and hence the appropriate cursor will be used
        while executing the query.

        """
        if self.return_as_dict is True:
            self.return_as_dict = False

    def toggle_return(self):
        """Toggle Return as Dictionary

        Toggles the boolean value of return_as_dictionary attribute.
        
        """
        self.return_as_dict = not(self.return_as_dict)

    def _normal_cursor(self):
        """Normal Cursor.

        The cursor call returns the query result in the formt of tupples.

        """
        return self.connection.cursor()

    def _dict_cursor(self):
        """Dictionary Cursor.

        The cursor call returns the query result in the form of dictionary.

        """
        return self.connection.cursor(MySQLdb.cursors.DictCursor)

    def get_cursor(self):
        """Get Cursor Object.

        Check the return_as_dict attribute and return an appropriate cursor
        object.

        """
        if self.return_as_dict is True:
            return self._dict_cursor()
        else:
            return self._normal_cursor()

    def get_one_result(self, query, args=None):
        """Get One Result for Query.

        @param query: string, query string with values filled in
        @return: dict or tuple, result set

        """
        self.connection = self._connect()
        cur = self.get_cursor()
        cur.execute(query, args)
        res = cur.fetchone()
        cur.close()
        self.connection.close()
        self.connection = None
        return res

    def get_many_results(self, query, num_of_results=1):
        """Get Many Result of Query

        @param query: string, query string with values filled in
        @param num_of_results: int, number of results in result set, default 1
        @return: dict or tuple, result set

        """
        self.connection = self._connect()
        cur = self.get_cursor()
        cur.execute(query)
        res = cur.fetchmany(num_of_results)
        cur.close()
        self.connection.close()
        self.connection = None
        return res

    def get_all_results(self, query, args=None):
        """Get All Results for Query

        @param query: string, query string with values filled in
        @return: dict or tuple, result set

        """
        self.connection = self._connect()
        cur = self.get_cursor()
        cur.execute(query, args)
        res = cur.fetchall()
        cur.close()
        self.connection.close()
        self.connection = None
        return res

    def insert(self, query, args=None):
        """Insert Query for All Data.

        @param query: string, query string with place holders for values
        @return: cursor.lastrowid, the row id of the last inserted data

        """
        self.connection = self._connect()
        cur = self._normal_cursor()
        cur.execute(query, args)
        self.connection.commit()
        last_row_id = cur.lastrowid
        cur.close()
        self.connection.close()
        self.connection = None
        return last_row_id

    def execute(self, query, requires_commit=True, args=None):
        """Execute Query

        Can be used for all queries, especially non-table operations. Set the \
        parameter requires_commit to True when the connection is transactional
        and is useful for executing UPDATE queries.
        
        @param query: string, query string with place holders for values
        @return: cursor.rowcount, number of rows affected by the query

        """
        self.connection = self._connect()
        cur = self._normal_cursor()
        cur.execute(query, args)
        if requires_commit:
            self.connection.commit()
        rowcount = cur.rowcount
        cur.close()
        self.connection.close()
        self.connection = None
        return rowcount

    def commit(self):
        try:
            self.connection.commit()
            return True
        except:
            return False

    def rollback(self):
        from MySQLdb import NotSupportedError
        try:
            self.connection.rollback()
            return True
        except NotSupportedError, e:
            print str(e)
            return False

    def get_operator(self, oper):
        if oper == "eq":
            return "="
        elif oper == "gt":
            return ">"
        elif oper == "ge":
            return ">="
        elif oper == "lt":
            return "<"
        elif oper == "le":
            return "<="
        elif oper == "is":
            return "IS"
        else:
            return ""

    def build_query(self, querytype, table, data=None, condition=None,
                    groupby=None, asc_des=None, having=None, orderby=None,
                    limit=0):
        """Build Query.

        """
        query = ""
        if querytype is "select":
            query += "SELECT "
            if data is not None:
                query += ", ".join([ item for item in data]) + " FROM %s"%table
            else:
                query += "* FROM `%s`"%table
        elif querytype is "insert":
            query += "INSERT INTO `%s`"%table
            if data is None:
                raise "Data can not be None for an Insert query"
            cols = []
            vals = []
            for col, val in data:
                cols.append(col)
                vals.append(val)
            query += " (" + ', '.join(["`%s`"%col for col in cols]) + ")"
            query += " VALUES (" + ', '.join([ ( (isinstance(val, str) and ["'%s'"%val]) or ["%s"%val])[0]  for val in vals]) + ")"
        elif querytype is "update":
            query += "UPDATE `%s`"%table
            query += " SET "
            query += ', '.join([ "`%s`"%col + "=" + ( (isinstance(val, str) and ["'%s'"%val]) or ["%s"%val])[0] for col, val in data ])
        elif querytype is "delete":
            query += "DELETE FROM `%s`"%table
        if condition is not None:
            for link, col, oper, value in condition:
                if not link:
                    query += " WHERE"
                else:
                    query += " %s"%link
                if isinstance(value, str):
                    query += " `%s` %s '%s'"%(col, self.get_operator(oper), value)
                else:
                    query += " `%s` %s %s"%(col, self.get_operator(oper), value)
        if groupby is not None:
            query += " GROUP BY `%s`"%groupby
            if asc_des is not None:
                query += " %s"%asc_des
            if having is not None:
                col, oper, val = having
                query += " HAVING `%s` %s %s"%(col, self.get_operator(oper), val)
        if orderby is not None:
            query += " ORDER BY "
            if isinstance(orderby, str):
                query += "`%s`"%orderby
            else:
                query += ', '.join(["`%s`"%item for item in orderby])
        if limit:
            query == " LIMIT %d"%limit
        return query

if __name__ == "__main__":
    print "MySQLdb Wrapper";
    dbobj = MySQLWrapper()
    selectquery = dbobj.build_query('select', 'test', ('name', 'age', 'address'),
                                    [('','age','lt', 18),('OR','age','ge',80)],
                                    'age', 'ASC', None, None, 20)
    print "SELECT QUERY 1 : ", selectquery
    selectquery = dbobj.build_query('select', 'test')
    print "SELECT QUERY 2 : ", selectquery
    insertquery = dbobj.build_query("insert", 'test', [('name','shane'),('age',22)])
    print "INSERT QUERY : ", insertquery
    updatequery = dbobj.build_query("update", 'test', [('name', 'paul'), ('age', 32)],
                                    [('','age','eq',22)], None, None, None, 'age', 10)
    print "UPDATE QUERY : ", updatequery
    deletequery = dbobj.build_query('delete', 'test', None, [('','age','le',20)])
    print "DELETE QUERY : ", deletequery
