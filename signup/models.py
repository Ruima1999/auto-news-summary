from django.db import models

# Create your models here.

class email(models.Model):
    address = models.CharField(max_length=40)