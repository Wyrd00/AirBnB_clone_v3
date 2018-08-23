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
        cls.basepath = "api/v1/users"

    @classmethod
    def tearDownClass(cls):
        """teardown"""
        pass

    def test_get_users(self):
        """test get HTTP request"""
        attr = {"name":"Bob"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.get("{}".format(self.basepath))
        response_to_dict = json.load(str(response.data), encoding="utf8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict['__class__'], "User")
        self.assertEqual(response_to_dict['name'], new_instance['name'])
        self.assertEqual(response_to_dict['id'], new_instance.id)
        new_instance.delete()

    def test_get_user_by_id(self):
        """test get HTTP request"""
        attr = {"name":"Butter"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.get('{}/{}'.format(self.basepath, new_instance.user.id))
        self.assertEqual(response.status_code, 200)
        new_instance.delete()

    def test_get_user_by_id_fail(self):
        """test get HTTP request"""
        attr = {"name": "Unicorn"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.get('{}/troll'.format(self.basepath))
        response_to_dict = json.load(str(response.data, encoding="utf8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])
        new_instance.delete()

    def test_delete_id(self):
        """test delete HTTP request"""
        attr = {"name": "Umbridge"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.delete('{}/{}'.format(self.basepath,
                                   new_instance.id))
        response_to_dict = json.loads(str(response.data), encoding="utf-8")
        self.asssertEqual(response.status_code, 200)
        self.assertEqual(response_to_dict, {})
        confirm_in_db = self.app.get('{}/{}'.format(self.basepath, 
                                     new_instance.id))
        self.assertEqual(confirm_in_db.status_code, 404)
        new_instance.delete()

    def test_delete_id_fail(self):
        """test delete HTTP request"""
        attr = {"name": "McHammer"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.delete('{}/troll'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not found", response_to_dict["error"])
        obj = storage.get("User", new_instance.id)
        self.assertIsNotNone(obj)
        new_instance.delete()

    def test_create(self):
        """test create HTTP request"""
        attr = {"email": "bob@burger.com", "password": "brokenglassgang",
		"id": "111"}
        new_instance = User(**attr)
        new_instance.save()
        response = self.app.post('{}'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 201)
        obj = storage.get("User", "111")
        self.assertIsNotNone(obj)
        new_instance.delete()

    def test_create_fail_nojson(self):
        """test create HTTP request"""
        attr = {"email": "gimmeajob@please.co.nz", "id": "222"}
        response = self.app.post('{}'.format(self.basepath))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("User", "222")
        self.assertIsNone(obj)
	
    def test_create_fail_noemail(self):
        """test create HTTP request"""
        attr = {"password": "hot_tamales", "id": "010"}
        response = self.app.post('{}'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing email", response_to_dict["error"])
        obj = storage.get("User", "010")
        self.assertIsNone(obj)

    def test_create_fail_nopassword(self):
        """test create HTTP request"""
        attr = {"email": "hungry@feedme.com", "id": "011"}
        response = self.app.post('{}'.format(self.basepath),
                                 content_type="application/json",
                                 data=json.dumps(attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Missing password", response_to_dict["error"])
        obj = storage.get("User", "011")
        self.assertIsNone(obj)

    def test_update_id(self):
        """test update HTTP request"""
        attr = {"email": "peanutbutter@jelly.com"}
        new = User(**attr)
        new.save()
        new_attr = {"email": "peanutbutter@celery.com"}
        response = self.app.put('{}/{}'.format(self.basepath, new.id),
                                 content_type="application/json",
                                 data=json.dumps(new_attr))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 200)
        obj = storage.get("User", new.id)
        self.assertEqual(obj.name, new_attr["name"])
        new.delete()

    def test_update_id_fail_nojson(self):
        """test update HTTP request"""
        attr = {"email": "peanutbutter@jelly.com"}
        new = User(**attr)
        new.save()
        new_attr = {"email": "peanutbutter@celery.com"}
        response = self.app.put('{}/{}'.format(self.basepath, new.id))
        response_to_dict = json.loads(str(response.data, encoding="utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response_to_dict)
        self.assertIn("Not a JSON", response_to_dict["error"])
        obj = storage.get("User", new.id)
        self.assertNotEqual(obj.email, new_attr["email"])
        self.assertEqual(obj.email, new.email)
        new.delete()

    def test_update_id_fail_nouser(self):
        """test update HTTP request"""
        pass

if __name__ == "__main__":
    unittest.main()
