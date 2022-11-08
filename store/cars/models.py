from django.db import models
import uuid

class Cars(models.Model):

    id = models.AutoField(
        primary_key=True,
        null=False,
        blank=False)

    name = models.CharField(
        max_length=256,
        null=False,
        blank=False)

    brand = models.CharField(
        max_length=32,
        null=False,
        blank=False
    )

    model = models.CharField(
        max_length=32,
        null=False,
        blank=False
    ) 

    slug = models.CharField(
        max_length=256,
        null=True,
        blank=False
    )

    photo = models.CharField(
        max_length=1024,
        null=False,
        blank=True
    )

    price = models.FloatField(
        max_length=32,
        null=False,
        blank=False,
        default=0
    )

    owner = models.CharField(
        max_length=256,
        null=True,
        blank=False,
    )
