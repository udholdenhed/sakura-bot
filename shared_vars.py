import json
import logging

from btypes.chats import Chats

from database.database import Database
from database.redis_database import RedisDatabase
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

# CHATS
chats = Chats()

# DATABASE
database: Database = RedisDatabase(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

# CITIES
try:
    with open('cities.json') as f:
        cities = json.load(f)
except Exception as _ex:
    logging.error(_ex)

users_who_change_city = {}
