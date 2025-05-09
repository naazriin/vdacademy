from django.shortcuts import render
from core.models import Instructor  

def team_view(request):
    instructors = Instructor.objects.all()
    return render(request, 'team-three.html', {'instructors': instructors})