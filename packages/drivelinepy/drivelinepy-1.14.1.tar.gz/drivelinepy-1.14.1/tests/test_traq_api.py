import unittest
from unittest.mock import patch, MagicMock
from drivelinepy.traq_api import TRAQAPI
import os
from dotenv import load_dotenv
import logging
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestTRAQAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("TRAQ API - Setting up class for testing...")
        cls.client_id = os.getenv("DRIVELINEPY_TRAQ_CLIENT_ID")
        cls.client_secret = os.getenv("DRIVELINEPY_TRAQ_CLIENT_SECRET")
        if not cls.client_id or not cls.client_secret:
            raise ValueError("TRAQ API credentials not set in environment variables")
        cls.traq_api = TRAQAPI(cls.client_id, cls.client_secret)
        cls.VALID_TRAQ_ID = 6183
        cls.VALID_EMAIL = "garrettyork03@gmail.com"
        cls.mock_response = {"data": [
            {'id': 6183, 'email': 'garrettyork03@gmail.com'}
        ]}

    #-----------------------------------------------------------------
    # Test - Get users by TRAQ ID
    #----------------------------------------------------------------

    @patch('drivelinepy.traq_api.BaseAPIWrapper.get')
    def test_get_users_by_traq_id(self, mock_get):
        print("TRAQ API - Testing get_users by TRAQ ID...")
        mock_get.return_value.json.return_value = self.mock_response
        response = self.traq_api.get_users(traq_id=self.VALID_TRAQ_ID)
        
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['id'], self.VALID_TRAQ_ID)
        self.assertEqual(response[0]['email'], 'garrettyork03@gmail.com')

    #-----------------------------------------------------------------
    # Test - Get users by email
    #-----------------------------------------------------------------

    @patch('drivelinepy.traq_api.BaseAPIWrapper.get')
    def test_get_users_by_email(self, mock_get):
        print("TRAQ API - Testing get_users by email...")
        mock_get.return_value.json.return_value = self.mock_response
        response = self.traq_api.get_users(email=self.VALID_EMAIL)
        
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['id'], self.VALID_TRAQ_ID)
        self.assertEqual(response[0]['email'], 'garrettyork03@gmail.com')

if __name__ == '__main__':
    unittest.main()