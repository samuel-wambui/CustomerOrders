from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Role
from unittest.mock import patch

class UserViewTests(TestCase):
    def setUp(self):
        # Create roles for testing
        self.user_role = Role.objects.create(name="user")
        self.admin_role = Role.objects.create(name="admin")

        # Create a test client
        self.client = Client()

        # Test user
        self.email = "testuser@example.com"
        self.user = User.objects.create(email=self.email)

    def test_add_user_from_jwt_creates_user_and_assigns_role(self):
        response = self.client.get(reverse('add_user_from_jwt', args=["newuser@example.com"]))
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("newuser@example.com", response.json()["message"])
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertIn(self.user_role, User.objects.get(email="newuser@example.com").roles.all())

    def test_add_user_from_jwt_existing_user(self):
        response = self.client.get(reverse('add_user_from_jwt', args=[self.email]))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"User {self.email} already exists.", response.json()["message"])

    def test_add_user_from_jwt_no_default_role(self):
        self.user_role.delete()
        response = self.client.get(reverse('add_user_from_jwt', args=["newuser@example.com"]))

        self.assertEqual(response.status_code, 500)
        self.assertIn("Default role 'user' not found.", response.json()["error"])

    def test_upgrade_user_to_admin(self):
        response = self.client.get(reverse('upgrade_user_to_admin', args=[self.email]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(f"User {self.email} upgraded to admin.", response.json()["message"])
        self.assertIn(self.admin_role, self.user.roles.all())

    def test_upgrade_user_to_admin_user_not_found(self):
        response = self.client.get(reverse('upgrade_user_to_admin', args=["nonexistent@example.com"]))

        self.assertEqual(response.status_code, 404)

    def test_upgrade_user_to_admin_no_admin_role(self):
        self.admin_role.delete()
        response = self.client.get(reverse('upgrade_user_to_admin', args=[self.email]))

        self.assertEqual(response.status_code, 500)
        self.assertIn("Admin role not found.", response.json()["error"])

    @patch('yourapp.utils.decode_jwt_and_get_email', return_value="jwtuser@example.com")
    def test_jwt_login_view_creates_user_and_assigns_role(self, mock_decode_jwt):
        response = self.client.get(reverse('jwt_login_view'))

        self.assertEqual(response.status_code, 200)
        self.assertIn("jwtuser@example.com", response.json()["message"])
        self.assertTrue(User.objects.filter(email="jwtuser@example.com").exists())
        self.assertIn(self.user_role, User.objects.get(email="jwtuser@example.com").roles.all())

    @patch('yourapp.utils.decode_jwt_and_get_email', return_value=None)
    def test_jwt_login_view_invalid_jwt(self, mock_decode_jwt):
        response = self.client.get(reverse('jwt_login_view'))

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid or missing JWT email.", response.json()["error"])

    @patch('yourapp.utils.decode_jwt_and_get_email', return_value="jwtuser@example.com")
    def test_jwt_login_view_no_default_role(self, mock_decode_jwt):
        self.user_role.delete()
        response = self.client.get(reverse('jwt_login_view'))

        self.assertEqual(response.status_code, 500)
        self.assertIn("Default role 'user' not found.", response.json()["error"])
