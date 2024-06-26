#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

import inspect
from models import user
from models.base_model import BaseModel
import unittest
User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""
    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        u = User(email="User1@mail.com", password='test')
        self.assertIsInstance(u, BaseModel)
        self.assertTrue(hasattr(u, "id"))
        self.assertTrue(hasattr(u, "created_at"))
        self.assertTrue(hasattr(u, "updated_at"))

    def test_email_attr(self):
        """Test that User has attr email, and it's an empty string"""
        u = User(email="User1@mail.com", password='test')
        self.assertTrue(hasattr(u, "email"))

    def test_password_attr(self):
        """Test that User has attr password, and it's an empty string"""
        u = User(email="User1@mail.com", password='test')
        self.assertTrue(hasattr(u, "password"))

    def test_first_name_attr(self):
        """Test that User has attr first_name, and it's an empty string"""
        u = User(email="User1@mail.com", password='test')
        self.assertTrue(hasattr(u, "first_name"))

    def test_last_name_attr(self):
        """Test that User has attr last_name, and it's an empty string"""
        u = User(email="User1@mail.com", password='test')
        self.assertTrue(hasattr(u, "last_name"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        u = User(email="User1@mail.com", password='test')
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User(email="User1@mail.com", password='test')
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        u = User(email="User1@mail.com", password='test')
        string = "[User] ({}) {}".format(u.id, u.__dict__)
        self.assertEqual(string, str(u))
