from django.db import models

# Create your models here.

class newuser(models.Model):
    username=models.CharField(max_length=100)
    Email1=models.EmailField(max_length=100)
    Password1=models.CharField(max_length=100)
    Password2=models.CharField(max_length=100)
