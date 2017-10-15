import sqlite3
from utils import py2sql

def sql_create(db_name = None):
    """
    Creates a new SQL DB if it does not exist;
    In SQL DB, it creates a new table
    """
    
    connection = sqlite3.connect(db_name)

    return True

def sql_add_table(db_name, tb_name, **kwargs):
    """
    Creates a new table & header for each arg in kwargs
    """

    cmd = ''
    for key, val in kwargs.items():
        cmd = cmd + '%s %s, ' %(key, val)
    
    cmd = cmd + ' PRIMARY KEY (time)'
    
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    sql_command = 'CREATE TABLE %s (%s);' %(tb_name, cmd)

    cursor.execute(sql_command)
    connection.commit()
    connection.close()

    return True

def sql_add_value(db_name, tb_name, **kwargs):

    if tb_name not in get_sql_db_table(db_name):
        tb_fields = py2sql(kwargs)
        sql_add_table(db_name, tb_name, **tb_fields)
   
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    k = ''
    v = ''
    for key, val in kwargs.items():
        k = k + '%s, ' %key
        v = v + '"%s", ' %val

    k = k.replace('', '')[:-2]
    v = v.replace('', '')[:-2]

    sql_command = 'INSERT INTO %s (%s) VALUES (%s);' %(tb_name, k, v)

    cursor.execute(sql_command)
    connection.commit()
    connection.close()

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

