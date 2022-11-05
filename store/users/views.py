from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import UsersSerializer
from .models import Users


class users(APIView):
    def get_users(self, users_id):
        try:
            return Users.objects.get(pk=users_id)
        except Users.DoesNotExist:
            return None

    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }


        serializer = UsersSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.GET.get('id')

        user = self.get_users(id)
        
        if not user:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

        serializer = UsersSerializer(user)

        return Response(serializer.data)

    def patch(self, request):
        id = request.GET.get('id')
        
        user = self.get_users(id)

        if not user:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

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
        id = request.GET.get('id')
        user = self.get_users(id)

        if not user:
            return Response(
                "not exists", 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UsersSerializer(user)
        serializer.delete()

        return Response(
            "deleted!",
            status=status.HTTP_200_OK
        )

