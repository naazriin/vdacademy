from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("about/", about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('category/<int:id>/', category_detail, name='category_detail'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),


    
]
