from django.urls import path
from .views import *

urlpatterns = [
    path("team", team_view, name='team-3'),
    
]