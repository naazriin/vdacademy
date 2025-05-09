from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import *
from .forms import *

def format_number(number):
    if number >= 1000:
        return {'value': round(number / 1000, 1), 'suffix': 'K'}
    return {'value': number, 'suffix': ''}


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    posts = BlogPost.objects.filter(category=category)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category_detail.html', context)


def home(request):
    image = HeroBanner.objects.all()
    about_section = AboutSection.objects.first()

    categories = Category.objects.all()
    courses = Course.objects.all()
    testimonials = Testimonial.objects.all()
    instructors = Instructor.objects.all()
    brands = PartnerBrand.objects.all()
    blogs = BlogPost.objects.order_by('-published_date')[:6]

    course_count = Course.objects.count()
    instructor_count = Instructor.objects.count()
    member_count = Testimonial.objects.count()
    award_count = AboutSection.objects.count()
    enrolled = Testimonial.objects.count()
    completed = Course.objects.filter(is_completed=True).count()

    faq_categories = FaqCategory.objects.all()
    selected_category_id = request.GET.get('faq_category')

    if selected_category_id:
        faqs = Faq.objects.filter(category_id=selected_category_id)
    else:
        faqs = Faq.objects.all()



    context = {
        'categories': categories,
        'courses': courses,
        'testimonials': testimonials,
        'instructors': instructors,
        'brands': brands,
        'blogs':blogs,
        'course_count': course_count,
        'instructor_count': instructor_count,
        'member_count': member_count,
        'award_count': award_count,
        'enrolled_data': format_number(enrolled),
        'completed_data': format_number(completed),
        'image': image,
        'about_section': about_section,
 
        'faq_categories': faq_categories,
        'faqs': faqs,
    

    }
    return render(request, 'index.html', context)



def about(request):
    student_count = Course.objects.count()
    enrolled = Testimonial.objects.count()
    completed = Course.objects.filter(is_completed=True).count()
    total_participants = Course.objects.aggregate(total=models.Sum('students'))['total']

    instructors = Instructor.objects.all()
    testimonials = Testimonial.objects.all()
    brands = PartnerBrand.objects.all()

    if total_participants is None:
        total_participants = 0

    instructor_count = Instructor.objects.count()
    about_section = AboutSection.objects.first()
    why_chooses = WhyChoose.objects.all()

    context = {
        'enrolled_data': format_number(enrolled),
        'completed_data': format_number(completed),
        'student_count': round(total_participants / 1000, 1),  
        'instructor_count': instructor_count,
        'about_section': about_section,
        'why_chooses': why_chooses,
        'instructors': instructors,
        'testimonials':testimonials,
        'brands': brands,

    }
    return render(request, 'about-one.html', context)




def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})





def subscribe_newsletter(request):
    categories = Category.objects.all()
 
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "This email is already subscribed to our newsletter.")
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
                return redirect('home')
    else:
        form = NewsletterForm()

    context = {
        'categories': categories,
        'form': form,
    }

    return render(request, 'base.html', context)