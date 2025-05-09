from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.user.username




class Category(models.Model):
    CATEGORY_CHOICES = [
        ('business_management', 'Business Management'),
        ('arts_design', 'Arts & Design'),
        ('personal_development', 'Personal Development'),
        ('health_fitness', 'Health & Fitness'),
        ('data_science', 'Data Science'),
        ('marketing', 'Marketing'),
        ('business_finance', 'Business & Finance'),
        ('computer_science', 'Computer Science'),
        ('video_photography', 'Video & Photography'),
    ]

    name = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(max_length=100)  
    link = models.URLField()  
    color_class = models.CharField(max_length=100)  
    
    def __str__(self):
        return self.get_readable_name()
    
    def get_readable_name(self):
        return self.name.replace('_', ' ').title()
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def course_count(self):
        return self.courses.count()



class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='course_images/')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    duration = models.CharField(max_length=50)  
    price = models.IntegerField()
    lessons = models.PositiveIntegerField()
    students = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1, related_name="courses")  
    created_at = models.DateTimeField(auto_now_add=True)


    details = models.TextField(blank=True)  


    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('score'))['score__avg'], 1)
        return 0

    @property
    def rating_count(self):
        return self.ratings.count()

    def __str__(self):
        return self.title



class Rating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.course.title} - {self.score} stars"


class HeroBanner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='banner_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    video_thumbnail = models.ImageField(upload_to='about_images/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    award_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class AboutImage(models.Model):
    about_section = models.ForeignKey(AboutSection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='about_images/')

    def __str__(self):
        return f"Image for {self.about_section.title}"
    

class WhyChoose(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50) 
    color_class = models.CharField(max_length=50)  

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='authors/')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('online', 'Online'),
        ('lecture', 'Lecture'),
        ('business', 'Business'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    published_date = models.DateField()
    comments_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    extra_categories = models.CharField(max_length=255, blank=True, help_text="for blog details page")
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    category_c = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        while BlogPost.objects.filter(slug=self.slug).exists():
            self.slug = slugify(self.title + "-" + str(self.pk))
        super().save(*args, **kwargs)


    def get_extra_categories_list(self):
        return [cat.strip() for cat in self.extra_categories.split(',') if cat.strip()]
    
    def __str__(self):
        return self.title



class BlogSection(models.Model):
    blog = models.ForeignKey(BlogPost, related_name='sections', on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    body = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.blog.title} - {self.heading}"



class BlogSectionImage(models.Model):
    section = models.ForeignKey(BlogSection, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_sections/')



class SiteStatistic(models.Model):
    students_enrolled = models.PositiveIntegerField(default=0)
    classes_completed = models.PositiveIntegerField(default=0)
    top_instructors = models.PositiveIntegerField(default=0)
    satisfaction_rate = models.DecimalField(max_digits=5, decimal_places=2, default=99.99)  
    
    def __str__(self):
        return "Site Statistics"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}"
    
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='instructors/')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return self.rating


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)  
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)  
    image = models.ImageField(upload_to='testimonials/')
    
    enrolled_courses = models.ManyToManyField('Course', blank=True)

    def __str__(self):
        return self.name



class FaqCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Faq(models.Model):
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question




class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class PartnerBrand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/')

    def __str__(self):
        return self.name