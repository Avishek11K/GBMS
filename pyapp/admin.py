from django.contrib import admin
from pyapp.models import Contact
from pyapp.models import Home
# Register your models here.
admin.site.register(Contact)
admin.site.register(Home)

from pyapp.models import availablerent
admin.site.register(availablerent)

# from pyapp.models import janak
# admin.site.register(janak)

from pyapp.models import landlord
admin.site.register(landlord)

from pyapp.models import Application
admin.site.register(Application)

from pyapp.models import roomseeker
admin.site.register(roomseeker)