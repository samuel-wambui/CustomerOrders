# utils.py
from .models import User, Role
import jwt
from django.http import JsonResponse
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

def decode_jwt_and_get_email(request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Missing or invalid Authorization header")
        return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)
    
    token = auth_header.split(" ")[1]  # Extract token from "Bearer <token>"
    
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded.get("email")
    except jwt.ExpiredSignatureError:
        logger.error("JWT Error: Token has expired")
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.DecodeError:
        logger.error("JWT Error: Invalid token")
        return JsonResponse({"error": "Invalid token"}, status=400)
    except Exception as e:
        logger.exception(f"Unexpected JWT error: {str(e)}")
        return JsonResponse({"error": "JWT processing error"}, status=500)

class JWTUserHandler:
    @staticmethod
    def handle_jwt_user(email):
        # Check if user exists, otherwise create them
        user, created = User.objects.get_or_create(email=email)
        if created:
            # Assign "user" role by default
            user.roles.add(Role.objects.get(name="user"))
        return user
