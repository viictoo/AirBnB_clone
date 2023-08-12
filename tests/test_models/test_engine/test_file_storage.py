#!/usr/bin/python3
"""unittessts module
"""
import os
import models
import unittest
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from unittest.mock import patch, mock_open
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """test cases for the FileStorage class"""

    def setUp(self):
        """instance for use in testing"""
        self.FileStorage = FileStorage()
        self.storage = FileStorage()

    def tearDown(self):
        """_summary_
        """
        FileStorage._FileStorage__objects = {}
        if os.path.exists('file.json'):
            os.remove('file.json')

    def test_module_docstring(self):
        """_summary_
        """
        self.assertIsNotNone(FileStorage.__doc__)
        self.assertNotEqual(FileStorage.__doc__, "")

    def test_all_returns_dict_type(self):
        """test that created object is a dictionary"""
        ret_value = self.FileStorage.all()
        self.assertIsInstance(ret_value, dict)
        self.assertIsNotNone(ret_value)

    def test_new_adds_class_obj(self):
        """test new"""
        my_obj = User()
        self.FileStorage.new(my_obj)
        key = "{}.{}".format(my_obj.__class__.__name__, my_obj.id)
        self.assertEqual(self.FileStorage.all()[key], my_obj)

    @patch('json.dump')
    def test_save_writes_to_file(self, mock_dump):
        """tests if saves to file.json"""
        with patch('builtins.open', mock_open()) as mock_file:
            self.FileStorage.save()
            mock_file.assert_called_once_with('file.json', 'w')
            mock_dump.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_reload_from_file(self, mock_load, mock_open):
        """_summary_

        Args:
            mock_load (_type_): _description_
            mock_open (_type_): _description_
        """
        # Create a BaseModel instance and store it
        baseModel = BaseModel()
        self.FileStorage.new(baseModel)
        self.FileStorage.save()
        # Mock the JSON data for reloading
        mock_load.return_value = {
            "{}.{}".format(baseModel.__class__.__name__, baseModel.id):
                baseModel.to_dict()
        }
        # Create a new FileStorage instance and reload from mock data
        file_storage = FileStorage()
        file_storage.reload()
        # Check if the instance has been reloaded correctly
        key = f'{baseModel.__class__.__name__}.{baseModel.id}'
        self.assertIn(key, file_storage._FileStorage__objects)

    def test_reload_error_nonexistent_file(self):
        """_summary_
        """
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            self.FileStorage.reload()

    def test_save_reload_all_classes(self):
        """_summary_
        """
        instances = [
            BaseModel(),
            User(),
            State(),
            City(),
            Amenity(),
            Place(),
            Review()
        ]

        for instance in instances:
            self.FileStorage.new(instance)
            self.FileStorage.save()

            # Clear object and reload from file
            self.FileStorage._FileStorage__objects = {}
            self.FileStorage.reload()

        # Check if reloaded objects match original instances
        for instance in instances:
            key = "{}.{}".format(instance.__class__.__name__, instance.id)
            reloaded_instance = self.FileStorage.all()[key]
            self.assertIsInstance(reloaded_instance, instance.__class__)
            self.assertEqual(reloaded_instance.to_dict(),
                             instance.to_dict())

    def test_class_d(self):
        """_summary_
        """
        self.assertIsNotNone(FileStorage.__doc__)

    def test_module_d(self):
        """_summary_
        """
        self.assertIsNotNone(models.engine.file_storage.__doc__)

    def test_clas(self):
        """_summary_
        """
        self.assertIsNotNone(FileStorage.__doc__)

    def test_initial_attr(self):
        """Test it is a dictionary"""
        self.assertEqual(self.storage._FileStorage__file_path, "file.json")
        self.assertIsInstance(self.storage._FileStorage__objects, dict)

    def test_all_meth(self):
        """Test the all method"""
        obj = self.storage.all()
        self.assertIsInstance(obj, dict)
        self.assertIs(obj, self.storage._FileStorage__objects)

    def test_new_meth(self):
        """Test the new method"""
        bass = BaseModel()
        self.storage.new(bass)
        key = "{}.{}".format(bass.__class__.__name__, bass.id)
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_new_user(self):
        """Test the new method with user"""
        uss = User()
        self.storage.new(uss)
        key = "{}.{}".format(uss.__class__.__name__, uss.id)
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_reload(self):
        """Test the reload method"""
        bass = BaseModel()
        self.storage.new(bass)
        self.storage.save()
        with open("file.json", "r") as file:
            text = file.read()
            self.assertIn("BaseModel." + bass.id, text)

        bass.name = "Updated name"
        bass.save()

        stor = FileStorage()
        stor.reload()
        key = "{}.{}".format(bass.__class__.__name__, bass.id)
        self.assertIn(key, self.storage._FileStorage__objects)
        reloaded_ins = stor.all()[key]


if __name__ == '__main__':
    unittest.main()
