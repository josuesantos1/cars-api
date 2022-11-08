from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()


