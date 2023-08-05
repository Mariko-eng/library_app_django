from django.urls import path
from . import views 

app_name = 'main'

urlpatterns = [
    path('home',views.index, name="home"),
    path('categories/list',views.category_list_view,name="category_list"),
    path('categories/new',views.category_create_view,name="category_new"),
    path('products/list',views.product_list_view,name="product_list"),
    path('products/new',views.product_create_view,name="product_new"),
]
