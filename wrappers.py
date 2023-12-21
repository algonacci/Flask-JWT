from functools import wraps

import jwt
from flask import jsonify, request

SECRET_KEY = "secret"


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            return jsonify({
                "status": {
                    "code": 401,
                    "message": "Invalid token",
                },
                "data": None
            }), 401
        try:
            token_prefix, token_value = token.split()
            if token_prefix.lower() != 'bearer':
                raise ValueError('Invalid token prefix')
            data = jwt.decode(token_value, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": {
                    "code": 401,
                    "message": "Token has expired",
                },
                "data": None
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "status": {
                    "code": 401,
                    "message": "Invalid token"
                },
                "data": None,
            }), 401
        except ValueError:
            return jsonify({
                "status": {
                    "code": 401,
                    "message": "Invalid token format",
                },
                "data": None
            }), 401
        return f(*args, **kwargs)
    return decorator
