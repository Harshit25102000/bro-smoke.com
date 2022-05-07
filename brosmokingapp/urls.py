from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path("", views.index,name="Home"),
    path("myaccount/", views.myaccount,name="myaccount"),
    path("make_entry", views.make_entry,name="make_entry"),
    path("handle_signup", views.handle_signup,name="handle_signup"),
    path("handle_login", views.handle_login,name="handle_login"),
    path("signup", views.signup,name="signup"),
    path("login", views.loginpage,name="login"),
    path("logout", views.handleLogout,name="handleLogout"),
    path("about", views.about,name="about"),
    path("allbros", views.allbros,name="allbros"),
    path("contact", views.contact,name="contact"),
    path("searchresult", views.searchresult,name="searchresult"),
    path("handlecontactus", views.handlecontactus,name="handlecontactus"),
    path("history", views.history,name="history"),
    path("forgotpassword", views.forgotpassword,name="forgotpassword"),
    path("handle_username", views.handle_username,name="handle_username"),
    path("change_password", views.change_password,name="change_password"),
    path("handle_changepassword", views.handle_changepassword,name="handle_changepassword"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="brosmokingapp/password_reset.html"),
    name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="brosmokingapp/password_reset_sent.html"),
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
    template_name="brosmokingapp/password_reset_confirm.html"),
    name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(
    template_name="brosmokingapp/password_reset_complete.html"), name="password_reset_complete"),


]