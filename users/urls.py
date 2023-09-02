from django.urls import path
from . import views 


app_name = 'users'

urlpatterns = [ 
    path('',views.index),
    path('users/login',views.index, name="login"),
    path('users/register',views.registerView, name="register"),
    path('users/logout',views.logoutView, name="logout"),

    path('users/sm',views.send_mail_now),

     ### USERS
     path('users/list/',views.users_list_view,name="user_list"),
     path('users/new/',views.users_new_view,name="user_new"),
     path('users/list/search/',views.users_search,name="user_list_search"),
     path('users/detail/<int:pk>',views.users_detail_view,name="user_detail"),
     path('users/delete/<int:pk>',views.users_delete_view,name="user_delete"),

     ### USERS
     path('users/attendance/list/',views.attendance_list_view,name="attendance_list"),
     path('users/attendance/list/search/',views.attendance_search,name="attendance_list_search"),

     ### DEVICES
     path('users/device/list/',views.device_list_view,name="device_list"),
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