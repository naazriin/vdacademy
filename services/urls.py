from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('courses/<int:id>/', course_detail, name='course-detail'),
    path('load-more-courses/', load_more_courses, name='load-more-courses'),


]
