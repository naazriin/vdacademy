from django.shortcuts import render, get_object_or_404
from core.models import Course
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def course_list(request):
    courses = Course.objects.all()
    sort_by = request.GET.get('sort_by')
    courses = Course.objects.all()

    paginator = Paginator(courses, 3) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)


    if sort_by == 'low_to_high':
        courses = courses.order_by('price')
    elif sort_by == 'high_to_low':
        courses = courses.order_by('-price')
    elif sort_by == 'last_viewed':
        courses = courses.order_by('-id')

        
    return render(request, 'course-three.html', {
        'courses': page_obj.object_list,
        'course_count': courses.count(),
        'page_obj': page_obj,

        'courses': courses,
        'course_count': courses.count()
    })



def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'index.html', {
        'course': course
    })




def load_more_courses(request):
    page_number = request.GET.get('page', 3)  
    courses = Course.objects.all()
    paginator = Paginator(courses, 6) 
    page_obj = paginator.get_page(page_number)

    courses_html = render_to_string('partials/course_card.html', {'courses': page_obj.object_list})

    return JsonResponse({
        'courses_html': courses_html,
        'has_next': page_obj.has_next(),  
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None, 
    })
