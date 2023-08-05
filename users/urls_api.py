from django.urls import path
from .views_api import LoginTokenObtainView
from .views_api import LoginTokenRefreshView
from .views_api import BlackListTokenView
from .views_api import AttendanceListCreateAPIView

urlpatterns = [
    path('users/token/login/',LoginTokenObtainView.as_view()),
    path('users/token/refresh/',LoginTokenRefreshView.as_view()),
    path('users/token/blacklist/', BlackListTokenView.as_view()),

    path('users/attendance/list/', AttendanceListCreateAPIView.as_view()),
    path('users/attendance/add/', AttendanceListCreateAPIView.as_view()),
]