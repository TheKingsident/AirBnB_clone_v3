import unittest
import json
from flask import current_app
from api.v1.app import app
from models import storage
from models.user import User

class TestUserAPI(unittest.TestCase):
    """This class represents the test case for user endpoints."""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.app = app
        cls.client = cls.app.test_client
        # Ensure the app is in testing mode
        cls.app.config['TESTING'] = True
        # Create a user for testing
        cls.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        cls.user = User(**cls.user_data)
        storage.new(cls.user)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Tear down test variables."""
        storage.delete(cls.user)
        storage.save()

    def test_get_users(self):
        """Test API can get a list of users (GET request)."""
        res = self.client().get('/api/v1/users')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(json.loads(res.data.decode('utf-8')), list)

    def test_create_user(self):
        """Test API can create a user (POST request)."""
        res = self.client().post('/api/v1/users', json=self.user_data)
        self.assertEqual(res.status_code, 201)
        # Clean up by deleting the created user
        data = json.loads(res.data)
        user = storage.get(User, data['id'])
        storage.delete(user)
        storage.save()

    def test_delete_user(self):
        """Test API can delete a user (DELETE request)."""
        res = self.client().delete(f'/api/v1/users/{self.user.id}')
        self.assertEqual(res.status_code, 200)



if __name__ == "__main__":
    unittest.main()
