#!/usr/bin/python3
"""Defines the methods for the State unittests"""
import unittest
from flask import json
from api.v1.app import app
from models import storage
from models.state import State


class TestStates(unittest.TestCase):
    """This class represents the test case for states endpoints."""

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize the app."""
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    @classmethod
    def tearDownClass(self):
        """Teardown all initialized variables."""
        # Clean up the database or reset app configurations if necessary
        self.app_context.pop()

    def test_get_status(self):
        """Test the /status endpoint."""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('OK', response.get_json()['status'])

    def test_get_states(self):
        """Test API can get a list of states (GET request)."""
        res = self.client.get('/api/v1/states')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(json.loads(res.data), list)

    def test_get_state(self):
        """Test API can get a single state by using its ID (GET request)."""
        # Assuming you have at least one State in your test database
        state = State(name="Test State")
        state.save()
        res = self.client.get(f'/api/v1/states/{state.id}')
        self.assertEqual(res.status_code, 200)
        state.delete()


if __name__ == "__main__":
    unittest.main()
