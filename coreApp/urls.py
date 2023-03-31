from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('about/', views.aboutPage, name='aboutPage'),
    path('user/data-queries/', views.userDataAndQueries, name='userDataAndQueries'),
    path('user/data-queries/profile/', views.userDataProfileEdit, name='userDataProfileEdit'),
    path('user/data-queries/detail/<int:pk>/', views.userDataAndQueryDetail, name='userDataAndQueryDetail'),
    path('user/data-queries/delete/<int:pk>/', views.deleteUserQuery, name='deleteUserQuery'),
    path('user/sign-up/', views.signUp, name='signUp'),
    path('user/login/', views.loginPage, name='loginPage'),
    path('user/logout/', views.logoutUser, name='logoutUser'),
    path('service/all/', views.allService, name='allService'),
    path('services/<slug:slug>/', views.allService, name='businessListByCategory'),
    path('service/<slug:slug>/', views.serviceDetail, name='serviceDetail'),
    path('service/record/<slug:slug>/', views.addQuery, name='addQuery'),
    path('user/change-password/', auth_views.PasswordChangeView.as_view(template_name='user/change-password.html', success_url = '/'), name='change_password'),
]