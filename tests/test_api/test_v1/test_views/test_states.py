#!/usr/bin/python3
"""
Unittest for api/v1/view/states.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
from models.state import State
import json


class Test_State_API(unittest.TestCase):
    """Testing all routes in State API"""

    @classmethod
    def setUpClass(cls):
        """setup"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.basepath = "api/v1/states"

    @classmethod
    def tearDownClass(cls):
        """teardown"""
        pass

    def test_get(self):
        """test get HTTP request"""
        attr = {"name": "NY"}
        new_instance = State(**attr)
        new_instance.save()
        response = self.app.get('{}'.format(self.basepath))
        self.assertEqual(response.status_code, 200)
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertTrue(type(response_to_dict), list)
        self.assertEqual(response_to_dict[0]["__class__"], "State")
        self.assertEqual(response_to_dict[0]["name"], attr["name"])
        new_instance.delete()

    def test_get_id(self):
        """test get HTTP request"""
        attr = {"name": "NJ"}
        new_s = State(**attr)
        new_s.save()
        response = self.app.get('{}/{}'.format(self.basepath, new_s.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict["__class__"], "State")
        self.assertEqual(response_to_dict["name"], attr["name"])
        self.assertEqual(response_to_dict["id"], new_s.id)
        new_s.delete()

    def test_get_id_fail(self):
        """test get HTTP request"""
        attr = {"name": "NY"}
        new_instance = State(**attr)
        new_instance.save()
        response = self.app.get('{}/fake_id_123'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])
        new_instance.delete()

    def test_delete_id(self):
        """test delete HTTP request"""
        attr = {"name": "NY"}
        new_instance = State(**attr)
        new_instance.save()
        response = self.app.delete('{}/{}'.format(self.basepath,
                                                  new_instance.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict, {})
        new_instance.delete()

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        attr = {"name": "NY"}
        new_instance = State(**attr)
        new_instance.save()
        response = self.app.delete('{}/fake_id_123'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])
        obj = storage.get("State", new_instance.id)
        self.assertIsNotNone(obj)
        new_instance.delete()

    def test_create_id(self):
        """test create HTTP request"""
        attr = {"name": "NY", "id": "888"}
        new_instance = State(**attr)
        new_instance.save()
        response = self.app.post('{}'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 201)
        obj = storage.get("State", "888")
        self.assertIsNotNone(obj)
        new_instance.delete()

    def test_create_fail_nojson(self):
        """test create HTTP request"""
        attr = {"name": "NY", "id": "888"}
        response = self.app.post('{}'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("State", "888")
        self.assertIsNone(obj)

    def test_create_fail_noname(self):
        """test create HTTP request"""
        attr = {"id": "777"}
        response = self.app.post('{}'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing name", response_to_dict["error"])
        obj = storage.get("State", "777")
        self.assertIsNone(obj)

    def test_update_id(self):
        """test update HTTP request"""
        attr = {"name": "FarAway"}
        new = State(**attr)
        new.save()
        new_attr = {"name": "FarFarAway"}
        response = self.app.put('{}/{}'.format(self.basepath, new.id),
                                 content_type="application/json",
                                 data=json.dumps(new_attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        obj = storage.get("State", new.id)
        self.assertEqual(obj.name, new_attr["name"])
        new.delete()

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        attr = {"name": "FarAway"}
        new = State(**attr)
        new.save()
        new_attr = {"name": "FarFarAway"}
        response = self.app.put('{}/{}'.format(self.basepath, new.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("State", new.id)
        self.assertNotEqual(obj.name, new_attr["name"])
        new.delete()


if __name__ == "__main__":
    unittest.main()
