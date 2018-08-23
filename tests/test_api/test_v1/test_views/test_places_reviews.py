#!/usr/bin/python3
"""
Unittest for api/v1/view/reviews.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
from models.place import Place
from models.review import Review
import json


class Test_Place_Review_API(unittest.TestCase):
    """Testing all routes in Place Review API"""

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

    def test_get_review_by_place_id(self):
        """test get HTTP request"""
        pass

    def test_get_review_by_place_id_fail(self):
        """test get HTTP request"""
        pass

    def test_get_review_id(self):
        """test get HTTP request"""
        pass

    def test_get_review_id_fail(self):
        """test get HTTP request"""
        pass

    def test_delete_id(self):
        """test delete HTTP request"""
        pass

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        pass

    def test_create_review_by_place_id(self):
        """test create HTTP request"""
        pass

    def test_create_review_by_place_id_fail_nojson(self):
        """test create HTTP request"""
        pass

    def test_create_review_by_place_id_fail_noplace(self):
        """test create HTTP request"""
        pass

    def test_create_review_by_place_id_fail_nouserID(self):
        """test create HTTP request"""
        pass

    def test_update_id(self):
        """test update HTTP request"""
        pass

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        pass


if __name__ == "__main__":
    unittest.main()
