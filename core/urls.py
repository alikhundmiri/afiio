"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from accounts.views import (edit_bio, new_bio, first_last_name, change_password)

app_name = 'core'

urlpatterns = [
    path('', views.index , name='index'),

    path('@<str:username>/', include([


        path('', views.user_profile, name='user_profile'),
        path('generated/card/', views.card, name='card'),
        # path('generated/card/new', views.new_card, name='new_card'),

        # path to redirect!
        path('stats/', views.stats, name='stats'),
        path('superuser/', views.super_user, name='super_user'),

        path('new_bio/', new_bio, name='new_bio'),
        path('edit_bio/', edit_bio, name='edit_bio'),
        path('user_info/', first_last_name, name='first_last_name'),
        path('new/', views.create_product, name='create_product'),
        path('new_category/', views.create_category, name='create_category'),
         
        path('limit_reach/', views.limit_reach, name='limit_reach'),
        path('password/', change_password, name='change_password'),
        path('edit_category/<slug:slug>/', views.edit_category, name='edit_category'),
        path('edit/<slug:slug>/', views.edit_product, name='edit_product'),

        path('<slug:slug>/', views.redirect_link, name='redirect_link'),

    ])),

]