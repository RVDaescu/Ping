from __future__ import division
from random import choice
from time import strftime, strptime, localtime, time, mktime
import numpy as np
import sqlite3, string, pexpect, re, statistics
import sys
import time

sys.dont_write_bytecode = True

def raw(n):
    """Builds a n long/bytes string with n characters
    """

    return ''.join(choice(string.lowercase) for i in range(n))

def ret_type(i):
    """Return python based type of value "i"
    """
    
    return str(type(i)).split("'")[1]

def py2sql(dict):
    """
    Based on value type of input dict, return dict with Sqlite type value into a dict
    """

    py2sql_dict = {
            'int': 'INT',
            'str': 'VARCHAR(8000)',
            'float': 'FLOAT(2)',
            'unicode': 'VARCHAR(8000)',
            'long': 'BIGINT',
            'bool': 'BIT'
            }
    
    ls_dict = {}

    for i,j in dict.items():
        ls_dict[i] = py2sql_dict[ret_type(j)]

    return ls_dict

def get_sql_db_table(db):
    """
    For database "db" return all table list
    """

    connection = sqlite3.connect(db)
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
    """
    For IP (a.b.c.d) returns outgoing interface from local routing table
    """

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

def ip_to_gw(ip):
    """
    For IP (a.b.c.d) return mac of outgoing interface
    """

    p = pexpect.spawn('ip route get %s' %ip)
    a = [i for i in p]

    for i in a: 
        i = i.split(' ')
        
        #checking if IP is local or remote
        if 'via' in i:
            gw_ip = i[i.index('via')+1]
            ap = pexpect.spawn('arp -a %s' %gw_ip)
            for j in ap:
                j = j.split(' ')
                if 'at' in j:
                    arp = j[j.index('at')+1]
                    return arp

        #IP is local
        else:
            ap = pexpect.spawn('arp -a %s' %ip)
            for k in ap:
                k = k.split(' ')
                if 'at' in k:
                    arp = k[k.index('at')+1]
                    return arp

    print 'Could not obtain mac for %s' %ip
    return False

def time_con(tm = None, format = 'D.mt-H:m:S'):
    """
    Converts time "tm" to given format:
    D - day;mt - month, H - Hour(24 hour format); m: - minute
    full dict https://docs.python.org/2/library/time.html
    """
    dict = {'D': '%d', 'mt':'%b', 'H':'%H','m':'%M', 'S':'%S'}

    res = re.compile(r'\b(' + '|'.join(dict.keys()) + r')\b')
    res = res.sub(lambda x: dict[x.group()],format)

    return strftime(res, localtime(tm))

def time_epoch(tm, pattern = '%d/%m/%y-%H:%M:%S'):
    """takes a date as string and returns epoch time
    """
    
    return int(mktime(strptime(tm, pattern)))

def list_split(list, no = 50, mode = 'average'):
    """
    Takes list with X number of elements and returns new list 
    devided into "no" lists averaged/maxed/mined
    """

    if len(list)<no:
        return list

    new_list = []

    n = len(list)/no

    if mode is None:
        return list

    for (i,j) in zip(range(0,no),range(1,(no+1))):
        
        if mode.lower() == 'average':
            new_list.append(statistics.mean([list[i] for i in range(int(n*i),int(n*j))]))
        elif mode.lower() == 'max':
            new_list.append(max([list[i] for i in range(int(n*i),int(n*j))]))
        elif mode.lower() == 'min':
            new_list.append(min([list[i] for i in range(int(n*i),int(n*j))]))
        elif 'fractile' in mode.lower():
            fr = mode[-2:]
            new_list.append(np.percentile([list[i] for i in range(int(n*i),int(n*j))], fr))

    return new_list
