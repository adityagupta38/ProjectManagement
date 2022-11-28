"""ProjectManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authviews
from proj import views
from rest_framework import routers
from proj import apiviews

from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register('clients', apiviews.ClientsApi, basename='clients')
router.register('projects', apiviews.ProjectsApi, basename='projects')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authviews.LoginView.as_view(next_page='/userhome/', template_name='user_login.html'), name='user_login'),
    path('', include(router.urls)),
    path('api_auth/', include('rest_framework.urls')),
    path('usersignup', views.user_signup, name='user_signup'),
    path('userlogout/', authviews.LogoutView.as_view(next_page='/'), name='user_logout'),
    path('userhome/', views.user_home, name='user_home'),
    path('registerclient/', views.register_client, name='register_client'),
    path('updateclient<int:pk>', views.update_client, name='update_client'),
    path('deleteclient<int:pk>', views.delete_client, name='delete_client'),
    path('addproject', views.add_project, name='add_project'),
    path('assignusers', views.assign_users, name='assign_users'),
    path('userprojects', views.user_projects, name='user_projects'),
]





urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)