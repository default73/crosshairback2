import os

from django.http import HttpResponseNotFound, FileResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer
from django.conf import settings
import glob


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer




class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


def download_photo_team(request, folder_name):
    # Получаем имя файла и путь до него
    filename = 'image.png'
    path = os.path.join(settings.BASE_DIR, 'teams', folder_name, filename)

    # Ищем файл по указанному пути
    try:
        file_path = glob.glob(path)[0]
    except IndexError:
        # Если файл не найден, возвращаем ошибку 404
        return HttpResponseNotFound('File not found')

    # Открываем файл и возвращаем его как ответ
    f = open(file_path, 'rb')
    response = FileResponse(f)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


def download_photo_player(request, folder_name):
    # Получаем имя файла и путь до него
    filename = 'image.png'
    path = os.path.join(settings.BASE_DIR, 'CSGOSettings', folder_name, filename)

    # Ищем файл по указанному пути
    try:
        file_path = glob.glob(path)[0]
    except IndexError:
        # Если файл не найден, возвращаем ошибку 404
        return HttpResponseNotFound('File not found')

    # Открываем файл и возвращаем его как ответ
    f = open(file_path, 'rb')
    response = FileResponse(f)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


def download_cfg_player(request, folder_name):
    # Получаем имя файла и путь до него
    filename = 'config.cfg'
    path = os.path.join(settings.BASE_DIR, 'CSGOSettings', folder_name, filename)

    # Ищем файл по указанному пути
    try:
        file_path = glob.glob(path)[0]
    except IndexError:
        # Если файл не найден, возвращаем ошибку 404
        return HttpResponseNotFound('File not found')

    # Открываем файл и возвращаем его как ответ
    f = open(file_path, 'rb')
    response = FileResponse(f)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response