from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import jwt, datetime

from .serializer import UsersSerializer
from .models import Users


class users(APIView):
    def get_users(self, users_id):
        try:
            print(users_id)
            return Users.objects.get(email=users_id)
        except Users.DoesNotExist:
            return None

    def user_exists(self, users_id):
        try:
            Users.objects.get(email=users_id)
            return True
        except Users.DoesNotExist:
            return None

    def verify_jwt(self, token):
        try:
            return jwt.decode(token, 'password', algorithms='HS256')
        except:
            return None

    def create_jwt(self, user_id):
        tnow = datetime.datetime.utcnow()
        payload = {
            'id': user_id,
            'exp': tnow + datetime.timedelta(hours=3),
            'iat': tnow
        }

        return jwt.encode(payload, 'password', algorithm='HS256').decode('utf-8')

    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        if self.user_exists(request.data.get('email')): 
            return Response({'message': 'already exists user'})

        serializer = UsersSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            token = self.create_jwt(data.get('email'))
            
            response = Response() #({'TOKEN': token}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='token',
                value=token,
                httponly=True
            )

            response.data = {
                'token': token
            }

            return response

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.META.get('HTTP_AUTHORIZATION')

        print(id)
        if not id:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        email = self.verify_jwt(id.replace("Bearer ", ""))
        print(email)
        if not email:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_users(email.get('id'))
        print(email)
        if not user:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializer(user)

        return Response(serializer.data)

    def patch(self, request):
        id = request.META.get('HTTP_AUTHORIZATION')

        if not id:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        email = self.verify_jwt(id.replace("Bearer ", ""))

        if not email:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_users(email.get('id'))

        if not user:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        serializer = UsersSerializer(user, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.META.get('HTTP_AUTHORIZATION')

        if not id:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        email = self.verify_jwt(id.replace("Bearer ", ""))

        print(email)

        if not email:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        user = self.get_users(email.get('id'))

        if not user:
            return Response(
                "not exists", 
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response(
            "deleted!",
            status=status.HTTP_200_OK
        )


class Login(APIView):
    def verify_jwt(self, token):
        try:
            return jwt.decode(token, 'password', algorithms=['HS256'])
        except:
            return None

    def create_jwt(self, user_id):
        tnow = datetime.datetime.utcnow()
        payload = {
            'id': user_id,
            'exp': tnow + datetime.timedelta(hours=3),
            'iat': tnow
        }

        return jwt.encode(payload, 'password', algorithm='HS256').decode('utf-8')

    def get_users(self, users_id):
        try:
            return Users.objects.get(email=users_id)
        except Users.DoesNotExist:
            return None

    def user_exists(self, users_id):
        try:
            Users.objects.get(email=users_id)
            return True
        except Users.DoesNotExist:
            return None

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        email = data.get('email')

        if not self.user_exists(email):
            return Response({'message': 'user not found'})

        user = self.get_users(email)

        if not user:
            return Response({'message': 'wrong email or password'})

        token = self.create_jwt(email)

        if not token:
            return Response("UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

        return Response({'token': token})

