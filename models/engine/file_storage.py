#!/usr/bin/python3
'''The file_storage module'''

import json
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class FileStorage:
    '''FileStorage performs serialization and deserilization'''

    __file_path = 'file.json'
    __objects = {}
    all_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "Amenity": Amenity,
        "City": City,
        "Review": Review,
        "State": State
    }

    def all(self):
        '''Return all objects of the class'''
        return self.__objects

    def new(self, obj):
        '''Adds new object to the __objects'''
        if obj:
            key = f'{obj.__class__.__name__}.{obj.id}'
            self.__objects[key] = obj

    def save(self):
        '''Serialization step'''
        save_dict = {}
        for key, obj in self.__objects.items():
            '''if type(obj) is dict:'''
            save_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(save_dict, f)

    def reload(self):
        '''Deserilaization step'''
        try:
            with open(self.__file_path, 'r') as f:
                str_oj = json.load(f)
            for key, value in str_oj.items():
                class_v = self.all_classes[value['__class__']](**value)
                self.__objects[key] = class_v
        except FileNotFoundError:
            pass
