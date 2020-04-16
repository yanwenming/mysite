from django import forms
from .models import Course,Lesson


#创建课程表单
class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields =("title","overview")


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course','title','video','description','attach']

    def __init__(self,user,*args,**kwargs):
        super(CreateLessonForm,self).__init__(*args,**kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)