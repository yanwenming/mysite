from django.shortcuts import render,get_object_or_404
from .models import BlogArticles

# Create your views here.


#博客标题方法
def blog_title(request):
    blogs = BlogArticles.objects.all()  #得到所有BlogArticles类的实例
    return render(request,"blog/titles.html",{"blogs":blogs})  #将数据渲染到指定的模板templates上


#博客文章详情方法
def blog_article(request,article_id):  #传入博客文章id
    # article = BlogArticles.objects.get(id=article_id)
    article = get_object_or_404(BlogArticles,id=article_id)  #对BlogArticles依据id进行查询，如果没有查询到任何数据，就返回404错误
    pub = article.publish_date
    return render(request,"blog/content.html",{"article":article,"publish_date":pub})