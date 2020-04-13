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
        fields = ("title","body")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  #指定数据源
        fields = ("commentator","body",)


#文章标签表单类
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)