from enum import Enum
from flask import json

class Mapper:
    @staticmethod
    def to_dict(obj):
        if isinstance(obj, list):
            return [Mapper._to_dict_single(item) for item in obj]
        else:
            return Mapper._to_dict_single(obj)
 
    @staticmethod
    def to_json(obj):
        return json.dumps(Mapper.to_dict(obj))    
    
  
    def _to_dict_single(obj):
        if hasattr(obj, '__dict__'):
            data = {key: Mapper._handle_value(getattr(obj, key)) for key in obj.__dict__.keys() if not key.startswith('_')}
            return data
        elif isinstance(obj, Enum):
            return obj.value  # Return the value of the Enum
        else:
            return obj  # handle non-object types
    

    def _handle_value(value):
        if isinstance(value, Enum):
            return value.value
        return value