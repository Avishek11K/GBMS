from django.db import models

# inbuilt model:user that is imported i.e. djnago.contrib.auth.models
from django.contrib.auth.models import User

# from pyapp.models import Home


# Create your models here.not in use but can be used in future for contact us form
class Contact(models.Model):
    name = models.CharField(max_length=140)
    email = models.CharField(max_length=160)
    password = models.CharField(max_length=190)
    feedback = models.TextField()

    def __str__(self):
        return self.name + " " + self.email


# landlord model
# phone/whatsapp added so roomseekers can contact the landlord directly
# (previously the WhatsApp number was hardcoded in the templates for every house)
class landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(
        max_length=20, blank=True, help_text="Used for WhatsApp/phone contact button"
    )

    def __str__(self):
        username = getattr(self.user, "username", "Unknown")
        return username


# roomseeker profile: replaces the old standalone 'roomseeker' model, which stored
# its own separate hashed password and was never actually used for login.
# Real authentication always goes through Django's built-in User model + Groups;
# this just holds the extra profile info (phone) admin can view/manage.
class RoomSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return getattr(self.user, "username", "Unknown")


class Home(models.Model):
    landlord = models.ForeignKey(
        landlord, on_delete=models.CASCADE, null=True, blank=True, related_name="homes"
    )
    title = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    price = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class availablerent(models.Model):
    home = models.ForeignKey(
        Home, on_delete=models.CASCADE, related_name="avhome", blank=True, null=True
    )
    address = models.CharField(max_length=450)
    price = models.IntegerField()
    image = models.ImageField(upload_to="houses/")


# model homeimage created new
class HomeImage(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="houses/")


# store the applied data by specified user in Application model
# status added so landlord can accept/decline, and roomseeker can see the outcome
class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(
        Home, on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)
    # landlord_read: powers the "unread notification" badge for the landlord
    landlord_read = models.BooleanField(default=False)
    # seeker_read: powers the "unread notification" badge for the roomseeker,
    # set False again whenever the landlord changes the status
    # seeker_read = models.BooleanField(default=True)
    roomseeker_read = models.BooleanField(default=True)

    class Meta:
        ordering = ["-applied_at"]
        unique_together = ("user", "house")

    def __str__(self):
        return f"{self.user.username} -> {self.house.title} ({self.status})"
