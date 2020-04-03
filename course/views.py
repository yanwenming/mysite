from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,DeleteView
from .models import Course
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm
from django.urls import reverse_lazy
from django.http import HttpResponse
import json


# Create your views here.


class CourseListView(ListView):
    model = Course #获取Course中的所有数据
    context_object_name = "courses" #声明传入模板course_list.html中的变量名称
    template_name = 'course/course_list.html' #指定模板


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = "/account/login" #当用户没有登录的时候，强制跳转到登录页面


class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


#新增课程的方法
class CreateCourseView(UserCourseMixin,CreateView):
    fields = ['title','overview'] #声明在表单中显示的字段
    template_name = 'course/manage/create_course.html'  #指定前端展示的html模板

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data = request.POST)
        if form.is_valid():
            new_course = form.save(commit = False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course") #当表单数据保存以后，重新跳转到指定页面
        return self.render_to_response({"form":form})


#删除课程的方法
class DeleteCourseView(UserCourseMixin, DeleteView):
    #template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy("course:manage_course")

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp
