#!/usr/bin/python3
'''Tests for the review module'''

import unittest
from models.review import Review
from unittest.mock import patch
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    '''tests for the Review class'''

    @classmethod
    def setUp(cls):
        cls.review = Review()

    @classmethod
    def tearDown(cls) -> None:
        del cls.review

    def test_docstring(self):
        self.assertIsNotNone(Review.__doc__)

    def test_has_all_attributes(self):
        self.assertTrue(hasattr(self.review, 'place_id'))
        self.assertTrue(hasattr(self.review, 'user_id'))
        self.assertTrue(hasattr(self.review, 'text'))

    def test_type_attributes(self):
        self.assertTrue(isinstance(self.review.place_id, str))
        self.assertTrue(isinstance(self.review.user_id, str))
        self.assertTrue(isinstance(self.review.text, str))

    def test_inherits_from_BaseClass(self):
        self.assertIsInstance(self.review, BaseModel)
        self.assertTrue(issubclass(self.review.__class__, BaseModel), True)

    def test_str_repr(self):
        str_repr = str(self.review)
        self.assertIn('[Review]', str_repr)
        self.assertIn(self.review.id, str_repr)

    @patch('models.storage')
    def test_save(self, mock_storage):
        self.review.save()
        self.assertIsNotNone(self.review.updated_at)
        mock_storage.save.assert_called()

    def test_to_dict(self):
        obj = self.review.to_dict()
        self.assertEqual(obj['__class__'], 'Review')
        self.assertEqual(obj['id'], self.review.id)
        self.assertEqual(obj['created_at'], self.review.created_at.isoformat())


if __name__ == '__main__':
    unittest.main()
