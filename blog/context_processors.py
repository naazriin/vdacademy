from core.models import Tag
from .models import BlogPost


def all_tags(request):
    return {
        'all_tags': Tag.objects.all()
    }


def latest_blog_post(request):
    latest_post = BlogPost.objects.order_by('-published_date').first()
    return {'latest_blog_post': latest_post}