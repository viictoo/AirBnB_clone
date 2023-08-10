#!/user/bin/python3
from models.base_model import BaseModel


class City(BaseModel):
    '''A city in the appliication

    Attributes:
           name
           state_id
    '''
    state_id = ""
    name = ""
