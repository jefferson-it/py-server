
from utils.db.models import Collection, Users
from utils.list import find


class DataBase:
    def __init__(self):
        self.collections = [ ]
        pass

    def collection(self, name: str) -> Collection:
        if not isinstance(self.collections, (list, dict)):
            raise TypeError("self.collections must be a list or dictionary")

        col = find(self.collections, lambda x: x.name == name)

        return col
    
    def set_col(self, Col: Collection):
        self.collections.append(Col)

database: DataBase = DataBase()

database.set_col(Users.Users("users"))
