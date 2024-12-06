import os
import unittest
from dotenv import load_dotenv
from hvmnd_api_client import APIClient


class TestAPIClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        base_url = os.getenv('API_BASE_URL')
        if not base_url:
            raise ValueError("API_BASE_URL environment variable not set in .env file")
        cls.client = APIClient(base_url=base_url)

        cls.telegram_user_id = 231584958
        cls.test_user_data = {
            'telegram_id': cls.telegram_user_id,
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'language_code': 'en',
            'total_spent': 0,
            'balance': 99999,
            'banned': False
        }
        cls.client.create_or_update_user(cls.test_user_data)

    def test_ping(self):
        """Test the ping method."""
        result = self.client.ping()
        self.assertTrue(result)

    def test_get_nodes(self):
        """Test retrieving nodes."""
        nodes = self.client.get_nodes()
        self.assertIsInstance(nodes, list)

    def test_get_users(self):
        """Test retrieving users."""
        users = self.client.get_users(limit=5)
        self.assertIsInstance(users, list)
        self.assertLessEqual(len(users), 5)

    def test_create_or_update_user(self):
        """Test creating or updating a user."""
        user_data = {
            'telegram_id': self.telegram_user_id,
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'language_code': 'en',
            'banned': False
        }
        result = self.client.create_or_update_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['first_name'], 'Updated')

    def test_get_payments(self):
        """Test retrieving payments."""
        payments = self.client.get_payments(limit=5)
        self.assertIsInstance(payments, list)
        self.assertLessEqual(len(payments), 5)

    def test_create_complete_and_cancel_payment(self):
        result = self.client.create_payment_ticket(user_id=1, amount=50.0)
        self.assertIsInstance(result, dict)
        self.assertIn('payment_ticket_id', result)
        payment_ticket_id = result['payment_ticket_id']

        # Complete the payment
        result = self.client.complete_payment(id_=payment_ticket_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('payment_ticket_id'), str(payment_ticket_id))

        # Cancel the payment
        result = self.client.cancel_payment(id_=payment_ticket_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('payment_ticket_id'), str(payment_ticket_id))
        self.assertEqual(result.get('status'), 'cancelled')


if __name__ == '__main__':
    unittest.main()
