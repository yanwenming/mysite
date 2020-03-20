from django.contrib import admin
from .models import BlogArticles


# Register your models here.
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title","author","publish_date")
    list_filter = ("publish_date","author")
    search_fields = ("title","body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish_date"
    ordering = ['-publish_date','author']

admin.site.register(BlogArticles,BlogArticlesAdmin)