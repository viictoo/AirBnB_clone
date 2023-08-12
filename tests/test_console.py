#!/usr/bin/python3
'''Test Console Module'''

import io
import sys
import json
import models
import console
import unittest
import pycodestyle
from os import remove
from uuid import UUID
from os.path import isfile
from datetime import datetime
from io import StringIO as SIO
from console import HBNBCommand
from models.base_model import BaseModel
from unittest.mock import create_autospec, patch


class TestConsole(unittest.TestCase):
    """unit tests for the console
    """
    def setUp(self):
        """set up test tools
        """
        self.SimIn = HBNBCommand()
        self.out = SIO()

    def tearDown(self):
        """destroy created test elements
        """
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_docstrings(self):
        """Test docstrings exist in console.py"""
        self.assertTrue(len(console.__doc__) >= 1)

    def test_emptyline(self):
        """Test no user input"""
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("\n")
            self.assertEqual(SimOut.getvalue(), '')

    def test_quit(self):
        """test quit command."""
        with patch('sys.stdout', SIO()) as SimOut:
            self.assertTrue(self.SimIn.onecmd("quit"))
            self.assertTrue(self.SimIn.onecmd("quit now"))

            self.assertFalse(self.SimIn.onecmd("Exit"))
            self.assertEqual('*** Unknown syntax: Exit\n', SimOut.getvalue())

    def test_EOF(self):
        """test quit command."""
        with patch('sys.stdout', SIO()) as SimOut:
            self.assertTrue(self.SimIn.onecmd("EOF"))

    def test_create_error(self):
        """test quit command."""
        with patch('sys.stdout', SIO()) as SimOut:
            self.assertFalse(self.SimIn.onecmd("create"))
            self.assertEqual('** class name missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("create model"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("create Basemodel"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("create BaseModel again"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())

    def test_create_success(self):
        models.storage._FileStorage__objects.clear()
        with patch('sys.stdout', SIO()) as SimOut:
            '''create BaseModel instances'''
            self.SimIn.onecmd("create BaseModel")
            self.SimIn.onecmd("create BaseModel")
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("BaseModel.all()")
            # self.assertGreater(len(SimOut.getvalue()), len([]))
            # self.assertIsNot(SimOut.getvalue(), [])
            output = SimOut.getvalue().strip()
            # Confirm output is not Empty
            self.assertNotEqual(output, "[]")

            # Check if the output starts and ends with expected text
            self.assertTrue(output.startswith('["['))
            self.assertTrue(output.endswith('"]'))

    def test_show_error(self):
        """test quit command."""
        with patch('sys.stdout', SIO()) as SimOut:
            self.assertFalse(self.SimIn.onecmd("show"))
            self.assertEqual('** class name missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("show ModelDoesNotExist"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("show ModelDoesNotExist 123"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("show BaseModel"))
            self.assertEqual("** instance id missing **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("show BaseModel User"))
            self.assertEqual("** no instance found **\n", SimOut.getvalue())

    def test_show_default_error(self):
        """test quit command."""
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("''.show()")
            self.assertEqual(
                "*** Unknown syntax: ''.show()\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("ModelDoesNotExist.show(id)"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("BaseModel.show(123)"))
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd('BaseModel.show("string")'))
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd(
                "BaseModel.show(this is a long input)"))
            self.assertEqual("** no instance found **\n", SimOut.getvalue())

    def test_show_success(self):
        with patch('sys.stdout', SIO()) as SimOut:
            # Create an instance of Place
            self.SimIn.onecmd('create Place')
            output = SimOut.getvalue().strip()

            # Extract the instance ID from the output
            instance_id = output

        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd(f'show Place {instance_id}')
            show_output = SimOut.getvalue().strip()

            # Check if the output contains the expected attributes
            self.assertTrue(show_output.startswith("[Place"))
            self.assertIn(instance_id, show_output)
            self.assertIn("'created_at': datetime.datetime", show_output)
            self.assertIn("'updated_at': datetime.datetime", show_output)

    def test_show_default_success(self):
        with patch('sys.stdout', SIO()) as SimOut:
            # Create an instance of Place
            self.SimIn.onecmd('create Place')
            output = SimOut.getvalue().strip()

            instance_id = output

        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd(f'Place.show({instance_id})')
            show_output = SimOut.getvalue().strip()

            self.assertTrue(show_output.startswith("[Place"))
            self.assertIn(instance_id, show_output)
            self.assertIn("'created_at': datetime.datetime", show_output)
            self.assertIn("'updated_at': datetime.datetime", show_output)

    def test_destroy_error(self):
        """test destroy command."""
        models.storage._FileStorage__objects.clear()
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("''.destroy()")
            self.assertEqual(
                "*** Unknown syntax: ''.destroy()\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd(
                "ModelDoesNotExist.destroy(id)"))
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd("BaseModel.destroy(101)"))
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd('BaseModel.destroy("string")')
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("BaseModel.destroy(this is a long input)")
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("destroy")
            self.assertEqual("** class name missing **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("destroy User")
            self.assertEqual("** instance id missing **\n", SimOut.getvalue())

    def test_destroy_success(self):
        with patch('sys.stdout', SIO()) as SimOut:
            # Create an instance of Place
            self.SimIn.onecmd('create Place')
            instance_id = SimOut.getvalue().strip()
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd('create Place')
            instance2_id = SimOut.getvalue().strip()
            SimOut.truncate(0)
            SimOut.seek(0)
            # Extract the instance ID from the output

        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd(f'destroy Place {instance_id}')
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'show Place {instance_id}')
            show_output = SimOut.getvalue().strip()
            self.assertEqual("** no instance found **", show_output)
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'Place.destroy({instance2_id})')
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'Place.show({instance2_id})')
            show_output2 = SimOut.getvalue().strip()
            self.assertEqual("** no instance found **", show_output2)

    def test_all(self):
        models.storage._FileStorage__objects.clear()
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("all FakeModel")
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("all more FakeModel to test")
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())

        with patch('sys.stdout', SIO()) as SimOut:
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd("Place.all()")
            output = SimOut.getvalue().strip()
            # Confirm output is Empty
            self.assertEqual(output, "[]")
            self.SimIn.onecmd("create Place")
            self.SimIn.onecmd("create Place")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("Place.all()")
            output = SimOut.getvalue().strip()
            # Check if the output starts and ends with expected text
            self.assertTrue(output.startswith('["['))
            self.assertTrue(output.endswith('"]'))

    def test_all_default(self):
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("FakeModel.all()")
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("This FakeModel.all()")
            output = SimOut.getvalue()
            self.assertEqual(
                "*** Unknown syntax: This FakeModel.all()\n", output)

        with patch('sys.stdout', SIO()) as SimOut:
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd("User.all()")
            output = SimOut.getvalue().strip()
            # Confirm output is Empty
            self.assertEqual(output, "[]")
            self.SimIn.onecmd("create User")
            self.SimIn.onecmd("create User")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("User.all()")
            output = SimOut.getvalue().strip()
            # Check if the output starts and ends with expected text
            self.assertTrue(output.startswith('["['))
            self.assertTrue(output.endswith('"]'))

    def test_all_no_arg(self):
        """test all with no arguments"""
        with patch('sys.stdout', SIO()) as SimOut:
            """clear all objects"""
            models.storage._FileStorage__objects.clear()
            self.assertFalse(self.SimIn.onecmd('all'))
            self.assertEqual('[]\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd('create User'))
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd('all'))
            """confirm object list is created successfully"""
            objects = json.loads(SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertEqual(len(objects), 1)
            self.assertIsInstance(objects, list)
            for item in objects:
                self.assertIsInstance(item, str)
            self.SimIn.onecmd('create City')
            self.SimIn.onecmd('create BaseModel')
            self.SimIn.onecmd('create Amenity')
            self.SimIn.onecmd('create Place')
            self.SimIn.onecmd('create State')
            self.SimIn.onecmd('create Review')
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd('all'))
            self.assertIn("BaseModel", SimOut.getvalue())
            self.assertIn("City", SimOut.getvalue())
            self.assertIn("Place", SimOut.getvalue())
            self.assertIn("State", SimOut.getvalue())
            self.assertIn("Review", SimOut.getvalue())
            objects = json.loads(SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertIsInstance(objects, list)
            self.assertEqual(len(objects), 7)
            for item in objects:
                self.assertIsInstance(item, str)

    def test_count(self):
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("count FakeModel")
            self.assertEqual(
                "*** Unknown syntax: count FakeModel\n", SimOut.getvalue())

        with patch('sys.stdout', SIO()) as SimOut:
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd("City.count()")
            output = SimOut.getvalue().strip()
            # Confirm output is Empty
            self.assertEqual(output, '0')
            self.SimIn.onecmd("create City")
            self.SimIn.onecmd("create City")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("City.count()")
            output = SimOut.getvalue()
            # Check if count is 2
            self.assertEqual(output, '2\n')

    def test_count_error(self):
        with patch('sys.stdout', SIO()) as SimOut:
            self.SimIn.onecmd("count FakeModel")
            self.assertEqual(
                "*** Unknown syntax: count FakeModel\n", SimOut.getvalue())

        with patch('sys.stdout', SIO()) as SimOut:
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd("Cit.count()")
            output = SimOut.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("count Cities")
            output = SimOut.getvalue().strip()
            self.assertEqual(output, "*** Unknown syntax: count Cities")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(".count()")
            output = SimOut.getvalue().strip()
            self.assertEqual(output, "*** Unknown syntax: .count()")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("City.count(123)")
            output = SimOut.getvalue().strip()
            self.assertEqual(output, "*** Unknown syntax: City.count(123)")
            SimOut.truncate(0)
            SimOut.seek(0)

    def test_update_attributes(self):
        """test update attributes success"""
        with patch('sys.stdout', SIO()) as SimOut:
            """clear all objects"""
            models.storage._FileStorage__objects.clear()
            self.assertFalse(self.SimIn.onecmd('all'))
            self.assertEqual('[]\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd('create User')
            userId = SimOut.getvalue()
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'show User {userId}')
            self.assertNotIn("Maximus", SimOut.getvalue())
            self.SimIn.onecmd(f'update User {userId} "name" "Maximus"')
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'show User {userId}')
            self.assertIn("Maximus", SimOut.getvalue())
            self.SimIn.onecmd(f'update User {userId} "Weight" 100 "Age" "old"')
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'show User {userId}')
            self.assertIn('100', SimOut.getvalue())

    def test_update_error(self):
        """test update attributes success"""
        with patch('sys.stdout', SIO()) as SimOut:
            """clear all objects"""
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd('create User')
            userId = SimOut.getvalue()
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update')
            self.assertEqual(
                '** class name missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update User')
            self.assertEqual(
                '** instance id missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update User {userId}')
            self.assertEqual(
                '** attribute name missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update User 101 "name" "Maximus"')
            self.assertEqual('** no instance found **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update User {userId} "name"')
            self.assertEqual('** value missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(
                f'update User, {userId}, "Weight", 100 "Age" "old"')
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'update User 123')
            self.assertEqual("** no instance found **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'MaUser.update(123)')
            self.assertEqual("** class doesn't exist **\n", SimOut.getvalue())

    def test_default_update_error(self):
        """test update attributes success"""
        with patch('sys.stdout', SIO()) as SimOut:
            """clear all objects"""
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd('create User')
            userId = SimOut.getvalue().strip("\n")
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'.update')
            self.assertEqual(
                '*** Unknown syntax: .update\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'User.update')
            self.assertEqual(
                '*** Unknown syntax: User.update\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'User.update()')
            self.assertEqual(
                '*** Unknown syntax: User.update()\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("User.update(125)")
            self.assertEqual('** no instance found **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(
                "User.update(125, {'sum': 'count', 'muliply':'product'})")
            self.assertEqual('** no instance found **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.assertFalse(self.SimIn.onecmd(f'User.update({userId})'))
            self.assertEqual(
                "** attribute name missing **\n", SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd('User.update("11", "greeting")')
            self.assertEqual('** no instance found **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'User.update({userId}, "greeting")')
            self.assertEqual('** value missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'User.update({userId}, "greeting")')
            self.assertEqual('** value missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd('User.update({userId, "greeting"})')
            self.assertEqual('** no instance found **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(f'User.update({userId}, {"greeting"})')
            self.assertEqual('** value missing **\n', SimOut.getvalue())
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd(
                f'User.update({userId}, {"greeting", "Jambo", "100"})')
            self.assertEqual('', SimOut.getvalue())
            # self.assertRaises(TypeError)

    def test_update_dictionary(self):
        """test update attributes success"""
        with patch('sys.stdout', SIO()) as SimOut:
            """clear all objects"""
            models.storage._FileStorage__objects.clear()
            self.SimIn.onecmd('create Place')
            userId = SimOut.getvalue()
            SimOut.truncate(0)
            SimOut.seek(0)
            self.SimIn.onecmd("Place.update\
                              ("+userId+", {'Age': 100, 'Heritage': old'}")
            self.assertIn("Heritage", SimOut.getvalue())
            self.assertIn("Age", SimOut.getvalue())
            self.assertIn("old", SimOut.getvalue())


if __name__ == "__main__":
    unittest.main()
