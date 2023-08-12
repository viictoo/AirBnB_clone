#!/usr/bin/python3
'''tests for the `place` module'''

import unittest
from models.place import Place
from unittest.mock import patch
from models.base_model import BaseModel
import models


class TestPlace(unittest.TestCase):
    '''Tests for the Place class'''

    @classmethod
    def setUp(cls):
        cls.my_place = Place()

    @classmethod
    def tearDown(cls) -> None:
        del cls.my_place

    def test_docstring(self):
        self.assertIsNotNone(Place.__doc__)

    def test_module_doc(self):
        self.assertIsNotNone(models.place.__doc__)

    def test_has_all_attributes(self):
        self.assertTrue(hasattr(self.my_place, 'city_id'))
        self.assertTrue(hasattr(self.my_place, 'user_id'))
        self.assertTrue(hasattr(self.my_place, 'name'))
        self.assertTrue(hasattr(self.my_place, 'description'))
        self.assertTrue(hasattr(self.my_place, 'number_rooms'))
        self.assertTrue(hasattr(self.my_place, 'number_bathrooms'))
        self.assertTrue(hasattr(self.my_place, 'max_guest'))
        self.assertTrue(hasattr(self.my_place, 'price_by_night'))
        self.assertTrue(hasattr(self.my_place, 'latitude'))
        self.assertTrue(hasattr(self.my_place, 'longitude'))
        self.assertTrue(hasattr(self.my_place, 'amenity_ids'))

    def test_inherits_from_BaseClass(self):
        self.assertIsInstance(self.my_place, BaseModel)
        self.assertTrue(issubclass(self.my_place.__class__, BaseModel), True)

    def test_str_repr(self):
        str_repr = str(self.my_place)
        self.assertIn('[Place]', str_repr)
        self.assertIn(self.my_place.id, str_repr)

    @patch('models.storage')
    def test_save(self, mock_storage):
        self.my_place.save()
        self.assertIsNotNone(self.my_place.updated_at)
        mock_storage.save.assert_called()

    def test_to_dict(self):
        a = self.my_place.to_dict()
        self.assertEqual(a['__class__'], 'Place')
        self.assertEqual(a['id'], self.my_place.id)
        self.assertEqual(a['created_at'], self.my_place.created_at.isoformat())

    def test_attribute_longitude(self):
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        self.assertEqual(place.longitude, 0.0)
        self.assertTrue(type(place.longitude) == float)


if __name__ == '__main__':
    unittest.main()
