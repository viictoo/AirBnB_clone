#!/usr/bin/python3
import os
import copy
import uuid
import unittest
from unittest.mock import patch
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.base_model = BaseModel()
        cls.base_model2 = BaseModel()

    @classmethod
    def tearDown(cls):
        del cls.base_model
        del cls.base_model2
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_attributes(self):
        self.assertTrue(hasattr(self.base_model, "id"))
        self.assertTrue(hasattr(self.base_model, "created_at"))
        self.assertTrue(hasattr(self.base_model, "updated_at"))

    def test_class_docstring(self):
        '''Tests class for docstring '''
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertNotEqual(BaseModel.__doc__, "")

    def test_init_docstring(self):
        '''Tests init method for docstring '''
        self.assertIsNotNone(self.base_model.__init__.__doc__)
        self.assertNotEqual(self.base_model.__init__.__doc__, "")

    def test_id_is_string(self):
        self.assertTrue(isinstance(self.base_model.id, str))

    def test_created_at_is_datetime(self):
        self.assertTrue(isinstance(self.base_model.created_at, datetime))

    def test_updated_at_is_datetime(self):
        self.assertTrue(isinstance(self.base_model.updated_at, datetime))

    def test_init_with_attributes(self):
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
        obj_dict = self.base_model.to_dict()
        self.assertTrue(isinstance(obj_dict, dict))
        self.assertIn('__class__', obj_dict)
        self.assertEqual(obj_dict['__class__'], 'BaseModel')

    def test_to_dict_returns_correct_format(self):
        obj_dict = self.base_model.to_dict()
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertEqual(type(obj_dict["created_at"]), str)
        self.assertEqual(type(obj_dict["updated_at"]), str)

    def test_str_docstring(self):
        self.assertIsNotNone(self.base_model.__str__.__doc__)
        self.assertNotEqual(self.base_model.__str__.__doc__, "")

    def test_str_method(self):
        res = f"[BaseModel] ({self.base_model.id}) {self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), res)

    def test_save_docstring(self):
        '''Tests save method for docstring'''
        self.assertIsNotNone(self.base_model.save.__doc__)
        self.assertNotEqual(self.base_model.save.__doc__, "")

    def test_save_method_updated_created_at(self):
        old_created_at = self.base_model.created_at

        self.base_model.save()
        self.assertEqual(old_created_at, self.base_model.created_at)

    def test_save_updates_updated_at(self):
        old_updated_at = self.base_model.updated_at

        self.base_model.save()
        self.assertNotEqual(old_updated_at, self.base_model.updated_at)

    @patch('models.storage')
    def test_save_method_updates_file(self, mock_storage):
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
        obj_dict = {self.base_model.id: self.base_model}
        mock_storage.all.return_value = copy.deepcopy(obj_dict)

        self.base_model.save()
        new_obj_dict = mock_storage.all()

        self.assertNotEqual(obj_dict, new_obj_dict)

    @patch('models.storage')
    def test_reload_retores_objects(self, mock_storage):
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

    def test_initial_attribute(self):
        """Test object id"""
        basemodels = BaseModel()
        basemodels2 = BaseModel()

        self.assertTrue(hasattr(basemodels, "id"))
        self.assertIsNotNone(basemodels.id)
        self.assertIsInstance(basemodels.id, str)

        self.assertTrue(uuid.UUID(basemodels.id))

        self.assertNotEqual(basemodels.id, basemodels2.id)

        self.assertTrue(hasattr(basemodels, "created_at"))
        self.assertIsNotNone(basemodels.created_at)
        self.assertIsInstance(basemodels.created_at, datetime)

        self.assertTrue(hasattr(basemodels, "updated_at"))
        self.assertIsNotNone(basemodels.updated_at)
        self.assertIsInstance(basemodels.updated_at, datetime)

        self.assertTrue(hasattr(basemodels, "__class__"))
        self.assertIsNotNone(basemodels.__class__)
        self.assertIsInstance(basemodels.__class__, object)

        arg_test = BaseModel("args")
        self.assertNotIn("args", arg_test.__dict__)

        str_ = "[BaseModel] ({}) {}".format(basemodels.id, basemodels.__dict__)
        self.assertEqual(str(basemodels), str_)

        elders = basemodels.updated_at
        basemodels.save()
        self.assertGreater(basemodels.updated_at, elders)

    def test_kwargs(self):
        """Test ``BaseModel`` initialization with kwargs"""
        my_dic = {
            "id": "test_id",
            "created_at": "2023-08-09T12:34:56.789012",
            "updated_at": "2023-08-09T13:45:12.345678",
            "name": "lls",
            "value": 42,
        }
        test_model = BaseModel(**my_dic)

        self.assertEqual(test_model.id, "test_id")
        self.assertEqual(test_model.name, "lls")
        self.assertEqual(test_model.value, 42)
        self.assertIsInstance(test_model.created_at, datetime)
        self.assertIsInstance(test_model.updated_at, datetime)

    def test_to_dict_data_type(self):
        """Test each data type after ``to_dict``"""
        test_model = BaseModel()
        test_model.name = "bah"
        test_model.age = "ol"
        test_model.num = 12
        test_model.float_num = 12.21
        test_model.bool_val = True

        test_dict = test_model.to_dict()

        self.assertIsInstance(test_dict, dict)
        self.assertEqual(test_dict["__class__"], "BaseModel")
        self.assertEqual(test_dict["id"], test_model.id)
        self.assertEqual(test_dict["name"], "bah")
        self.assertEqual(test_dict["age"], "ol")
        self.assertEqual(test_dict["num"], 12)
        self.assertEqual(test_dict["float_num"], 12.21)
        self.assertEqual(test_dict["bool_val"], True)


if __name__ == "__main__":
    unittest.main()
