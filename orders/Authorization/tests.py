from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import Role
from .views import jwt_login_view  # Assuming jwt_login_view is in views.py

class JWTLoginTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('Authorization.utils.decode_jwt_and_get_email')
    def test_user_registration_and_role_assignment(self, mock_decode_jwt):
        request = self.factory.get("/jwt-login/", HTTP_AUTHORIZATION="Bearer mocktoken")

        # Mock JWT decoding function to return a valid email
        mock_decode_jwt.return_value = "testuser@example.com"

        # Call the actual view function
        from Authorization.views import jwt_login_view  # Import your view
        response = jwt_login_view(request)

        # Assert response status code is 200
        self.assertEqual(response.status_code, 200)
    @patch('Authorization.utils.decode_jwt_and_get_email')  # Mock JWT decoding function
    def test_user_registration_and_role_assignment(self, mock_decode_jwt):
        mock_email = "testuser@example.com"
        mock_decode_jwt.return_value = mock_email  # Simulating decoded email
        
        request = self.factory.post("/jwt-login/")
        response = jwt_login_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user_model.objects.filter(email=mock_email).exists())
        user = self.user_model.objects.get(email=mock_email)
        self.assertIn(self.user_role, user.roles.all())  # Check if user role is assigned