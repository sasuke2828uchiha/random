from django.urls import path

from . import views

urlpatterns = [
    path("",views.login_user, name="login_u"),
    path("login_user",views.login_user, name="login_u"),
    path("logout",views.log_out),
    path("signup_staff",views.signup_user,name="signup"),
    path("staff_home",views.staff_home,name="staffhome"),
    path("feedback_view",views.feedback_view, name = "feedback_view"),
    path("bill",views.bill, name = "bill"),
    path("user_bills",views.user_bills,name='user_bills')

]

