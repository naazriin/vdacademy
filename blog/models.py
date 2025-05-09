from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from core.models import BlogPost
from django.conf import settings 


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    name = models.CharField(max_length=100, default="Anonymous") 
    email = models.EmailField(default="no-reply@example.com")            
    content = models.TextField(_('Content'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        return f'{_("Comment by")} {self.author.username} {_("on")} {self.post.title}'
