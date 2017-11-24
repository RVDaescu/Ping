from random import choice
from time import ctime
import sqlite3, string, pexpect

def raw(int):
        
    if int:
        return ''.join(choice(string.lowercase) for i in range(int))
    else:
        pass

def ret_type(i):
    
    return str(type(i)).split("'")[1]

def py2sql(dict):

    py2sql_dict = {
            'int': 'INT',
            'str': 'VARCHAR(8000)',
            'float': 'FLOAT(2)',
            'unicode': 'VARCHAR(8000)',
            'long': 'BIGINT'
                }
    
    ls_dict = {}

    for i,j in dict.items():
        ls_dict[i] = py2sql_dict[ret_type(j)]

    return ls_dict

def float2date(i):

    return ctime(i)

def get_sql_db_table(db_name):

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type ='table';")
     
    val = cursor.fetchall()

    table_list = []

    if not val:
        return ''
    else:
        for i in range(len(val)):
            table_list.append(val[i][0].encode('utf-8'))
        
        return table_list

def ip_to_dev(ip):
    p = pexpect.spawn('ip route get %s' %ip)

    a = [i for i in p]

    for i in a: 
        i = i.split(' ')
        if 'dev' in i:
            return i[i.index('dev')+1]
        else:
            print 'Could not find outgoing interface for ip %s' %ip
            print a[0]
            return False

