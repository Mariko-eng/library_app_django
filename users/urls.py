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