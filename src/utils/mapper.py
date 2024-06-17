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
        return {key: getattr(obj, key) for key in obj.__dict__.keys() if not key.startswith('_')}