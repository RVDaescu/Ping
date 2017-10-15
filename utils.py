from random import choice
import string

def raw(int):
    
        return ''.join(choice(string.lowercase) for i in range(int))

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
