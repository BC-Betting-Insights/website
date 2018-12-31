from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='teams'),
    path('leagues', views.teamLeagues, name='teamLeagues'),
    path('leagues/<int:league_id>', views.teamLeague, name='teamLeague'),
    path('leagues/<int:league_id>/<int:team_id>', views.team, name='team'),
    path('search', views.search, name='search'),
]

