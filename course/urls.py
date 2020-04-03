from django.urls import path
from django.views.generic import TemplateView
from .views import CourseListView,ManageCourseListView


app_name = "course"

urlpatterns = [
    path('about/',TemplateView.as_view(template_name="course/about.html"),name="about"),
    path('course-list/',CourseListView.as_view(),name="course_list"),
    path('manage-course/',ManageCourseListView.as_view(),name="manage_course"),
]
