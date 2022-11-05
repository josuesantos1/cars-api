from django.db import models

class Users(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=256,
        null=False,
        blank=False)

    email = models.CharField(
        max_length=256,
        null=False,
        blank=False
    )

    password = models.CharField(
        max_length=260,
        null=False,
        blank=False
    )
