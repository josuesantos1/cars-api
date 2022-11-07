from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import CarsSerializer
from .models import Cars


class cars(APIView):    
    def get_cars(self, cars_id):
        try:
            return Cars.objects.get(pk=cars_id)
        except Cars.DoesNotExist:
            return None

    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'brand': request.data.get('brand'),
            'model': request.data.get('model'),
            'slug': request.data.get('slug'),
            'photo': request.data.get('photo'),
            'price': request.data.get('price')
        }

        serializer = CarsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        id = request.GET.get('id')

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

