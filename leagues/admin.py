from django.contrib import admin

from .models import League

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'league_name', 'country')
    list_display_links = ('id', 'league_name', 'country')
    list_filter = ('id', 'league_name', 'country')
    list_per_page = 25
admin.site.register(League, LeagueAdmin)