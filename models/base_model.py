#!/usr/bin/python3
'''module
'''
import datetime
import uuid
import models


class BaseModel():
    '''class BaseModel'''
    def __init__(self, *args, **kwargs):
        '''init all ttributes except class'''
        if kwargs:
            for key, word in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        format = '%Y-%m-%dT%H:%M:%S.%f'
                        setattr(self, key, datetime.
                                datetime.strptime(word, format))
                    else:
                        setattr(self, key, word)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def __str__(self):
        '''string representation'''
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        '''update updated at attr and save changes'''
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        '''obj to dict'''
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == 'created_at' or key == 'updated_at':
                dict_copy[key] = value.isoformat()
        return dict_copy
