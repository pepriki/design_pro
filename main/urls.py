from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('requests/my/', views.my_requests, name='my_requests'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<int:request_id>/delete/', views.delete_request, name='delete_request'),
]
