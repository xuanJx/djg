from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'djgapp'

urlpatterns = [
    path('', TemplateView.as_view(template_name='djgapp/home.html')),
    path('index/', views.indexpage, name='index-page'),
    path('home/', TemplateView.as_view(template_name='djgapp/home.html'), name='home-page'),
    path('about/', views.Aboutpage.as_view(), name='about-page'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.logout_user, name='logout-page'),
    path('create-customer/', views.create_customer_page, name='create-customer-page'),
    path('create-order/', views.create_order_page, name='create-order-page'),
    path('update-order/<str:pk>/', views.update_order, name='update-order'),
    path('delete-order/<str:pk>/', views.delete_order, name='delete-order'),
    path('register/', views.register, name='register-page')
]