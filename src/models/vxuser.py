
from pony.orm import *
from models import db


class VXUser(db.Entity):
    _table_ = 'vx_user'

    id = PrimaryKey(int, auto=True)
    telegram_user_id = Required(int, unique=True)
    name = Required(str)
    first_name = Required(str)
    last_name = Required(str)
    language_code = Optional(str)
    honorific_address = Required(str)
    full_name = Required(str)
    gender = Optional(str)
    message_ids = Set('VXMessage')


