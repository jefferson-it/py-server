from utils import file
from typing import Dict, TypedDict
import datetime
import json

from utils.list import find

CONST_ROOT_COL = f"{file.__dirname}/data/"

class Validator(TypedDict):
    type: type
    required: bool
    default: any

ValidatorParam = Dict[str, Validator]

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

class Collection:
    validator: ValidatorParam
    itens: list
    
    def __init__(self, name):
        self.name = name
    
    def valid_data(self, data: dict):
        keys_of_validator = self.validator.keys()
        final_data = {}

        for key in keys_of_validator:
            is_required = self.validator[key].get('required', False)
            expected_type = self.validator[key].get('type')
            default_value = self.validator[key].get('default')

            if (not key in data) and is_required:
                return f"Error, the key '{key}' is required"
            elif key in data and not isinstance(data[key], expected_type) and data[key] is not None:
                return f"Error, the key '{key}' expects {expected_type.__name__}"
            else:
                if key in data:
                    final_data[key] = data[key]
                elif "default" in self.validator[key]:
                    final_data[key] = default_value

        return final_data


    def set_validation(self, data: ValidatorParam ):
        self.validator = data
    
    def create_col(self):
       data = file.write_file(f"{CONST_ROOT_COL}/{self.name}.json", "[]")
       
       if data:
           self.itens = json.loads(data)
    
    def find_one(self, query: dict):
        keys = list(query.keys())
        values = list(query.values())

        def match(item):
            if not isinstance(item, dict):
                return False
            return all(item.get(key) == value for key, value in zip(keys, values))

        return next((item for item in self.itens if match(item)), None)

    def find_many(self, query: dict = None, opts: dict = None):
        opts = opts or {}
        limit = opts.get('limit', -1)
        skip = opts.get('skip', 0)

        filtered_items = []

        if query is None:
            filtered_items = self.itens[skip:]
        else:
            keys = list(query.keys())
            values = list(query.values())

            def match(item):
                if not isinstance(item, dict):
                    return False
                return all(item.get(key) == value for key, value in zip(keys, values))

            filtered_items = filter(match, self.itens[skip:])

        if limit == -1:
            return list(filtered_items)
        else:
            return list(filtered_items)[:limit]
        
        return filtered_items


    def save(self):
        data = file.overwrite_file(f"{CONST_ROOT_COL}/{self.name}.json", json.dumps(self.itens, cls=DateTimeEncoder, indent=3))
       
        if data:
           self.itens = json.loads(data)

    def insert_one(self, data):
        result = final_data = self.valid_data(data)

        if isinstance(result, str):
            return {
                'err': result
            }

        self.itens.append(final_data)

        self.save()
