from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers

from .serializer import FileSerializer
from .models import File


class Uploader(APIView):    
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def put(self, request, format=None):
        print(type(request.FILES['image']))
        data = {
            'image': request.FILES['image']
        }

        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    