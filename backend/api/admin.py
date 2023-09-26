from django.contrib import admin

# Register your models here.
from .models import Team, Player

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass