#!/usr/bin/python3
"""
Unittest for api/v1/view/places.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
from models.place import Place
from models.city import City
import json


class Test_Place_API(unittest.TestCase):
    """Testing all routes in Place API"""

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

    def test_get_place_by_city_id(self):
        """test get HTTP request"""
        pass

    def test_get_place_by_city_id_fail(self):
        """test get HTTP request"""
        pass

    def test_get_place_id(self):
        """test get HTTP request"""
        pass

    def test_get_place_id_fail(self):
        """test get HTTP request"""
        pass

    def test_delete_id(self):
        """test delete HTTP request"""
        pass

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        pass

    def test_create_place_by_city_id(self):
        """test create HTTP request"""
        pass

    def test_create_place_by_city_id_fail_nojson(self):
        """test create HTTP request"""
        pass

    def test_create_place_by_city_id_fail_noname(self):
        """test create HTTP request"""
        pass

    def test_create_place_by_city_id_fail_nouserID(self):
        """test create HTTP request"""
        pass

    def test_update_id(self):
        """test update HTTP request"""
        pass

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        pass

    def test_update_id_fail_noplace(self):
        """test update HTTP request"""
        pass


if __name__ == "__main__":
    unittest.main()
