from django.urls import path
from . import views 
from users.views import attendance_list_view

app_name = 'main'

urlpatterns = [
    # path('home',views.index, name="home"),
    path('home',attendance_list_view, name="home"),
    path('categories/list',views.category_list_view,name="category_list"),
    path('categories/new',views.category_create_view,name="category_new"),
    path('products/new',views.product_create_view,name="product_new"),
    path('products/list',views.product_list_view,name="product_list"),
    path('products/detail/<int:pk>',views.product_detail_view,name="product_detail"),
    path('products/edit/<int:pk>',views.product_edit_view,name="product_edit"),
    path('products/delete/<int:pk>',views.product_delete_view,name="product_delete"),
]
