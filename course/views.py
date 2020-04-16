from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView,DeleteView
from .models import Course,Lesson
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm,CreateLessonForm
from django.urls import reverse_lazy
from django.http import HttpResponse
import json
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin


# Create your views here.

#课程列表视图
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
    context_object_name = "courses"  #此处的courses返回的是request.user名下创建的courses，原因是通过继续UserMinxin的return实现
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
    success_url = reverse_lazy("course:manage_course") #删除成功，跳转的页面

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


#课程内容的视图方法
class CreateLessonView(LoginRequiredMixin,View):
    model = Lesson
    login_url = "/account/login/"

    def get( self,request,*args,**kwargs ):
        form = CreateLessonForm(user = self.request.user)
        return render(request,"course/manage/create_lesson.html",{"form":form})

    def post( self,request,*args,**kwargs ):
        form = CreateLessonForm(self.request.user,request.POST,request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit = False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")


class ListLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = 'course/manage/list_lessons.html'

    def get( self,request,course_id ):
        course = get_object_or_404(Course,id=course_id)
        return self.render_to_response({'course':course})


#课程内容详情视图
class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = "course/manage/detail_lesson.html"

    def get( self,request,lesson_id ):
        lesson = get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({"lesson":lesson})


class StudentListLessonView(ListLessonView):
    template_name = "course/slist_lessons.html"  #指定前端展示的模板html

    def post(self , request , *args , **kwargs):
        course = Course.objects.get(id = kwargs['course_id'])
        course.student.add(self.request.user)
        return HttpResponse("ok")
