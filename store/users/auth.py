import jwt, datetime, os
from .models import Users

class Auth():
    def user_exists(users_id):
        try:
            Users.objects.get(email=users_id)
            return True
        except Users.DoesNotExist:
            return None

    def verify_jwt(token):
        try:
            return jwt.decode(token, str(os.getenv('TOKEN_PASS')), algorithms='HS256')
        except:
            return None

    def create_jwt(user_id):
        tnow = datetime.datetime.utcnow()
        payload = {
            'id': user_id,
            'exp': tnow + datetime.timedelta(hours=3),
            'iat': tnow
        }

        return jwt.encode(payload, str(os.getenv('TOKEN_PASS')), algorithm='HS256').decode('utf-8')