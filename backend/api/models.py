from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Player(models.Model):
    nick = models.CharField(max_length=50)
    name = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    team = models.CharField(max_length=50, null=True, blank=True)
    teamid = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    dpi = models.IntegerField(null=True, blank=True)
    m_freq = models.CharField(max_length=50, null=True, blank=True)
    m_sens_game = models.CharField(max_length=50, null=True, blank=True)
    m_sens_zoom = models.CharField(max_length=50, null=True, blank=True)
    m_sens_windows = models.CharField(max_length=50, null=True, blank=True)
    m_acceleration = models.CharField(max_length=50, null=True, blank=True)
    m_rawinput = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)
    aspect_ratio = models.CharField(max_length=50, null=True, blank=True)
    image_format = models.CharField(max_length=50, null=True, blank=True)
    refresh_rate = models.CharField(max_length=50, null=True, blank=True)
    sharecode = models.CharField(max_length=100, null=True, blank=True)
    cfg = models.CharField(max_length=100, null=True, blank=True)
    commands = models.TextField(null=True, blank=True)
    steam = models.CharField(max_length=300, null=True, blank=True)
    twitch = models.CharField(max_length=300, null=True, blank=True)
    twitter = models.CharField(max_length=300, null=True, blank=True)
    instagram = models.CharField(max_length=300, null=True, blank=True)
    youtube = models.CharField(max_length=300, null=True, blank=True)
    facebook = models.CharField(max_length=300, null=True, blank=True)
    vk = models.CharField(max_length=300, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)




