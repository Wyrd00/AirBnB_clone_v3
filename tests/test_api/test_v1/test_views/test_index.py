#!/usr/bin/python3
"""
Unittest for api/v1/view/index.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
import json


class Test_Index_API(unittest.TestCase):
    """Testing all routes in Index API"""

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

    def test_status(self):
        """test status view"""
        response = self.app.get('{}status/'.format(self.basepath))
#        self.assertEqual(response.status_code, 200)
#        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
#        self.assertIn("status", response_to_dict)
#        self.assertIn("OK", response_to_dict["status"])

    def test_stats(self):
        """test stats view"""
        response = self.app.get('{}/stats/'.format(self.basepath))
#        self.assertEqual(response.status_code, 200)
#        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
#        self.assertEqual(type(response_to_dict), list)
#        cls = ("users", "reviews", "cities", "states", "places", "amenities")
#        for c in cls:
#            self.assertIn(c, response_to_dict)
#        for c in cls:
#            self.assertIn(storage.count(c), response_to_dict[c])


if __name__ == "__main__":
    unittest.main()
