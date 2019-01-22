from django.urls import path
from .views import Teams

urlpatterns = [
    path('', Teams.index, name='teams'),
    path('leagues', Teams.teamLeagues, name='teamLeagues'),
    path('leagues/<str:league_slug>', Teams.teamLeague, name='teamLeague'),
    path('leagues/<str:league_slug>/<str:team_slug>', Teams.team, name='team'),
    path('search', Teams.search, name='search'),
]

