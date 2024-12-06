import pymongo, logging, traceback

'''
mongo_db = MongoDB(database_name='scrapy_hashdata', uri='mongodb://localhost:27017/')
player_urls_collection = mongo_db.initialize_collection('french_player_urls')
url = 'https://tenup.fft.fr/palmares/110663353'
results = mongo_db.filter(query={}, projection={'_id': False, 'url': True}, collection=player_urls_collection)
results = mongo_db.filter(query={'url': {'$regex': '/tournoi/'}}, projection={'_id': False, 'url': True}, collection=player_urls_collection)
if not mongo_db.counts(query={'url': url}, collection=player_urls_collection)
    mongo_db.save(
        query=
        {
            'tournament_url': tournament_url,
            'tournament_name': tournament_name,
            'tournament_host': tournament_host,
            'tournament_city': tournament_city,
            'tournament_start_date': tournament_start_date,
            'tournament_end_date': tournament_end_date,
        },
        collection=french_tournament_details_collection
    )
'''

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class MongoDB():
    def __init__(self, database_name, uri):
        self.database_name = database_name
        self.uri = uri
        self.client = pymongo.MongoClient(self.uri)
        self.initialize_database()

    def initialize_database(self):
        try:
            self.db = self.client[self.database_name]
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')


    def initialize_collection(self, collection_name=None):
        collection = None
        try:
            if collection_name not in self.db.list_collection_names():
                collection = self.db.create_collection(collection_name)
            else:
                collection = self.db[collection_name]
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')
        return collection


    def delete_collection(self, collection=None):
        try:
            if collection.name in self.db.list_collection_names():
                collection.drop()
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')


    def create_index(self, name, collection=None):
        try:
            collection.create_index(name)
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')


    def save(self, query={}, collection=None):
        last_id = None
        try:
            last_id = collection.insert_one(query)
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')
        return last_id


    def counts(self, query={}, collection=None):
        totals = 0
        try:
            totals = collection.count_documents(query)
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')
        return totals


    def filter(self, query={}, projection={}, collection=None):
        results = []
        try:
            results = list(collection.find(query, projection))
        except :
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')
        return results


    def update(self, query={}, where={}, collection=None):
        try:
            collection.update_many(where, {"$set": query})
        except:
            logging.warning(f'⚠️\n{traceback.format_exc()}⚠️')

