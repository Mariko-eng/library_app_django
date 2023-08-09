from django.urls import path
from .views_api import LoginTokenObtainView
from .views_api import LoginTokenRefreshView
from .views_api import BlackListTokenView
from .views_api import LoggedInUserView
from .views_api import AttendanceCreateAPIView
from .views_api import AttendanceListAPIView

urlpatterns = [
    path('users/token/login/',LoginTokenObtainView.as_view()),
    path('users/token/refresh/',LoginTokenRefreshView.as_view()),
    path('users/token/blacklist/', BlackListTokenView.as_view()),
    path('users/get-logged-in-user/',LoggedInUserView.as_view()),

    path('users/attendance/add/', AttendanceCreateAPIView.as_view()),
    path('users/attendance/list/', AttendanceListAPIView.as_view()),
]