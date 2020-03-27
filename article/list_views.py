from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ArticleColumn,ArticlePost
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


def article_titles(request,username=None):
    if username:
        user = User.objects.get(username = username)#获取用户对象
        articles_title = ArticlePost.objects.filter(author = user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else :
        articles_title = ArticlePost.objects.all()
        # articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title , 2)
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

    if username :
        return render(request, "article/list/author_articles.html",
                        {"articles": articles , "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})


def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    total_views = r.incr("article:{}:views".format(article.id)) #记录每一个文章的访问次数
    r.zincrby('article_ranking',1,article.id) #1 根据amount所设定的值增加有序集合name中的value值
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10] #2获取article_ranking中排序前10的对象
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids)) #3
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    return render(request,"article/list/article_content.html",{"article":article,"total_views":total_views,"most_viewed":most_viewed})


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
                article.user_like.add(request.user)
                return HttpResponse("1")
            else:
                article.user_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")