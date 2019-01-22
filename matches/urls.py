from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='matches'),
    path('leagues', views.matchLeagues, name='matchLeagues'),
    path('leagues/<str:league_slug>', views.matchLeague, name='matchLeague'),
    path('leagues/<str:league_slug>/<str:match_slug>', views.match, name='match'),
    path('search', views.matchSearch, name='matchSearch'),
]
