import logging

from pony.orm import *

logger = logging.getLogger("VLIM Bot")

db = Database()

class User(db.Entity):
    _table_ = 'partner'

    id = PrimaryKey(int, auto=True)
    user_id = Required(int, unique=True)
    name = Required(str)
    first_name = Required(str)
    last_name = Required(str)
    language_code = Required(str)
    honorific_address = Required(str)
    full_name = Required(str)
    gender = Optional(str)


logger.info("Partner Model Difined")
db.bind(provider='postgres', user='vlimbot', password='asdfghjk', host='127.0.0.1', database='vlim_bot')
logger.info("Pony DB Bind")

db.generate_mapping(create_tables=True)
logger.info("DB Generated")
#
#
#
#
#

# class Partner(models.Model):
#     _table = 'partner'
#
#     def __init__(self):
#         super(Partner, self).__init__(id)
#         self.table = 'partner'
#         self.language_code = ''
#         self.first_name = ''
#         self.last_name = ''
#         self.name = ''
#         self.honorific_address = ''
#         self.full_name = ''
#
#     def save(self, user):
#         self.create(id=user.id, first_name=user.first_name, last_name=user.last_name, name=user.name,
#                     full_name=user.full_name)
#
#     def create(self, id, first_name, last_name, name, **kwargs):
#
#         self.language_code = 'en-KH'
#         self.id = id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.name = name
#         self.honorific_address = 'Sir'
#         self.full_name = kwargs['full_name'] if 'full_name' in kwargs else " "
#
#         data_ids = self.read()
#         row = self.get_csv_record_field()
#         data_ids.append(row)
#         self.write(data_ids)
#
#     def get(self, user):
#         if user.id in self.read_ids():
#             return 0
#         else:
#             self.save(user)
#
#     def update(self, id):
#         data_ids = self.read()
#
#
#     def set_honorific_address(self, honorific_address):
#         self.honorific_address = honorific_address.strip()
#
#     def get_csv_record_field(self):
#
#         return [
#             self.id,
#             self.first_name,
#             self.last_name,
#             self.full_name,
#             self.language_code,
#             self.name,
#             self.honorific_address,
#         ]
