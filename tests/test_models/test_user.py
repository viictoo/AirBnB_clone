#!/user/bin/python3
'''Unit tests for the `user` module.
'''
import os
import copy
from unittest.mock import patch
import unittest
from models.user import User
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''Test cases for the `User` class.'''

    @classmethod
    def setUp(cls):
        '''used to created objects to be used in diiferent tests'''
        cls.user = User()
        # self.storage = FileStorage

    @classmethod
    def tearDown(cls) -> None:
        '''clear anything that was created after the test'''
        del cls.user
        # if os.path.exists("file.json"):
        #     os.remove("file.json")

    def test_docstring(self):
        ''''checks if class has a docstring'''
        self.assertIsNotNone(User.__doc__)
        self.assertNotEqual(User.__doc__, "")

    def test_user_instances(self):
        '''Tests for class attributes'''
        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))

    def test_user_attributes(self):
        '''tests for the initial values of class attributes'''
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_email_type(self):
        '''Test of the type of email attribute of the class'''
        self.assertEqual(type(self.user.email), str)

    def test_user_password_type(self):
        '''Tests for the type of password attribute'''
        self.assertEqual(type(self.user.password), str)

    def test_user_first_name_type(self):
        '''tests for the type attribute of first_name '''
        self.assertEqual(type(self.user.first_name), str)

    def test_user_last_name_type(self):
        '''Tests for the type of last_name'''
        self.assertEqual(type(self.user.last_name), str)

    def test_user_to_dict(self):
        '''Tests for the to_dict methods'''
        user_dict = self.user.to_dict()
        self.assertTrue(isinstance(user_dict, dict))
        self.assertIn('__class__', user_dict)
        self.assertEqual(user_dict['__class__'], 'User')

    def test_user_str_method(self):
        '''tests for the __str__ method'''
        expected = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(str(self.user), expected)

    # def test_user_save_updated_file(self):
    #     self.user.save()
    #     self.assertTrue(os.path.exist(self.storage._FileStorage__file_path))
    # def test_user_save_updates_objects_dict(self):
    #     objs_dict = self.storage.all()
    #     self.user.save()
    #     new_obj_dict = self.storage.all()
    #     self.assertNotEqual(objs_dict, new_obj_dict)

    @patch('models.storage')
    def test_save(self, mock_storage):
        '''tests for the save method'''
        self.user.save()
        self.assertIsNotNone(self.user.updated_at)
        mock_storage.save.assert_called()

    @patch('models.storage')
    def test_save_method_updates_objects_dict(self, mock_storage):
        '''tests to see if save method when called updates'''
        obj_dict = {self.user.id: self.user}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.user.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)


if __name__ == "__main__":
    unittest.main()
