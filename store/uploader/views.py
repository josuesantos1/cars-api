import uuid, os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers

from .serializer import FileSerializer

from boto3.session import Session

class Uploader(APIView):    
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def put(self, request, format=None):
        file_extension = os.path.splitext(str(request.FILES['image']))[1]
        key = f"{uuid.uuid4()}{file_extension}"

        session = Session(region_name=str(os.getenv('REGION')),
                          aws_access_key_id=str(os.getenv('ACCESS_KEY')),
                          aws_secret_access_key=str(os.getenv('SECRETE_KEY')))

        s3 = session.resource('s3')
        s3.Bucket(str(os.getenv('BUCKET'))).put_object(Key=key, Body=request.FILES['image'])

        return Response({'key': key})
    