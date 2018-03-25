from sql_lib import *
from utils import *

from time import time

db = 'res_db.sqlite'
tbs = get_sql_db_table(db = db)

for tb in tbs:
    t = max(sql().get_data(db = db, tb = tb, field = 'Time'))[0]
    if time() - t > 400:
        print tb
