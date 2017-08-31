#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect('127.0.0.1','root','admin','mydb')

cursor = db.cursor()

cursor.execute('DROP TABLE IF EXISTS mydb')

sql = """CREATE TABLE mydb(
         TIME FLOAT,
         SENT INT,
         RECEIVED INT,
         REACHABILITY CHAR(5),
         JITTER FLOAT,
         AVG_RSP FLOAT )"""

cursor.execute(sql)

db.close()
