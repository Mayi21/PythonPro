from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=2)
    age = models.IntegerField()

    def __str__(self):
        return self.name
