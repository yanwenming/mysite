from django import template
register = template.Library()
from article.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()#返回文章数量的查询结果


@register.simple_tag
def author_total_articles(user):
    return user.article.count()#得到某用户的文章总数


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n] #按照created时间倒序查询，排名前n的文章
    return {"latest_articles":latest_articles}