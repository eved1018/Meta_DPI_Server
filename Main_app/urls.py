from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "Main_App_Home"),
    path('Results/', views.Results, name = "Main_App_Results"),
    path('About/', views.About, name = "Main_App_about"),
    path('Refrences/',views.Refrences,name="Main_App_Refrences")

]