from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from .fields import OrderField

# Create your models here.


#课程数据模型
class Course(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "courses_user")
    title = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200,unique = True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    student = models.ManyToManyField(User,related_name = "courses_joined",blank = True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super(Course,self).save(*args,**kwargs)

    def __str__(self):
        return self.title


def user_directory_path(instance,filename):
    return "courses/user_{0}/{1}".format(instance.user.id,filename)


#课程内容的数据模型
class Lesson(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "lesson_user")
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name = "lesson")
    title = models.CharField(max_length = 200)
    video = models.FileField(upload_to = user_directory_path) #用于接收上传的视频
    description = models.TextField(blank = True)
    attach = models.FileField(blank = True,upload_to = user_directory_path) #用于接收上传的附件
    created = models.DateTimeField(auto_now_add = True)
    order = OrderField(blank = True,for_fields = ['course'])  #order用来存储某内容在相应的课程标题Course中的序号，默认序号从0开始

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)
