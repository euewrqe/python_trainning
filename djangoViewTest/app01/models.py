from django.db import models

class UserModel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

