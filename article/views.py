from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn,ArticlePost,ArticleTag
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import ArticleColumnForm,ArticlePostForm,ArticleTagForm
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json

# Create your views here.


#新增栏目的视图
@login_required(login_url = '/account/login')
@csrf_exempt #解决提交表单中遇到的CSRF问题的一种方式
def article_column(request):
    # columns = ArticleColumn.objects.filter(user=request.user)
    # return render(request,"article/column/article_column.html",{"columns":columns}
    if request.method == "GET":
        columns_list = ArticleColumn.objects.filter(user=request.user)
        column_from = ArticleColumnForm()
        #下面是分页方法
        paginator = Paginator(columns_list,5)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            columns = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            columns = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            columns = current_page.object_list

        return render(request,"article/column/article_column.html",{"columns":columns,"column_form":column_from,"page": current_page})  #传入2个参数columns跟column_form到article_column.html模板中
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name) #7传入当前用户跟栏目名称2个参数后，来查询当前用户是否已经创建过当前的栏目名称，如果没有创建该栏目则允许创建提交，否则创建失败
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


#编辑栏目的视图
@login_required(login_url = '/account/login')
@require_POST  #目的是保证此视图函数只接受通过POST方法提交的数据
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id) #根据所要修改的栏目名称所在记录的id，查询到该数据，并建立实例对象
        line.column = column_name #重新赋值
        line.save() #将数据保存到数据库
        return HttpResponse("1")
    except:
        return HttpResponse("0")


#删除栏目的视图
@login_required(login_url = '/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"] #获取Ajax传过来的column_id
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete() # 删除该记录
        return HttpResponse("1")
    except:
        return HttpResponse("2")


#文章视图函数
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()#获取当前用户的所有文章标签
        return render(request, "article/column/article_post.html",{"article_post_form":article_post_form, "article_columns":article_columns, "article_tags":article_tags})


@login_required(login_url = '/account/login')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author = request.user)
    paginator = Paginator(articles_list, 2)
    page = request.GET.get('page')
    try :
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger :
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage :
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request , "article/column/article_list.html", {"articles": articles, "page": current_page})


@login_required(login_url = '/account/login')
def article_detail(request,id,slug):
    article=get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/column/article_detail.html",{"article":article})


@login_required(login_url = '/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url = '/account/login')
@csrf_exempt
def redit_article(request,article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial = {"title":article.title})
        this_article_column = article.column
        return render(request,"article/column/redit_article.html",
                      {"article":article,
                       "article_columns":article_columns,
                       "this_article_column":this_article_column,
                       "this_article_form":this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


@login_required ( login_url = '/account/login' )
@csrf_exempt
def article_tag( request ) :
    if request.method == "GET" :
        article_tags = ArticleTag.objects.filter ( author = request.user )
        article_tag_form = ArticleTagForm ()
        return render ( request , "article/tag/tag_list.html" ,
                        {"article_tags" : article_tags , "article_tag_form" : article_tag_form} )

    if request.method == "POST" :
        tag_post_form = ArticleTagForm ( data = request.POST )
        if tag_post_form.is_valid () :
            try :
                new_tag = tag_post_form.save ( commit = False )
                new_tag.author = request.user
                new_tag.save ()
                return HttpResponse ( "1" )
            except :
                return HttpResponse ( "the data cannot be save." )
        else :
            return HttpResponse ( "sorry, the form is not valid." )


@login_required(login_url = '/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id = tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
