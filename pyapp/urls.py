from django.urls import path
from .import views


# all the url are defined here the url which we hit in navbar corresponds here and views execute or render the content relevantly
urlpatterns = [
    path('', views.pyapp, name='pyapp'),# ''it refers blank path and  if 'initial\' this means in url /initial need to be added
    # path('home', views.home, name="home"),
    path('contact', views.contact, name='contact'),
    path("profile", views.profile, name="profile"),
    path("register",views.register,name="register"),
    path("about.html",views.about,name="about.html"),
    path("loginUser",views.loginUser,name="loginUser"),
    path("logout",views.loginUser,name="logout"),
    # path("viewhtml",views.viewhtml,name="viewhtml"),
    path("home.html",views.home_data, name="home.html"),
    # path("vd/<int:pk>/",views.view_details,name="view_details"),
    path('home/<int:pk>/', views.view_details, name='view_details'),
    path("llhome",views.llhome,name="llhome"),
   path("apply/<int:pk>/", views.process_apply, name="process_apply"),
   path("add.html",views.add,name="add.html"),
   path("notify.html",views.notify,name="notify.html"),
   path("llprofile",views.llprofile,name="llprofile")
]
