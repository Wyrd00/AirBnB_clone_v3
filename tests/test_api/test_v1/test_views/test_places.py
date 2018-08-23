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
        attr = {"id": "01", "name": "San Francisco"}
        city = City(**attr)
        city.save()
        attr2 = {"id": "00", "name": "Esera"}
        user = User(**attr2)
        user.save()

    @classmethod
    def tearDownClass(cls):
        """teardown"""
        city.delete()
        user.delete()

    def test_get_place_by_city_id(self):
        """test get HTTP request"""
        attr = {"name":"Bobs Burger", "city_id": "01"}
        new = Place(**attr)
        new.save()
        response = self.app.get("{}/cities/{}/places".format(self.basepath,
                                                             city.id))
        response_to_dict = json.load(str(response.data, encoding="utf8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict['__class__'], "Place")
        self.assertEqual(response_to_dict['name'], new['name'])
        self.assertEqual(response_to_dict['id'], new.id)
        new.delete()

    def test_get_place_by_city_id_fail(self):
        """test get HTTP request"""
        pass

    def test_get_place_id(self):
        """test get HTTP request"""
        attr = {"name": "Standard Shack", "max_guest": 3}
        new = Place(**attr)
        new.save()
        response = self.app.get('{}/places/{}'.format(self.basepath, new.id))
        self.assertEqual(response.status_code, 200)
        new_instance.delete()

    def test_get_place_id_fail(self):
        """test get HTTP request"""
        response = self.app.get('{}/places/troll_id'.format(self.basepath))
        response_to_dict = json.load(str(response.data, encoding="utf8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])

    def test_delete_id(self):
        """test delete HTTP request"""
        attr = {"name": "Unicorn Den"}
        new = Place(**attr)
        new.save()
        response = self.app.delete('{}/places/{}'.format(self.basepath, 
                                                         new.id))
        response_to_dict = json.load(str(response.data, encoding="utf8"))
	self.asssertEqual(response.status_code, 200)
	self.assertEqual(response_to_dict, {})
        confirm_in_db = self.app.get('{}/places/{}'.format(self.basepath, 
                                                           new.id))
	self.assertEqual(confirm_in_db.status_code, 404)
	new.delete()

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        attr = {"name": "McHammer"}
        new = Place(**attr)
        new.save()
        pass

    def test_create_place_by_city_id(self):
        """test create HTTP request"""
        attr = {"city_id": "01", "name": "jeezlouise",
                "id": "333", "user_id": "00"}
        response = self.app.post('{}/cities/{}/places'.format(self.basepath,
                                 city.id), content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 201)
        obj = storage.get("Place", "333")
        self.assertIsNotNone(obj)
        new.delete()

    def test_create_place_by_city_id_fail_nojson(self):
        """test create HTTP request"""
        attr = {"city_id": "01", "name": "ooohlala",
                "id": "444", "user_id": "00"}
        response = self.app.post('{}/cities/{}/places'.format(self.basepath,
                                 city.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("Place", "444")
        self.assertIsNone(obj)

    def test_create_place_by_city_id_fail_noname(self):
        """test create HTTP request"""
        attr = {"city_id": "01", "description": "Yabadabadooh",
                "id": "444", "user_id": "00"}
        response = self.app.post('{}/cities/{}/places'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing name", response_to_dict["error"])
        obj = storage.get("Place", "444")
        self.assertIsNone(obj)

    def test_create_place_by_city_id_fail_nouserID(self):
        """test create HTTP request"""
        attr = {"city_id": "01", "name": "Jojo", "id": "544"}
        response = self.app.post('{}/cities/{}/places'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing user_id", response_to_dict["error"])
        obj = storage.get("Place", "544")
        self.assertIsNone(obj)

    def test_update_id(self):
        """test update HTTP request"""
        attr = {"name": "Room with three walls"}
        new = Place(**attr)
        new.save()
        new_attr = {"name": "Room with four walls"}
        response = self.app.put('{}/places/{}'.format(self.basepath, new.id),
                                 content_type="application/json",
                                 data=json.dumps(new_attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        obj = storage.get("Place", new.id)
        self.assertEqual(obj.name, new_attr["name"])
        new.delete()

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        attr = {"name": "Parent's basement"}
        new = Place(**attr)
        new.save()
        new_attr = {"name": "Parent's garage"}
        response = self.app.put('{}/places/{}'.format(self.basepath, new.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("Place", new.id)
        self.assertNotEqual(obj.name, new_attr["name"])
	self.assertEqual(obj.name, new["name"])
        new.delete()

    def test_update_id_fail_noplace(self):
        """test update HTTP request"""
        pass

if __name__ == "__main__":
    unittest.main()
