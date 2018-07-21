from datetime import datetime

from pony.orm import *

from models import db
from models.vxuser import VXUser


class VXMessage(db.Entity):
    _table_ = 'vx_message'

    id = PrimaryKey(int, auto=True)
    message_id = Required(int, unique=True)
    user_id = Required(VXUser)
    chat_id = Required(int)
    date = Required(datetime)
    text = Required(LongStr)
    state = Required(str, default="0")
    read = Optional(bool)

    @db_session
    def create(self, message):
        return VXMessage(user_id=message.message_id, date=message.date, text=message.text, partner_id=message.from_user.id)

