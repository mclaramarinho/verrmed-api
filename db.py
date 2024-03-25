import datetime
from pymongo.collection import Collection
from pymongo import MongoClient
from dotenv import load_dotenv
from os import environ

load_dotenv()

client = MongoClient(environ["ATLAS_URI"])
db = client.get_database(environ["DB_NAME"])


class DBCollection:
    collection: Collection
    name: str

    def __init__(self, path: str):
        if 'substAtivas' in path:
            self.collection = db['activeSubst']
            self.name = 'activeSubst'

        elif 'substInativas' in path:
            self.collection = db['inactiveSubst']
            self.name = 'inactiveSubst'

        elif 'nomesComerciais' in path:
            self.collection = db['comName']
            self.name = 'comName'

        elif 'medicamentos' in path:
            self.collection = db['drugs']
            self.name = 'drugs'

    def register_update(self):
        now = f'{datetime.datetime.utcnow().isoformat()}Z'
        db['updates'].update_one({"collection": self.name}, {'$set': {"last_update": now}}, upsert=True)
