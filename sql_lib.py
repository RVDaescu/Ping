import sqlite3
from utils import *
import sys

sys.dont_write_bytecode = True

class sql(object):
    """
    Object for sql purposes (details bellow)
    """

    def connect(self, db):
        """
        creates/opens DB
        """
        self.con = sqlite3.connect(db)

    def add_table(self, db, tb, **kwargs):
        """adds a table and its header
        """
        
        self.connect(db)
        self.cursor = self.con.cursor()

        tb_fields = py2sql(kwargs)

        cmd = "CREATE TABLE %s (" %tb

        for key, val in tb_fields.items():
            cmd = cmd + "%s %s, " %(key, val)
        
        if 'Time' in kwargs.keys():
            cmd = cmd + "PRIMARY KEY(time))" 
        elif 'IP' in kwargs.keys():
            cmd = cmd + "PRIMARY KEY(IP))"
            
        try:
            self.cursor.execute(cmd)
        except:
            pass
        self.con.commit()

    def add_value(self, db, tb, **kwargs):
        """Adds entries inside sql db
        """

        if tb not in get_sql_db_table(db = db):
            self.add_table(db, tb, **kwargs)
        
        self.connect(db)
        self.cursor = self.con.cursor()

    	k = ''
    	v = ''
    	
    	for key, val in kwargs.items():
	        k = k + '%s, ' %key
	        v = v + '"%s", ' %val

        k = k.replace('', '')[:-2]
        v = v.replace('', '')[:-2]

        cmd = 'INSERT INTO %s (%s) VALUES (%s);' %(tb, k, v)

        self.cursor.execute(cmd)
        self.con.commit()

        self.close()

    def get_data(self, db, tb, field = '*', start = None, end = None, key = 'time'):
        """ 
        if start and end - return values between them
        if start - return values from "start" till "end" of file
        if end - return values from begining till "end"
        if not (start or end) - return all table content
        if filed == * - returns all fields
           else - returns selected field
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        if start and end:
            if start < end:
                wh = 'WHERE time > %s and time < %s' %(start,end)
            else:
                print 'Start should be larger than end'
        elif start and not end:
            wh = 'WHERE time > %s' %start
        elif not start and end:
            wh = 'WHERE time < %s' %end
        else:
            wh = ''
        
        if key.lower() == 'time':
            cmd = 'SELECT %s FROM %s %s ORDER BY time;' %(field, tb, wh)
        elif key.lower() == 'ip':
            cmd = 'SELECT %s FROM %s %s ORDER BY ip;' %(field, tb, wh)

        data = self.cursor.execute(cmd).fetchall()
        header = [i[0] for i in self.cursor.execute(cmd).description]
        header = dict(zip(header, range(0,(len(header)))))
        
        res = [header]+data
        
        self.close()

        return res

    def get_value(self, db, tb, field = '*', lookup = 'IP', value = None):
        """
        gets only one value from db file based on field and field value
        gets entire column based on field
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        if value:
            where = ' WHERE %s is "%s"' %(lookup, value)
        else:
            where = ''
       
        cmd = 'SELECT %s from %s%s;' %(field, tb, where)

        data = self.cursor.execute(cmd).fetchall()

        if value:
            return str(data[0][0])
        else:
            return [i[0] for i in data]

        self.close()

    def get_row(self, db, tb, lookup):
        """
        returns entire row for an lookup (usualy IP)
        """

        self.connect(db)
        self.cursor = self.con.cursor()

        cmd = "SELECT * from %s WHERE IP = \"%s\"" %(tb, lookup)
        data = self.cursor.execute(cmd).fetchall()
    
        header = [i[0] for i in self.cursor.execute(cmd).description]
        header = dict(zip(header, range(0,(len(header)))))
        return [header] + data

        self.close()

    def close(self):
        
        self.con.close()

def ip_to_name(db, tb, ip):

    return sql().get_value(db = db, tb = tb, field = 'Name', lookup = 'IP', value = ip)
