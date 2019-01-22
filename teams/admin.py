from django.contrib import admin

from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'division')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Team, TeamAdmin)