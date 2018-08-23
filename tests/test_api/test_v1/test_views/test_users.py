#!/usr/bin/python3
"""
Unittest for api/v1/view/users.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
from models.user import User
import json


class Test_User_API(unittest.TestCase):
    """Testing all routes in User API"""

    @classmethod
    def setUpClass(cls):
        """setup"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.basepath = "api/v1"

    @classmethod
    def tearDownClass(cls):
        """teardown"""
        pass

    def test_get_users(self):
        """test get HTTP request"""
        pass

    def test_get_user_by_id(self):
        """test get HTTP request"""
        pass

    def test_get_user_by_id_fail(self):
        """test get HTTP request"""
        pass

    def test_delete_id(self):
        """test delete HTTP request"""
        pass

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        pass

    def test_create(self):
        """test create HTTP request"""
        pass

    def test_create_fail_nojson(self):
        """test create HTTP request"""
        pass

    def test_create_fail_noemail(self):
        """test create HTTP request"""
        pass

    def test_create_fail_nopassword(self):
        """test create HTTP request"""
        pass

    def test_update_id(self):
        """test update HTTP request"""
        pass

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        pass

    def test_update_id_fail_nouser(self):
        """test update HTTP request"""
        pass


if __name__ == "__main__":
    unittest.main()
