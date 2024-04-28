from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):

    name = models.CharField(max_length=100) 
    description = models.CharField(max_length=500) 

    def __str__(self):
        return self.name

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=20) 
    address = models.CharField(max_length=200) 
    role_id = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)   #
    picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.username