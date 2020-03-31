from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone #1
from django.urls import reverse
from slugify import slugify


# Create your models here.


class ArticleColumn(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'article_column')
    column = models.CharField(max_length = 200)
    created = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.column


#文章标签
class ArticleTag(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "tag")
    tag = models.CharField(max_length = 500)
    def __str__(self):
        return self.tag


class ArticlePost(models.Model) :
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "article")
    title = models.CharField( max_length = 200)
    slug = models.SlugField(max_length = 500)
    column = models.ForeignKey( ArticleColumn , on_delete = models.CASCADE , related_name = "article_column")
    body = models.TextField()
    created = models.DateTimeField(default = timezone.now)
    updated = models.DateTimeField(auto_now = True)
    user_like = models.ManyToManyField(User,related_name = "article_like",blank = True)
    article_tag = models.ManyToManyField(ArticleTag,related_name = "article_tag",blank = True)

    class Meta :
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)

    def __str__( self ) :
        return self.title

    def save(self , *args , **kargs) :
        self.slug = slugify( self.title)
        super(ArticlePost , self ).save(*args , **kargs)

    def get_absolute_url( self ) :
        return reverse( "article:article_detail" , args = [self.id , self.slug])

    def get_url_path( self ):
        return reverse("article:article_content", args = [self.id , self.slug])


#评论功能数据模型
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost,on_delete = models.CASCADE,related_name = "comments") #将本数据模型与ArticlePost数据模型建立多对一的关系，即一篇文章可以有多条评论
    commentator = models.CharField(max_length = 90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-created',) #按照created的倒序排序

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username,self.article)

