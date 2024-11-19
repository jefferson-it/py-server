from utils.db.models.Collection import *
import datetime

class Users(Collection):
    def __init__(self, name):
        super().__init__(name)
        super().create_col()
        super().set_validation({
            "name": {
                "type": str,
                "required": True
            },
            "age": {
                "type": int,
                "required": True
            },
            "creation_date": {
                "type": int,
                "default": datetime.datetime.now()
            }
        })

    def find_many(self, query: dict, opts: dict = None):
        return super().find_many(query, opts)
    
    def find_one(self, query: dict):
        return super().find_one(query)
    
    def insert_one(self, data):
        return super().insert_one(data)