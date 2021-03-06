from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


#博客数据模型类
class BlogArticles(models.Model):
    title = models.CharField(max_length = 300)
    author = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "blog_ports")
    body = models.TextField()
    publish_date = models.DateTimeField(default = timezone.now)

    class Meta:
        #按照publish字段值倒序显示
        ordering = ("-publish_date",)

    def __str__(self):
        return self.title

