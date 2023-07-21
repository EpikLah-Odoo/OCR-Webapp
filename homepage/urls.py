from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'homepage'

urlpatterns = [    
    path('', views.index, name='index'),
    path('custom_invoices', views.homepage, name='homepage'),
    path('sftp/', views.sftp_view, name='sftp'),    
    path('validation/', views.validation, name='validation'),  
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logged_out/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
    path('general_invoices/', views.homepage_invoices, name='homepage_invoices'),
    path('sftp_invoices/', views.sftp_invoices, name='sftp_invoices'),    
    path('validation_invoices/', views.validation_invoices, name='validation_invoices'),  
]