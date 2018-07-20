from datetime import datetime

from pony.orm import *

from models import db
from models.vxuser import VXUser


class VXMessage(db.Entity):
    _table_ = 'message'

    id = PrimaryKey(int, auto=True)
    date = Required(datetime)
    text = Required(LongStr)
    user_id = Required(str)
    partner_id = Required(VXUser)

    @db_session
    def create(self, m):
        return VXMessage(m.message_id, m.date, m.text, m.from_user.id)

