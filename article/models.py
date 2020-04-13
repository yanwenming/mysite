from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone #1
from django.urls import reverse
from slugify import slugify


# Create your models here.


#文章栏目数据模型
class ArticleColumn(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'article_column')
    column = models.CharField(max_length = 200)
    created = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.column


#文章标签数据模型
class ArticleTag(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "tag")
    tag = models.CharField(max_length = 500)
    def __str__(self):
        return self.tag


#文章数据模型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "article") #文章作者，文章与作者属于一对多的关系
    title = models.CharField( max_length = 200) #文章标题
    slug = models.SlugField(max_length = 500) #用于将文章标题转化为英文跟-
    column = models.ForeignKey(ArticleColumn , on_delete = models.CASCADE, related_name = "article_column") #文章栏目，文章栏目与文章属于一对多的关系
    body = models.TextField() #文章内容
    created = models.DateTimeField(default = timezone.now) #文章创建时间
    updated = models.DateTimeField(auto_now = True) #文章更新时间
    user_like = models.ManyToManyField(User,related_name = "article_like",blank = True)
    # article_tag = models.ManyToManyField(ArticleTag,related_name = "article_tag",blank = True)
    article_tag = models.ManyToManyField(ArticleTag,related_name = 'article_tag',blank = True)

    class Meta:
        ordering = ("-updated",) #按照更新时间updated字段进行降序排序，最新的放在最前面
        # ordering = ("updated" ,)  # 按照更新时间updated字段进行升序排序，最久的放在最前面
        index_together = (('id', 'slug'),) #对数据库中这2个字段建立索引

    def __str__( self ):
        return self.title  #__str__方法返回一个字符串，当做这个对象的描写

    #对默认的save方法进行重写
    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost , self).save(*args, **kargs)

    def get_absolute_url( self ):
        return reverse("article:article_detail", args = [self.id , self.slug])  #得到相应文章的路径

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

