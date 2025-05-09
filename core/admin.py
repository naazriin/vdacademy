from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Testimonial)
admin.site.register(Instructor)
admin.site.register(PartnerBrand)
admin.site.register(ContactMessage)
admin.site.register(Course)
admin.site.register(FaqCategory)
admin.site.register(Faq)
admin.site.register(SiteStatistic)
admin.site.register(Newsletter)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(HeroBanner)
admin.site.register(Rating)
admin.site.register(WhyChoose)

class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [AboutImageInline]

class BlogSectionImageInline(admin.TabularInline):
    model = BlogSectionImage
    extra = 1

class BlogSectionAdmin(admin.ModelAdmin):
    inlines = [BlogSectionImageInline]

admin.site.register(BlogSection, BlogSectionAdmin)


class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlogSectionInline]
    filter_horizontal = ('tags',)

