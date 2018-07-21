from pony.orm import Database, sql_debug

db = Database()
sql_debug(False)

from . import vxdb

