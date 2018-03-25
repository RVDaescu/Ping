from sql_lib import *
from utils import *

from time import time, ctime

db = 'res_db.sqlite'
tbs = get_sql_db_table(db = db)
failed = []
ts = []

for tb in tbs:
    t = max((sql().get_data(db = db, tb = tb, field = 'Time'))[0])
    if time() - t > 400:
        failed.append(tb)
        ts.append(ctime(t))

print "%s are not working for 400s" %len(failed)
for i,j in zip(failed,ts): print "%s since \t\t %s" %(i,j)
