#!/user/bin/python3
'''Tests for city module'''

import os
import unittest
from models.city import City
from models.engine.file_storage import FileStorage
import copy
from unittest.mock import patch


class TestUser(unittest.TestCase):
    '''Unittest for the `City` class.'''
    @classmethod
    def setUp(cls):
        '''creating object to used for the test'''
        cls.city = City()
        # self.storage = FileStorage

    @classmethod
    def tearDown(cls) -> None:
        '''Doing cleanup after all tests'''
        del cls.city

    def test_docstring(self):
        '''test for docstring of City class'''
        self.assertIsNotNone(City.__doc__)
        self.assertNotEqual(City.__doc__, "")

    def test_city_instances(self):
        '''Tests for city parameters'''
        self.assertIsInstance(self.city, City)
        self.assertTrue(hasattr(self.city, 'state_id'))
        self.assertTrue(hasattr(self.city, 'name'))

    def test_city_attributes(self):
        '''Tests for the values of the obj parameter'''
        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

    def test_city_state_id_type(self):
        '''Tests for the type of the state_id'''
        self.assertEqual(type(self.city.state_id), str)

    def test_city_name_type(self):
        '''Test for the type of name'''
        self.assertEqual(type(self.city.name), str)

    def test_city_to_dict(self):
        '''test for the to_dict method'''
        city_dict = self.city.to_dict()
        self.assertTrue(isinstance(city_dict, dict))
        self.assertIn('__class__', city_dict)
        self.assertEqual(city_dict['__class__'], 'City')

    def test_city_str_method(self):
        '''Test for the str method'''
        expected = "[City] ({}) {}".format(self.city.id, self.city.__dict__)
        self.assertEqual(str(self.city), expected)

    @patch('models.storage')
    def test_save(self, mock_storage):
        '''Tests for the save method'''
        self.city.save()
        self.assertIsNotNone(self.city.updated_at)
        mock_storage.save.assert_called()

    @patch('models.storage')
    def test_save_method_updates_objects_dict(self, mock_storage):
        '''Tests to check if save updates the original value of obj'''
        obj_dict = {self.city.id: self.city}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.city.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)


if __name__ == "__main__":
    unittest.main()
