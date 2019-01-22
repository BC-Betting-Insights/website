from django.contrib import admin

from .models import Match

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'date')
    list_display_links = ('id', 'home_team', 'away_team')
    list_filter = ('home_team', 'away_team',)
    list_editable = ('date',)
    search_fields = ('date',)
    list_per_page = 25
admin.site.register(Match, MatchAdmin)

