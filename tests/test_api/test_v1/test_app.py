#!/usr/bin/python3
"""
Testing app.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
import json


class Test_App(unittest.TestCase):
    """Testing app.py"""

    def setUp(self):
        """setup"""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """teardown"""
        pass

    def test_404(self):
        """test @app.errorhandler(404)"""
        response = self.app.get('/fake_route')
        self.assertEqual(response.status_code, 404)
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])


if __name__ == "__main__":
    unittest.main()
