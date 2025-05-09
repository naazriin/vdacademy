from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from core.models import BlogPost, Tag, Course, Category
from .models import Comment
from .forms import *
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def blog_list_view(request):
    blog_posts = BlogPost.objects.all()

    paginator = Paginator(blog_posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog-masonry.html', {'page_obj': page_obj})



def blog_page(request):
    query = request.GET.get('q')
    posts = BlogPost.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    
    else:
        posts = BlogPost.objects.none()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        post_list = [
            {
                'title': post.title,
                'content': post.content[:150] + '...',
                'slug': post.slug,
            }
            for post in posts
        ]
        return JsonResponse({'posts': post_list})

        

    context = {
        'posts': posts,
        'query': query,
        
    }
    return render(request, 'blog-details.html', context)





def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    previous_post = BlogPost.objects.filter(published_date__lt=post.published_date).order_by('-published_date').first()
    next_post = BlogPost.objects.filter(published_date__gt=post.published_date).order_by('published_date').first()
    
    archives = Course.objects.annotate(month=TruncMonth('created_at')) \
                              .values('month') \
                              .annotate(course_count=Count('id')) \
                              .order_by('-month')
    
    categories = Category.objects.annotate(post_count=Count('posts'))

    blog_post = get_object_or_404(BlogPost, slug=slug)
    
    latest_posts = BlogPost.objects.exclude(id=blog_post.id).order_by('-published_date')[:5]


    comments = post.comments.filter(parent__isnull=True) 

        
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            
            if request.user.is_authenticated:
                comment.author = request.user
                comment.name = request.user.username
                comment.email = request.user.email
            else:
                comment.name = form.cleaned_data['name']
                comment.email = form.cleaned_data['email']
            
            comment.post = post 
            comment.save() 
            return redirect('blog_detail', slug=slug)  
    else:
        if request.user.is_authenticated:
            initial_data = {'name': request.user.username, 'email': request.user.email}
            form = CommentForm(initial=initial_data)  
        else:
            form = CommentForm()
    

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,

        'archives': archives,
        'categories': categories,
        
        'blog_post': blog_post,
        'latest_posts': latest_posts,
        
    }
    return render(request, 'blog-details.html', context)




@login_required
@csrf_exempt
def post_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        comment_id = data.get('comment_id')
        
        if content and comment_id:
            comment = Comment.objects.get(id=comment_id)
            reply = Comment.objects.create(
                content=content,
                author=request.user,
                parent=comment,
                post=comment.post  
            )
            reply.save()

            response_data = {
                'success': True,
                'reply': {
                    'author_username': reply.author.username,
                    'author_profile_picture': reply.author.userprofile.profile_picture.url if reply.author.userprofile.profile_picture else '/static/assets/images/blog/default-user.jpg',
                    'created_at': reply.created_at.strftime("%b %d, %Y"),
                    'content': reply.content
                }
            }
            return JsonResponse(response_data)

        return JsonResponse({'success': False}, status=400)




def tagged_blogs(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    
    posts = BlogPost.objects.filter(tags=tag)

    all_tags = Tag.objects.all()

    context = {
        'posts': posts,
        'tag': tag,
        'all_tags': all_tags  
    }

    return render(request, 'blog-details.html', context)



