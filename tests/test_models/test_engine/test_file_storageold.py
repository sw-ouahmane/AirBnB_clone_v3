#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.__init__ import storage
import os
from os import environ


class test_fileStorage(unittest.TestCase):
    """Class to test the file storage method"""

    def setUp(self):
        """Set up test environment"""
        del_list = []
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """Remove storage file at end of tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_obj_list_empty(self):
        """__objects is initially empty"""
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """New object is correctly added to __objects"""
        new = BaseModel()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        for obj in storage.all().values():
            temp = obj
            self.assertTrue(temp is obj)

    def test_all(self):
        """__objects is properly returned"""
        new = BaseModel()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel save"""
        new = BaseModel()
        self.assertFalse(os.path.exists("file.json"))

    def test_empty(self):
        """Data is saved to file"""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        self.assertNotEqual(os.path.getsize("file.json"), 0)

    def test_save(self):
        """FileStorage save method"""
        new = BaseModel()
        storage.save()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        storage.save()
        storage.reload()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return

        for obj in storage.all().values():
            loaded = obj
            self.assertEqual(new.to_dict()["id"], loaded.to_dict()["id"])

    def test_reload_empty(self):
        """Load from an empty file"""
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        with open("file.json", "w") as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """Nothing happens if file does not exist"""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """BaseModel save method calls storage save"""
        new = BaseModel()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        new.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_type_path(self):
        """Confirm __file_path is string"""
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return

        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """Key is properly formatted"""
        new = BaseModel()
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        _id = new.to_dict()["id"]
        for key in storage.all().keys():
            temp = key
            self.assertEqual(temp, "BaseModel" + "." + _id)

    def test_storage_var_created(self):
        """FileStorage object storage created"""
        if environ.get("HBNB_TYPE_STORAGE") == "db":
            return
        from models.engine.file_storage import FileStorage

        print(type(storage))
        self.assertEqual(type(storage), FileStorage)
