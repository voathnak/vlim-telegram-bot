from pony.orm import *
from models import db


class VXSystemParameter(db.Entity):
    _table_ = 'vx_system_parameter'
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    value = Required(str)
