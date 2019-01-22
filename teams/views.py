from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from urllib.parse import urlparse

from .models import Team
from leagues.models import League
from matches.models import Match
from django.db.models import Q, F, Sum

import http.client
import json


def index(request):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '1f39c6d5a29947f282f44dfd0aa460f5' }
    connection.request('GET', '/v2/competitions/PL/matches/?matchday=22', None, headers )
    response = json.loads(connection.getresponse().read().decode())

    context = {
        'response': response
    }
    # print (response)

    return render(request, 'teams/index.html', context)

def teamLeagues(request):
    
    leagues = League.objects.order_by('league_name')

    paginator = Paginator(leagues, 6)
    page = request.GET.get('page')
    paged_leagues = paginator.get_page(page)

    context = {
        'leagues': paged_leagues
    }
    return render(request, 'teams/leagues.html', context)

def teamLeague(request, league_slug):
    teams = Team.objects.order_by('name').filter(league_slug=league_slug)
    league = get_object_or_404(League, slug=league_slug)
    context = {
        'teams': teams,
        'league': league
    }
    return render(request, 'teams/league.html', context)

def team(request, league_slug, team_slug):
    team = get_object_or_404(Team, slug=team_slug)
    matches = Match.objects.order_by('date').filter(Q(home_team__slug = team_slug) | Q(away_team__slug = team_slug))
    league = get_object_or_404(League, slug=league_slug)
    context = {
        'team': team,
        'matches': matches,
        'league': league
    }
    return render(request, 'teams/team.html', context)

def search(request):
    return render(request, 'teams/search.html')


