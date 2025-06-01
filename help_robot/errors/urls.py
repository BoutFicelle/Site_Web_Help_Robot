from django.urls import path
from . import views

app_name = 'errors'

urlpatterns = [
    path('', views.home, name='home'),
    path('fanuc/', views.fanuc_search, name='fanuc_search'),
    path('abb/', views.abb_coming_soon, name='abb_coming_soon'),
    path('kuka/', views.kuka_coming_soon, name='kuka_coming_soon'),
]