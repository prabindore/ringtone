from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path
from shuffle import views


urlpatterns = [
    # Auth
    path('login/', views.login_view, name='admin_login'),
    path('logout/', LogoutView.as_view(next_page='admin_login'), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    # Categories
    path('ringtone_lan/', views.ringtone_lan,name='ringtone_lan_list'),
    path('ringtone_lan/create', views.ringtone_lan_create,name='ringtone_lan_create'),
    path('ringtone_lan/<int:id>/edit/', views.ringtone_lan_edit, name='ringtone_lan_edit'),
    path('ringtone_lan/<int:id>/delete/', views.ringtone_lan_delete, name='categories_delete'),
    path('ringtone_lan/<int:id>/update_status/', views.update_status, name='update_status'),

    # Ringtone 
    path('ringtones/', views.ringtones, name='ringtones_list'),
    path('ringtones/create/', views.create_ringtone, name='ringtones_create'),
    path('ringtones/<int:id>/edit/', views.ringtones_edit, name='ringtones_edit'),
    path('ringtones/<int:id>/delete/', views.ringtones_delete, name='ringtones_delete'),
    path('get-cities/', views.get_cities_by_state, name='get_cities_by_state'),
    path('ringtones/<int:id>/update_status/', views.ringtone_update_status, name='ringtone_update_status'),


    # Notification 
    path('notification/create/', views.notification_create, name='notification_create'),



    # Users 
    path('users/', views.users, name='users_list'),
    path('users/create/', views.create_users, name='users_create'),
    path('users/<int:id>/edit/', views.users_edit, name='users_edit'),
    path('users/<int:id>/delete/', views.users_delete, name='users_delete'),


    # Users 
    path('admins/', views.admins, name='admins_list'),
    path('admins/create/', views.admins_create, name='admins_create'),
    path('admins/<int:id>/edit/', views.admins_edit, name='admins_edit'),
    # path('admins/<int:id>/delete/', views.admins_delete, name='admins_delete'),
]