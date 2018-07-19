

from pony.orm import *

db = Database(provider='postgres', user='vlimbot', password='asdfghjk', host='127.0.0.1', database='vlim_bot')
#
from . import partner
#
db.generate_mapping(create_tables=True)
