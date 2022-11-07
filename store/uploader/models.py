from django.db import models

import uuid

def upload_image(file, name):
    print(file)
    return f"{uuid.uuid4()}-{name}"

class File(models.Model):

    id = models.AutoField(
        primary_key=True,
        null=False,
        blank=False)

    image = models.ImageField(
            upload_to=upload_image,
            blank=True,
            null= True)
