import logging
from pony.orm import *
from models import db
from models.vxuser import VXUser
from models.vxmessage import VXMessage

logger = logging.getLogger("VLIM Bot")

db_provider = 'postgres'
db_user = 'vlimbot'
db_password = 'asdfghjk'
db_host = '127.0.0.1'
db_database = 'vlim_bot'

db.bind(provider=db_provider, user=db_user, password=db_password, host=db_host, database=db_database)

db.generate_mapping(create_tables=True)
