import sqlite3
from utils import *

class sql(object):

    def connect(self, db_name):
        """
        creates/opens DB
        """
    
        self.con = sqlite3.connect(db_name)

    def add_table(self, db_name, tb_name, **kwargs):
        """adds a table and its header
        """
        
        self.connect(db_name)
        self.cursor = self.con.cursor()

        tb_fields = py2sql(kwargs)

        cmd = "CREATE TABLE %s (" %tb_name

        for key, val in tb_fields.items():
            cmd = cmd + "%s %s, " %(key, val)

        cmd = cmd + "PRIMARY KEY(time))"

        try:
            self.cursor.execute(cmd)
        except:
            pass
        self.con.commit()

    def add_value(self, db_name, tb_name, **kwargs):
        """Adds entries inside sql db
        """
    
        if tb_name not in get_sql_db_table(db_name):
            self.add_table(db_name, tb_name, **kwargs)
        else:
            self.connect(db_name)
	    self.cursor = self.con.cursor()

	k = ''
	v = ''
	for key, val in kwargs.items():
	    k = k + '%s, ' %key
	    v = v + '"%s", ' %val

	k = k.replace('', '')[:-2]
	v = v.replace('', '')[:-2]

	cmd = 'INSERT INTO %s (%s) VALUES (%s);' %(tb_name, k, v)

        self.cursor.execute(cmd)
        self.con.commit()

    def get_data(self, db_name, tb_name, field = '*', start = None, end = None):
        """ if start and end - return values between them
            if start - return values from start till end of file
            if end - return values from begining till end
            if not (start or end) - return all table content
            if filed == * - returns all fields
            else - returns selected field
        """

        self.connect(db_name)

        if start and end:
            wh = ' WHERE time > start and time < end'
        elif start and not end:
            wh = ' WHERE time > start'
        elif not start and end:
            wh = ' WHERE time < end'
        else:
            wh = ''
            
        cmd = 'SELECT %S FROM %s%s ORDER BY time;' %(field, tb_name, wh)

        res = self.cursor.execute(cmd).fetchall()

        return res
