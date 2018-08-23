#!/usr/bin/python3
"""
Unittest for api/v1/view/cities.py
"""
import unittest
import flask
from api.v1.app import app
from models import storage
from models.state import State
from models.city import City
import json


class Test_City_API(unittest.TestCase):
    """Testing all routes in City API"""

    @classmethod
    def setUpClass(cls):
        """setup"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.basepath = "api/v1"
        cls.state_attr = {"name": "FarFarFarAway", "id": "FA"}
        cls.state = State(**cls.state_attr)
        cls.state.save()

    @classmethod
    def tearDownClass(cls):
        """teardown"""
        storage.delete(cls.state)

    def test_get(self):
        """test get HTTP request"""
        attr = {"name": "Icy", "state_id": "FA"}
        new01 = City(**attr)
        new01.save()
        response = self.app.get('{}/states/{}/cities'.format(self.basepath,
                                                             self.state.id))
        self.assertEqual(response.status_code, 200)
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertTrue(type(response_to_dict), list)
        self.assertEqual(response_to_dict[0]["__class__"], "City")
        new01.delete()

    def test_get_id(self):
        """test get HTTP request"""
        attr = {"name": "San Fran", "state_id": "FA"}
        new_c = City(**attr)
        new_c.save()
        response = self.app.get('{}/cities/{}'.format(self.basepath, new_c.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict["__class__"], "City")
        self.assertEqual(response_to_dict["name"], attr["name"])
        self.assertEqual(response_to_dict["id"], new_c.id)
        new_c.delete()

    def test_get_id_fail(self):
        """test get HTTP request"""
        response = self.app.get('{}/cities/fake_id_123'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])

    def test_delete_id(self):
        """test delete HTTP request"""
        attr = {"name": "SF", "state_id": "FA"}
        new_i = City(**attr)
        new_i.save()
        response = self.app.delete('{}/cities/{}'.format(self.basepath,
                                                         new_i.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict, {})
        new_i.delete()

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        attr = {"name": "SF", "state_id": "FA"}
        new_in = City(**attr)
        new_in.save()
        response = self.app.delete('{}/cities/fake_id'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])
        obj = storage.get("City", new_in.id)
        self.assertIsNotNone(obj)
        new_in.delete()

    def test_create_id(self):
        """test create HTTP request"""
        attr = {"name": "SF", "id": "666", "state_id": "FA"}
        new_ins = City(**attr)
        new_ins.save()
        response = self.app.post('{}/states/{}/cities'.format(self.basepath,
                                                              self.state.id),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 201)
        obj = storage.get("City", "666")
        self.assertIsNotNone(obj)
        new_ins.delete()

    def test_create_fail_nojson(self):
        """test create HTTP request"""
        attr = {"name": "SF", "id": "555"}
        response = self.app.post('{}/states/{}/cities'.format(self.basepath,
                                                              self.state.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("City", "555")
        self.assertIsNone(obj)

    def test_create_fail_noname(self):
        """test create HTTP request"""
        attr = {"id": "444"}
        response = self.app.post('{}/states/{}/cities'.format(self.basepath,
                                                              self.state.id),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing name", response_to_dict["error"])
        obj = storage.get("City", "444")
        self.assertIsNone(obj)

    def test_update_id(self):
        """test update HTTP request"""
        attr = {"name": "FarAway", "state_id": "FA"}
        new007 = City(**attr)
        new007.save()
        new_attr = {"name": "FarFarAway"}
        response = self.app.put('{}/cities/{}'.format(self.basepath, new007.id),
                                 content_type="application/json",
                                 data=json.dumps(new_attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        obj = storage.get("City", new007.id)
        self.assertEqual(obj.name, new_attr["name"])
        new007.delete()

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        attr = {"name": "FarAway", "state_id": "FA"}
        new = City(**attr)
        new.save()
        new_attr = {"name": "FarFarAway"}
        response = self.app.put('{}/cities/{}'.format(self.basepath, new.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("City", new.id)
        self.assertNotEqual(obj.name, new_attr["name"])
        new.delete()


if __name__ == "__main__":
    unittest.main()
