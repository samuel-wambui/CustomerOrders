import logging
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from Authorization.utils import JWTUserHandler  # Import the JWT handler

# Configure logging
logger = logging.getLogger(__name__)

class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def verify_token(self, token, *args, **kwargs):
        # Log the raw JWT for debugging purposes
        logger.info("Received JWT: %s", token)
        # Continue with the default verification
        return super().verify_token(token, *args, **kwargs)

    def create_user(self, claims):
        """
        Create a new user if they don't exist based on the JWT claims.
        """
        email = claims.get("email")
        if email:
            user = JWTUserHandler.handle_jwt_user(email)  # Use the handler to process the user
            logger.info(f"Created or fetched user with email: {email}")
            return user
        logger.error("No email found in JWT claims, cannot create user.")
        return None

    def update_user(self, user, claims):
        """
        Update an existing user based on the JWT claims.
        """
        email = claims.get("email")
        if email and user.email != email:
            logger.info(f"Updating user email from {user.email} to {email}")
            user.email = email
            user.save()
        return user
