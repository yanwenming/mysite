from django import forms
from .models import ArticleColumn,ArticlePost,Comment,ArticleTag


#栏目表单类
class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)


#文章表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body") #将ArticlePost表中的字段拿出来，需要什么字段拿什么字段，这里列出来只需要拿title,body2个字段


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  #指定数据源
        fields = ("commentator","body",)


#文章标签表单类
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)