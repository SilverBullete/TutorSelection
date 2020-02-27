from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login),
    path('create', views.create),
    path('student/get_selection_res', views.get_selection_result),
    path('student/get_info', views.get_user_info),
    path('student/get_teachers', views.get_teachers),
    path('student/get_teachers_by_institute', views.get_teachers_by_institute),
]