from functools import wraps
from flask import request, current_app
from shared_kernel.auth import JWTTokenHandler
from shared_kernel.config import Config
from shared_kernel.exceptions import Unauthorized

config = Config()
token_handler = JWTTokenHandler(config.get('JWT_SECRET_KEY'))


# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if not request.authorization:
            raise Unauthorized('Token is missing!')

        token = request.authorization.token

        payload = token_handler.decode_token(token)

        if 'error' in payload:
            raise Unauthorized("Failed to parse token")

        # Add user information to the request context
        current_user = {
            "user_id": payload['user_id'],
            "organization_id": payload['organization_id']
        }

        # ensure_sync is used to ensure that the decorated function is
        # executed synchronously, even if it's an asynchronous function.
        return current_app.ensure_sync(f)(current_user, *args, **kwargs)

    return decorator
