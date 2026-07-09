from django.db import models
# inbuilt model:user that is imported i.e. djnago.contrib.auth.models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=140)
    email=models.CharField(max_length=160)
    password=models.CharField(max_length=190)
    feedback=models.TextField()
    
    def __str__(self):
        return (self.name+" "+self.email)
    # Home models or database 
# class Home(models.Model):
#     landlord=models.ForeignKey(, on_delete=models.CASCADE)
#     title=models.CharField(max_length=500)
#     location=models.CharField(max_length=500)
#     price=models.IntegerField()
#     description=models.TextField()
#     image=models.ImageField(upload_to='houses/')

#     def __str__(self):
#         return (self.title)
    
class availablerent(models.Model):
    address=models.CharField(max_length=450)
    price=models.IntegerField()
    image=models.ImageField(upload_to='houses/')

# landlord model
class landlord(models.Model):
    name=models.CharField(max_length=450)
    email=models.CharField(max_length=450)
    password=models.CharField(max_length=590)

    def __str__(self):
        return self.name
    

class Home(models.Model):
    landlord=models.ForeignKey(landlord, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=500)
    location=models.CharField(max_length=500)
    price=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='houses/')

    def __str__(self):
        return (self.title)

# store the applied data by specified user in Application model
class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house = models.ForeignKey(Home,on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

# roomseeker model
class roomseeker(models.Model):
    name=models.CharField(max_length=450)
    email=models.CharField(max_length=450)
    password=models.CharField(max_length=590)

    def __str__(self):
        return self.name



