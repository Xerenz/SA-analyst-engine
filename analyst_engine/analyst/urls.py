from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('malware/', views.search, name='malware'),
    path('malware/', views.update, name='change'),
]