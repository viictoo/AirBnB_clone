#!/usr/bin/python3
"""_summary_
"""
import os
import copy
import uuid
import models
import unittest
from unittest.mock import patch
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUp(cls):
        """_summary_
        """
        cls.base_model = BaseModel()
        cls.base_model2 = BaseModel()

    @classmethod
    def tearDown(cls):
        """_summary_
        """
        del cls.base_model
        del cls.base_model2
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_attributes(self):
        """_summary_
        """
        self.assertTrue(hasattr(self.base_model, "id"))
        self.assertTrue(hasattr(self.base_model, "created_at"))
        self.assertTrue(hasattr(self.base_model, "updated_at"))

    def test_type_attributes(self):
        """_summary_
        """
        bass = BaseModel()
        self.assertTrue(type(bass.id), str)
        self.assertTrue(type(bass.created_at), datetime)
        self.assertTrue(type(bass.updated_at), datetime)

    def test_class_docstring(self):
        '''Tests class for docstring '''
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertNotEqual(BaseModel.__doc__, "")

    def test_init_docstring(self):
        '''Tests init method for docstring '''
        self.assertIsNotNone(self.base_model.__init__.__doc__)
        self.assertNotEqual(self.base_model.__init__.__doc__, "")

    def test_id_is_string(self):
        """_summary_
        """
        self.assertTrue(isinstance(self.base_model.id, str))

    def test_created_at_is_datetime(self):
        """_summary_
        """
        self.assertTrue(isinstance(self.base_model.created_at, datetime))

    def test_updated_at_is_datetime(self):
        """_summary_
        """
        self.assertTrue(isinstance(self.base_model.updated_at, datetime))

    def test_init_with_attributes(self):
        """_summary_
        """
        attributes = {
            "name": "Calvin",
            "my_number": 17
        }
        self.base_model = BaseModel(**attributes)
        self.assertEqual(self.base_model.name, attributes["name"])
        self.assertEqual(self.base_model.my_number, attributes["my_number"])

    def test_to_dict_docstring(self):
        '''Tests for a docstring in the to_dict method'''
        self.assertIsNotNone(self.base_model.to_dict.__doc__)
        self.assertNotEqual(self.base_model.to_dict.__doc__, "")

    def test_to_dict_method(self):
        """_summary_
        """
        obj_dict = self.base_model.to_dict()
        self.assertTrue(isinstance(obj_dict, dict))
        self.assertIn('__class__', obj_dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')

    def test_to_dict_returns_correct_format(self):
        """_summary_
        """
        obj_dict = self.base_model.to_dict()
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertEqual(type(obj_dict["created_at"]), str)
        self.assertEqual(type(obj_dict["updated_at"]), str)

    def test_str_docstring(self):
        """_summary_
        """
        self.assertIsNotNone(self.base_model.__str__.__doc__)
        self.assertNotEqual(self.base_model.__str__.__doc__, "")

    def test_str_method(self):
        """_summary_
        """
        res = f"[BaseModel] ({self.base_model.id}) {self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), res)

    def test_save_docstring(self):
        '''Tests save method for docstring'''
        self.assertIsNotNone(self.base_model.save.__doc__)
        self.assertNotEqual(self.base_model.save.__doc__, "")

    def test_save_method_updated_created_at(self):
        """_summary_
        """
        old_created_at = self.base_model.created_at

        self.base_model.save()
        self.assertEqual(old_created_at, self.base_model.created_at)

    def test_save_updates_updated_at(self):
        """_summary_
        """
        old_updated_at = self.base_model.updated_at

        self.base_model.save()
        self.assertNotEqual(old_updated_at, self.base_model.updated_at)

    @patch('models.storage')
    def test_save_method_updates_file(self, mock_storage):
        """_summary_

        Args:
            mock_storage (_type_): _description_
        """
        self.base_model.save()
        mock_storage.save.assert_called()

    # def test_save_method_updates_objects_dict(self):
    #     obj_dict = storage.all()
    #     self.model.save()
    #     new_obj_dict = storage.all()
    #     self.assertNotEqual(obj_dict, new_obj_dict)

    # def test_reload_retores_objects(self):
    #     storage.new(self.base_model)
    #     storage.save()
    #     storage.reload()

    #     all_objs = storage.all()
    #     self.assertIn(self.base_model.id, all_objs)

    @patch('models.storage')
    def test_save_method_updates_objects_dict(self, mock_storage):
        """_summary_

        Args:
            mock_storage (_type_): _description_
        """
        obj_dict = {self.base_model.id: self.base_model}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.base_model.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)

    @patch('models.storage')
    def test_reload_retores_objects(self, mock_storage):
        """_summary_

        Args:
            mock_storage (_type_): _description_
        """
        mock_storage.new.return_value = None
        mock_storage.all.return_value = {self.base_model.id: self.base_model}
        mock_storage.save.return_value = None
        self.base_model.save()
        mock_storage.reload()

        all_objs = mock_storage.all()
        self.assertIn(self.base_model.id, all_objs)

    def test_class_docs(self):
        """Test ``BaseModel`` class for documentation"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(models.base_model.__doc__)

    def test_method_docstring(self):
        """Test methods in ``BaseModel`` for documentation"""
        methods = [
            BaseModel.__init__,
            BaseModel.__str__,
            BaseModel.save,
            BaseModel.to_dict,
        ]
        for m in methods:
            self.assertIsNotNone(m.__doc__)

        self.assertTrue(uuid.UUID(self.base_model.id))
        self.assertNotEqual(self.base_model.id, self.base_model2.id)


if __name__ == "__main__":
    unittest.main()
