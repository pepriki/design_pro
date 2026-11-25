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
    path('superadmin/', views.admin_panel, name='admin_panel'),
    path('superadmin/requests/<int:request_id>/', views.update_request, name='update_request'),
    path('superadmin/categories/add/', views.add_category, name='add_category'),
    path('superadmin/categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
]
