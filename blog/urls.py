from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('',views.blog_title,name='blog_title'),  #name是别名
    path('<int:article_id>/',views.blog_article,name='blog_article'), #views.blog_article也可以加上"",用"views.blog_article"显示
]
