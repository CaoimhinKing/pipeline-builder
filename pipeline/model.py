import json


class PipelineMetadata():
    def __init__(self, data):
        obj = json.loads(data)
        self.__dict__ = {}
        for key, value in obj.items():
            self.__dict__[key] = value
        
    def __getitem__(self, key):
        return self.__dict__[key]
