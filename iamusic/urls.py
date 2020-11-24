from django.urls import path
from iamusic import views

urlpatterns = [
    path('', views.home),
    path('new', views.new),
    path('ask', views.ask),
    path('submit', views.submit),
    path('results', views.results)
]
