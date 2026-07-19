from django.urls import path
from . import views

# all the url are defined here the url which we hit in navbar corresponds here and views execute or render the content relevantly
urlpatterns = [
    path('', views.pyapp, name='pyapp'),
    path('contact', views.contact, name='contact'),
    path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
    path("about.html", views.about, name="about.html"),
    path("loginUser", views.loginUser, name="loginUser"),
    path("logout", views.logout, name="logout"),

    # roomseeker
    path("home.html", views.home_data, name="home.html"),
    path('home/<int:pk>/', views.view_details, name='view_details'),
    path("apply/<int:pk>/", views.process_apply, name="process_apply"),
    path("llhome/<int:pk>/",views.view_details,name="view_details"),
    path("my-applications", views.my_applications, name="my_applications"),

    # landlord
    path("llhome", views.llhome, name="llhome"),
    path("add.html", views.add, name="add.html"),
    path("notify.html", views.notify, name="notify.html"),
    path("notify", views.notify, name="notify"),
    path("application/<int:pk>/<str:status>/", views.update_application_status, name="update_application_status"),
    path("llprofile", views.llprofile, name="llprofile"),
    path(
    "rs_notifications/",
    views.rs_notifications,
    name="rs_notifications"
    ),
    path("llapplications",views.llapplications,name="llapplications"),
    path("llhome/<int:pk>/edit/",views.edit_home,name="edit_home"),
    path("llhome/<int:pk>/delete/",views.delete_home,name="delete_home"),
    path('application/<int:pk>/cancel/', views.cancel_application, name='cancel_application'),
    path("llapplications/<int:pk>/cancel/",views.ll_cancel_application,name="ll_cancel_application")
]
