from django.urls import path
from django.views.generic import TemplateView
from .views import CourseListView,ManageCourseListView,CreateCourseView,DeleteCourseView,CreateLessonView,ListLessonView,DetailLessonView,StudentListLessonView,UpdateCourseView


app_name = "course"

urlpatterns = [
    path('about/',TemplateView.as_view(template_name="course/about.html"),name="about"), #关于本站
    path('course-list/',CourseListView.as_view(),name="course_list"), #课程列表
    path('manage-course/',ManageCourseListView.as_view(),name="manage_course"),
    path('create-course/',CreateCourseView.as_view(),name="create_course"),
    path('update-course/<int:pk>/',UpdateCourseView.as_view(),name="update_course"),
    path('delete-course/<int:pk>/',DeleteCourseView.as_view(),name="delete_course"),
    path('create-lesson/',CreateLessonView.as_view(),name="create_lesson"),
    path('list-lessons/<int:course_id>/',ListLessonView.as_view(),name="list_lessons"),
    path('detail-lessons/<int:lesson_id>/',DetailLessonView.as_view(),name="detail_lesson"),
    path('lessons-list/<int:course_id>/',StudentListLessonView.as_view(),name="lessons_list"),
]
