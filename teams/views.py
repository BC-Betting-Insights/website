from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from urllib.parse import urlparse

from .models import Team
from leagues.models import League
from matches.models import Match
from django.db.models import Q, F, Sum


def index(request):
    return render(request, 'teams/index.html')

def teamLeagues(request):
    
    leagues = League.objects.order_by('league_name')

    paginator = Paginator(leagues, 6)
    page = request.GET.get('page')
    paged_leagues = paginator.get_page(page)

    context = {
        'leagues': paged_leagues
    }
    return render(request, 'teams/leagues.html', context)

def teamLeague(request, league_id):
    teams = Team.objects.order_by('name').filter(division=league_id)
    league = get_object_or_404(League, id=league_id)
    context = {
        'teams': teams,
        'league': league
    }
    return render(request, 'teams/league.html', context)

def team(request, league_id, team_id):
    team = get_object_or_404(Team, id=team_id)
    matches = Match.objects.order_by('date').filter(Q(home_team = team_id) | Q(away_team = team_id))
    league = get_object_or_404(League, id=league_id)
    context = {
        'team': team,
        'matches': matches,
        'league': league
    }
    return render(request, 'teams/team.html', context)

def search(request):
    return render(request, 'teams/search.html')


