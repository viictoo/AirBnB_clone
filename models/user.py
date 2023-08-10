#!/usr/bin/python3
'''The `user` module

It defines one class, `User()`,
which inherits the `BaseModel()` class.`
'''
from models.base_model import BaseModel


class User(BaseModel):
    ''' A user in the application
    Attribute
        email
        password
        first_name
        last_name
    '''

    email = ""
    password = ""
    first_name = ""
    last_name = ""
