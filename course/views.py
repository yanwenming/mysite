from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import Course

# Create your views here.


class CourseListView(ListView):
    model = Course #获取Course中的所有数据
    context_object_name = "courses" #声明传入模板course_list.html中的变量名称
    template_name = 'course/course_list.html' #指定模板


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin):
    model = Course


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'
