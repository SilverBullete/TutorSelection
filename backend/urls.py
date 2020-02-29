from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login),
    path('create', views.create),
    path('update_password', views.update_password),
    path('get_info', views.get_user_info),
    path('student/get_resume', views.get_student_resume),
    path('student/update_resume', views.update_resume),
    path('student/get_teachers', views.get_teachers),
    path('student/get_teachers_by_institute', views.get_teachers_by_institute),
    path('student/update_selection', views.update_selection),
    path('student/get_selection_res', views.get_selection_result),
]
