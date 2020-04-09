from django.contrib import admin
from .models import BlogArticles


# Register your models here.
class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title","author","publish_date")  #设置列表展示的字段
    list_filter = ("publish_date","author","publish_date") #设置列表字段排序
    search_fields = ("title","body")  #设置查询条件
    raw_id_fields = ("author",)
    date_hierarchy = "publish_date"
    ordering = ['-publish_date','author']


admin.site.register(BlogArticles,BlogArticlesAdmin)

# admin.site.register(BlogArticles)