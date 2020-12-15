from django.urls import path
from . import views

app_name = 'djgapp'

urlpatterns = [
    path('', views.homepage),
    path('index/', views.indexpage, name='index-page'),
    path('home/', views.homepage, name='home-page'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.logout_user, name='logout-page'),
    path('create-customer/', views.create_customer_page, name='create-customer-page'),
    path('create-order/', views.create_order_page, name='create-order-page'),
    path('update-order/<str:pk>/', views.update_order, name='update-order'),
    path('delete-order/<str:pk>/', views.delete_order, name='delete-order'),
    path('register/', views.register, name='register-page')
]