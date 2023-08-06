#!/usr/bin/python3

import json
from models.base_model import BaseModel

class FileStorage:

    def __init__(self):

        self.__file_path = 'file.json'
        self.__objects = {}

    def all(self):

        return self.__objects

    def new(self, obj):

        if obj:
            key = f'{obj.__class__.__name__}.{obj.id}'
            self.__objects[key] = obj

    def save(self):

        save_dict = {}
        for key, obj in self.__objects.items():
            '''if type(obj) is dict:'''
            save_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(save_dict, f)

    def reload(self):

        try:
            with open(self.__file_path, 'r') as f:
                str_oj = json.load(f)
            for value in str_oj.values():
                class_v = value['__class__']
                self.new(eval(class_v)(**value))
        except FileNotFoundError:
            pass
