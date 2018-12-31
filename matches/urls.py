from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='matches'),
    path('leagues', views.matchLeagues, name='matchLeagues'),
    path('leagues/<int:league_id>', views.matchLeague, name='matchLeague'),
    path('leagues/<int:league_id>/<int:match_id>', views.match, name='match'),
    path('search', views.matchSearch, name='matchSearch'),
]
