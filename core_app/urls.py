from django.contrib import admin
from django.urls import path, include
from core_app import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('create/', views.create_post_view, name='create_post_view'),
    path('update/<int:pk>', views.update_post_view, name='update_post_view'),
    path('delete/<int:pk>', views.delete_post_view, name='delete_post_view'),
    path('editprofile/', views.edit_profile_view, name='edit_profile_view'),
]