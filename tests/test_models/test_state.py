#!/user/bin/python3
'''Unit tests for the `state` module
'''
import os
import copy
from unittest.mock import patch
import unittest
from models.state import State
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''Unitest for the State class.'''

    @classmethod
    def setUp(cls):
        cls.state = State()

    @classmethod
    def tearDown(cls) -> None:
        del cls.state
        # if os.path.exists("file.json"):
        #     os.remove("file.json")

    def test_docstring(self):
        '''Test for docstring for the State class'''
        self.assertIsNotNone(State.__doc__)
        self.assertNotEqual(State.__doc__, "")

    def test_state_paramteres(self):
        '''Tests for parameters for the State classs'''
        self.assertIsInstance(self.state, State)
        self.assertTrue(hasattr(self.state, 'name'))

    def test_state_attributes(self):
        '''test for attribute values'''
        self.assertEqual(self.state.name, "")
        self.assertTrue(isinstance(self.state.name, str))

    def test_state_name_type(self):
        '''Test for the type of name'''
        self.assertEqual(type(self.state.name), str)

    def test_state_to_dict(self):
        '''Tests for the to_dict method'''
        obj = self.state.to_dict()
        self.assertTrue(isinstance(obj, dict))
        self.assertIn('__class__', obj)
        self.assertEqual(obj['__class__'], 'State')
        self.assertEqual(obj['id'], self.state.id)
        self.assertEqual(obj['created_at'], self.state.created_at.isoformat())

    def test_state_str_method(self):
        '''Tests for the __str__ method'''
        expected = "[State] ({}) {}".format(self.state.id, self.state.__dict__)
        self.assertEqual(str(self.state), expected)

    @patch('models.storage')
    def test_save(self, mock_storage):
        '''Tests for the save method'''
        self.state.save()
        self.assertIsNotNone(self.state.updated_at)
        mock_storage.save.assert_called()

    @patch('models.storage')
    def test_save_method_updates_objects_dict(self, mock_storage):
        '''Tests if the save method updated the values of the dict obj'''
        obj_dict = {self.state.id: self.state}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.state.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)


if __name__ == "__main__":
    unittest.main()
