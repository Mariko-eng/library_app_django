from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 

app_name = 'users'

urlpatterns = [
    path('users/login',views.index, name="login"),
    path('users/register',views.registerView, name="register"),
    path('users/logout',views.logoutView, name="logout"),

    path('users/sm',views.send_mail_now),

    path('users/reset_password/', 
         auth_views.PasswordResetView.as_view(
            template_name ="accounts/password_reset.html"
             ),name="reset_password"), # Submit Email Form
    path('users/reset_password/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name ="accounts/password_reset_send.html"),name="password_reset_done"), # Email Sent Success Message
    path('users/reset_password/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name ="accounts/password_reset_form.html"),
         name="password_reset_confirm"), # Link to Password Reset ConfirmmView
    path('users/reset_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name ="accounts/password_reset_done.html"),name="password_reset_complete"), # Password Successfully Changed Message
]



# from .views import LoginTokenObtainView
# from .views import LoginTokenRefreshView
# from .views import BlackListTokenView
# from .views import GenerateOtpView
# from .views import VerifyOTPView
# #### Users ####
# from .views import RegisterSocUserCreateAPIView
# from .views import EditSocUserUpdateAPIView
# from .views import RegisterSfiUserCreateAPIView
# from .views import EditSfiUserUpdateAPIView
# from .views import UserListAPIView
# from .views import UserRetrieveAPIView
# from .views import UserDestroyAPIView
# #### Sfis ####
# from .views import RegisterSfiCreateAPIView
# from .views import EditSfiUpdateAPIView
# from .views import SfiListAPIView
# from .views import SfiRetrieveAPIView
# from .views import SfiDestroyAPIView
# from .views import SendOtpEmailView


# urlpatterns = [
#     path('users/token/login/',LoginTokenObtainView.as_view()),
#     path('users/token/refresh/',LoginTokenRefreshView.as_view()),
#     path('users/token/blacklist/', BlackListTokenView.as_view()),
#     path('users/otp/generate/', GenerateOtpView.as_view()),
#     path('users/otp/verify/', VerifyOTPView.as_view()),

#     ###
#     path('users/otp/send_email/', SendOtpEmailView.as_view()),


#     #### Users ####
#     path('users/soc/register/',RegisterSocUserCreateAPIView.as_view()),
#     path('users/soc/edit/<int:pk>/',EditSocUserUpdateAPIView.as_view()),
#     path('users/sfi/register/',RegisterSfiUserCreateAPIView.as_view()),
#     path('users/sfi/edit/<int:pk>/',EditSfiUserUpdateAPIView.as_view()),
#     path('users/list/',UserListAPIView.as_view()),
#     path('users/retrieve/<int:pk>/',UserRetrieveAPIView.as_view()),
#     path('users/delete/<int:pk>/',UserDestroyAPIView.as_view()),

#     #### SIi ####
#     path('sfi-entity/register/',RegisterSfiCreateAPIView.as_view()),
#     path('sfi-entity/edit/<int:pk>/',EditSfiUpdateAPIView.as_view()),
#     path('sfi-entity/list/',SfiListAPIView.as_view()),
#     path('sfi-entity/retrieve/<int:pk>/',SfiRetrieveAPIView.as_view()),
#     path('sfi-entity/delete/<int:pk>/',SfiDestroyAPIView.as_view())
# ]