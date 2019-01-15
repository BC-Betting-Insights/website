from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='teams'),
    path('leagues', views.teamLeagues, name='teamLeagues'),
    path('leagues/<str:league_slug>', views.teamLeague, name='teamLeague'),
    path('leagues/<str:league_slug>/<str:team_slug>', views.team, name='team'),
    path('search', views.search, name='search'),
]

