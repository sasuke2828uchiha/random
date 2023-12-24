from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/',include("allauth.urls")),
    path("stulogin",views.stulogin),
    path("logout",views.log_out),
    path("stuhome",views.stuhome,name='stuhome'),
    path("",views.stulogin,name='stulogin'),
    path("feedback",views.feedback, name = 'feedback'),
    path("rating",views.menu_rating,name = "rating"),
    path('inc-attendance/', views.inc_attendance, name='inc_attendance'),
    path('stu_info',views.student_data,name="stu_info"),
    path('monthlymenu',views.monthmenu,name="monthmenu"),
]

