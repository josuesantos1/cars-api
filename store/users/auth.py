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
            payload = jwt.decode(token, str(os.getenv('TOKEN_PASS')), algorithms='HS256')

            exp = payload.get('exp')
            exp_to_date = datetime.datetime.fromtimestamp(exp).strftime("%A, %B %d, %Y %I:%M:%S")
            if exp_to_date < datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M:%S"):
                return None

            return payload
        except:
            return None

    def create_jwt(user_id):
        tnow = datetime.datetime.utcnow()
        payload = {
            'id': user_id,
            'exp': tnow + datetime.timedelta(hours=5),
            'iat': tnow
        }

        return jwt.encode(payload, str(os.getenv('TOKEN_PASS')), algorithm='HS256').decode('utf-8')