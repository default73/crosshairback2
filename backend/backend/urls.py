"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from api.views import PlayerList, PlayerDetail, TeamDetail, TeamList, download_photo_team, download_photo_player, download_cfg_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/', PlayerList.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),
    path('teams/', TeamList.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    path('teamlogo/<str:folder_name>/', download_photo_team, name='download_photo_team'),
    path('playerlogo/<str:folder_name>/', download_photo_player, name='download_photo_player'),
    path('playercfg/<str:folder_name>/', download_cfg_player, name='download_cfg_player'),
]
