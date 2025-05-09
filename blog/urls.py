from django.urls import path
from .views import *

urlpatterns = [
    path('', blog_list_view, name='blog_list'),
    path('post-reply/', post_reply, name='post_reply'),
    path('tag/<str:tag_name>/', tagged_blogs, name='tagged_blogs'),
    path('blog/', blog_page, name='blog_page'),
    path('<slug:slug>/', blog_detail, name='blog_detail'), 


]


