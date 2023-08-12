#!/user/bin/python3
'''Tests for the amenity module'''

import os
import unittest
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
import copy
from unittest.mock import patch
from models.base_model import BaseModel
import models


class TestUser(unittest.TestCase):
    '''Unit tests for the Amenity class'''

    @classmethod
    def setUp(cls):
        cls.amenity = Amenity()
        # self.storage = FileStorage

    @classmethod
    def tearDown(cls) -> None:
        del cls.amenity

    def test_docstring(self):
        '''Tests for the docstring of the class'''
        self.assertIsNotNone(Amenity.__doc__)
        self.assertIsNotNone(models.amenity.__doc__)

    def test_amenity_instances(self):
        '''Tests for the obj of the class'''
        self.assertIsInstance(self.amenity, Amenity)
        self.assertTrue(hasattr(self.amenity, 'name'))

    def test_inherits_from_BaseClass(self):
        '''Test for inheritance from BaseModel'''
        self.assertIsInstance(self.amenity, BaseModel)
        self.assertTrue(issubclass(self.amenity.__class__, BaseModel), True)

    def test_amenity_attributes(self):
        '''Tests for the value of name attr'''
        self.assertEqual(self.amenity.name, "")

    def test_amenity_name_type(self):
        ''''tests for the type of name'''
        self.assertEqual(type(self.amenity.name), str)

    def test_amenity_to_dict(self):
        '''Tests for the to_dict method'''
        amenity_dict = self.amenity.to_dict()
        self.assertTrue(isinstance(amenity_dict, dict))
        self.assertIn('__class__', amenity_dict)
        self.assertEqual(amenity_dict['__class__'], 'Amenity')

    def test_amenity_str_method(self):
        '''Tests for the str method'''
        expected = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), expected)

    @patch('models.storage')
    def test_save(self, mock_storage):
        '''Test for the save method'''
        self.amenity.save()
        self.assertIsNotNone(self.amenity.updated_at)
        mock_storage.save.assert_called()

    @patch('models.storage')
    def test_save_method_updates_objects_dict(self, mock_storage):
        '''Test for the save method'''
        obj_dict = {self.amenity.id: self.amenity}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.amenity.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)


if __name__ == "__main__":
    unittest.main()
