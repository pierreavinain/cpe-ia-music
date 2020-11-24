from django.urls import path
from iamusic import views

urlpatterns = [
    path(r'', views.home, name='home'),
]
