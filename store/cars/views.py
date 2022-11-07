import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import CarsSerializer
from .models import Cars

from users.auth import Auth

class cars(APIView):    
    def get_cars(self, cars_id):
        try:
            return Cars.objects.get(pk=cars_id)
        except Cars.DoesNotExist:
            return None

    def me(self, owner):

        cars = Cars.objects.all().filter(owner=owner.get('id')).order_by('price').values()
        serializer = CarsSerializer(cars, many=True)
        return serializer.data

    def post(self, request):
        id = request.META.get('HTTP_AUTHORIZATION')

        token = Auth.verify_jwt(id.replace("Bearer ", ""))

        if not token:
            return Response({'message': 'UNAUTORIZER'}, status=status.HTTP_401_UNAUTHORIZED)

        name = request.data.get('name')

        data = {
            'name': name,
            'brand': request.data.get('brand'),
            'model': request.data.get('model'),
            'slug': name.replace(" ", "_") + str(+ random.randint(100, 999)),
            'photo': request.data.get('photo'),
            'price': request.data.get('price'),
            'owner': token.get('id')
        }

        serializer = CarsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.GET.get('id')
        me = request.GET.get('me')
        token = request.META.get('HTTP_AUTHORIZATION')

        if me:
            result = Auth.verify_jwt(token.replace("Bearer ", ""))
            if not result: 
                return Response({'message': 'UNAUTORIZER'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response(self.me(result))

        if not id:
            cars = Cars.objects.all().order_by('price').values()
            serializer = CarsSerializer(cars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        cars = self.get_cars(id)
        
        if not cars:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

        serializer = CarsSerializer(cars)

        return Response(serializer.data)

    def patch(self, request):
        id = request.GET.get('id')
        
        cars = self.get_cars(id)

        if not cars:
            return Response("not found", status=status.HTTP_404_NOT_FOUND)

        data = {
            'name': request.data.get('name'),
            'brand': request.data.get('brand'),
            'model': request.data.get('model'),
            'slug': request.data.get('slug'),
            'photo': request.data.get('photo')
        }

        serializer = CarsSerializer(cars, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id = request.GET.get('id')
        cars = self.get_cars(id)

        if not cars:
            return Response(
                "not exists", 
                status=status.HTTP_404_NOT_FOUND
            )

        cars.delete()

        return Response(
            "car deleted!",
            status=status.HTTP_200_OK
        )

