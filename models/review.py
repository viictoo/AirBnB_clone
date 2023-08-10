#!/usr/bin/python3
'''The `review` module

It defines one class, `review(),
which inherits from the 'BaseModel()` class
'''
from models.base_model import BaseModel


class Review(BaseModel):
    '''A review part of the application
    Attributes:
          place_id
          user_id
          text
    '''
    place_id = ""
    user_id = ""
    text = ""
