#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from unittest.mock import patch

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    @patch('models.engine.db_storage.DBStorage.__session', autospec=True)
    def test_get(self, mock_session):
        # Mock session query method to return a state object
        mock_session.query().get.return_value = State(id='state_id', name='California')

        # Call get method
        state = models.storage.get(State, 'state_id')

        # Assertions
        self.assertIsNotNone(state)
        self.assertEqual(state.id, 'state_id')
        self.assertEqual(state.name, 'California')

    @patch('models.engine.db_storage.DBStorage.__session', autospec=True)
    def test_count(self, mock_session):
        # Mock session query method to return 3 state objects
        mock_session.query().count.return_value = 3

        # Call count method without class argument
        total_count = models.storage.count()

        # Assertions
        self.assertEqual(total_count, 3)

        # Call count method with State class argument
        state_count = models.storage.count(State)

        # Assertions
        self.assertEqual(state_count, 3)



class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @patch('models.engine.file_storage.FileStorage._FileStorage__objects', autospec=True)
    def test_get(self, mock_objects):
        # Mock __objects dictionary to contain a state object
        mock_objects.get.return_value = State(id='state_id', name='California')

        # Call get method
        state = models.storage.get(State, 'state_id')

        # Assertions
        self.assertIsNotNone(state)
        self.assertEqual(state.id, 'state_id')
        self.assertEqual(state.name, 'California')

    @patch('models.engine.file_storage.FileStorage._FileStorage__objects', autospec=True)
    def test_count(self, mock_objects):
        # Mock __objects dictionary to contain 3 state objects
        mock_objects.values.return_value = [State() for _ in range(3)]

        # Call count method without class argument
        total_count = models.storage.count()

        # Assertions
        self.assertEqual(total_count, 3)

        # Call count method with State class argument
        state_count = models.storage.count(State)

        # Assertions
        self.assertEqual(state_count, 3)
