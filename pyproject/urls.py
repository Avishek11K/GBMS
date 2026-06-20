"""
URL configuration for pyproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# import settings,static

# manually renamed the admin portal 
admin.site.site_header = "Gharbhanda Admin"
admin.site.site_title = "Gharbhanda Admin Portal"
admin.site.index_title = "Welcome to Gharbhanda admin Portal"

urlpatterns = [
    # in url if entered /admin render the inbuilt admin portal
    path('admin/', admin.site.urls),
    # whatever is entered i.e. /home or /contact find relevant url in pyapp,which directs to views and render the relevant content
    path('',include('pyapp.urls'))
]
# for supporting the media files used in Home models
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
