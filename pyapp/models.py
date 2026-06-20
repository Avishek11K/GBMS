from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=140)
    email=models.CharField(max_length=160)
    password=models.CharField(max_length=190)
    feedback=models.TextField()
    
    def __str__(self):
        return (self.name+" "+self.email)
    
class Home(models.Model):
    title=models.CharField(max_length=500)
    location=models.CharField(max_length=500)
    price=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='houses/')

    def __str__(self):
        return (self.title)
    
class availablerent(models.Model):
    address=models.CharField(max_length=450)
    price=models.IntegerField()
    image=models.ImageField(upload_to='houses/')

class landlord(models.Model):
    name=models.CharField(max_length=450)
    email=models.CharField(max_length=450)
    password=models.CharField(max_length=590)

    def __str__(self):
        return self.name

class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house = models.ForeignKey(Home,on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

class roomseeker(models.Model):
    name=models.CharField(max_length=450)
    email=models.CharField(max_length=450)
    password=models.CharField(max_length=590)

    def __str__(self):
        return self.name


