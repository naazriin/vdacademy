from django.urls import path
from .views import *


urlpatterns = [
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),

]