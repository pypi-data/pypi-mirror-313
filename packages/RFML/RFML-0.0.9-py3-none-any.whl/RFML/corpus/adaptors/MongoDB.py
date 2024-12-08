import pymongo

from RFML.interface.ICorpusAdaptor import ICorpusAdaptor


class MongoDB(ICorpusAdaptor):

    def __init__(self, url, db):
        self.url = url
        self.db = db
        client = pymongo.MongoClient(url)
        self.database = client[db]

    def read(self, collection: str, child: str, query: str, callback):
        # try:
        ret = []
        _collection = self.database[collection]
        if child == "":
            ret = list(_collection.find(query))
        else:
            ret = list(_collection.find(query, {child}))
        return callback(ret, "read") if callback else ret

        # except OperationFailure as e:  # Exception as e:
        #     print(f"{e}")
        #     raise Exception(e)
        # except Exception as e:
        #     print(f"{e}")
        #     raise Exception(e)

    def save(self, collection: str, child: str, value: {}) -> bool:
        try:
            _collection = self.database[collection]
            _collection.insert_one(value)
            return True

        except Exception as e:
            if type(e) == TypeError: print("RFML ERROR: Failed to save data due to invalid JSON format!")
            return False

    def delete(self, collection: str, child: str, query: {}) -> str:
        _collection = self.database[collection]
        _collection.delete_one(query)  # {'id': '2'}
        pass

    def update(self, collection: str, child: str, query: {}, value: {}) -> str:
        _collection = self.database[collection]
        result = _collection.update_one(query, {'$set': value})
        return str(result.modified_count)

    def push(self, collection: str, child: str, query: {}, value: {}) -> str:
        _collection = self.database[collection]
        result = _collection.update_one(query, {'$push': value})
        return str(result.modified_count)

    def empty(self, collection: str, child: str, query: {}) -> str:
        _value = {"$set": {}}
        _collection = self.database[collection]
        _collection.update_one(query, _value)
        pass

    def is_empty(self, collection: str, query: {}) -> bool:
        _collection = self.database[collection]
        result = _collection.find(query)  # {"address": "Park Lane 38"}
        if result == {}:
            return True
        else:
            return False
        pass
