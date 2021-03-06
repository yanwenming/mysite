from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ArticleColumn,ArticlePost,Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.db.models import Count

import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


#文章标题列表视图
def article_titles(request,username=None):
    if username: #当username有值时
        user = User.objects.get(username = username) #根据传入的username获取用户对象
        articles_title = ArticlePost.objects.filter(author = user) #获取指定用户名下所有的文章信息
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else :
        articles_title = ArticlePost.objects.all() #获取所有的文章信息
        # articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title , 5) #进行分页处理，每页显示5条记录
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

    if username:
        return render(request, "article/list/author_articles.html",
                        {"articles": articles , "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})


#文章详情视图
def article_detail(request, id, slug):
    article = get_object_or_404( ArticlePost, id = id, slug = slug ) #调用django get_object_or_404方法，它会默认的调用django 的get方法， 如果查询的对象不存在的话，会抛出一个Http404的异常
    total_views = r.incr( "article:{}:views".format ( article.id ) ) #记录每一个文章的访问次数
    r.zincrby( 'article_ranking' , 1 , article.id ) #根据amount所设定的值增加有序集合name中的value值

    article_ranking = r.zrange( "article_ranking" , 0 , -1 , desc = True )[:10] #获取article_ranking中排序前10的对象
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list( ArticlePost.objects.filter( id__in = article_ranking_ids ) )
    most_viewed.sort( key = lambda x : article_ranking_ids.index ( x.id ) )

    if request.method == "POST" :
        comment_form = CommentForm( data = request.POST )
        if comment_form.is_valid() :
            new_comment = comment_form.save( commit = False )
            new_comment.article = article
            new_comment.save()
    else :
        comment_form = CommentForm ()
    article_tags_ids = article.article_tag.values_list("id" , flat = True)
    similar_articles = ArticlePost.objects.filter(article_tag__in = article_tags_ids).exclude(id = article.id)
    similar_articles = similar_articles.annotate(same_tags = Count("article_tag")).order_by('-same_tags','-created')[:4]
    return render ( request , "article/list/article_content.html" ,
                    {"article": article , "total_views": total_views , "most_viewed": most_viewed ,
                     "comment_form": comment_form,"similar_articles":similar_articles})
    # return render(request, "article/list/article_content.html", {"article":article})


#文章点赞视图
@csrf_exempt
@require_POST
@login_required(login_url = '/account/login/')
def like_article(request):
    article_id = request.POST.get("id") #得到前端以POST方式传递过来的id
    action = request.POST.get("action") #得到前端以POST方式传递过来的action
    if article_id and action:
        try:
            article =ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.user_like.add(request.user) #将article实例对象与user实例对象建立关联，通过add在article_articlepost_user_like表增加一个记录，表示那个用户点赞了这篇文章
                return HttpResponse("1")
            else:
                article.user_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")