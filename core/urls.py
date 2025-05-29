"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.urls import path, include
from sales import  views
from  oauth2login import views as authviews

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('django.contrib.auth.urls')),
    path('', include('sales.urls')),
    path('api/', include('sales.urls')),#for graphql
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.profile, name='profile'),

    path('oauth2', authviews.home, name='oauth2' ),
    path('oauth2/user', authviews.get_authenticated_user, name='get_authenticated_user'),
    path('oauth2/login', authviews.discord_login, name='discord_login'),
    path('oauth2/login/redirect', authviews.discord_login_redirect, name='discord_login_redirect'),
    #path('oauth2/login/redirect', authviews.discord_login_redirect, name='discord_login_redirect_sql')

]
