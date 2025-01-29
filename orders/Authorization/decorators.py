from functools import wraps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User, Role
from .utils import decode_jwt_and_get_email  # Ensure this function extracts the email from JWT


def role_required(required_role):
    """Decorator to check if the user has the required role."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Decode JWT and get email
            email_response = decode_jwt_and_get_email(request)
            if isinstance(email_response, JsonResponse):
                return email_response  # Return error if JWT is invalid

            email = email_response
            user = get_object_or_404(User, email=email)  # Get user object

            # Check if the user has the required role
            if not user.roles.filter(name=required_role).exists():
                return JsonResponse({"error": "Unauthorized access. Admin role required."}, status=403)

            return view_func(request, *args, **kwargs)  # Call original view function
        return _wrapped_view
    return decorator
