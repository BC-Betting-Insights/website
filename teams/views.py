from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from urllib.parse import urlparse
from datetime import datetime
from dateutil.parser import parse

from .models import Team
from leagues.models import League
from matches.models import Match
from django.db.models import Q, F, Sum
from django.template.defaultfilters import slugify


import http.client
import json


def index(request):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '1f39c6d5a29947f282f44dfd0aa460f5' }
    connection.request('GET', '/v2/competitions', None, headers)
    response = json.loads(connection.getresponse().read().decode())

    for x in response['competitions']:
        if (x['plan'] == 'TIER_ONE' and x['id'] not in [2000, 2001]):
            connection.request('GET', '/v2/competitions/' + x['code'] + '/matches', None, headers)
            matches= json.loads(connection.getresponse().read().decode())
            for i in matches['matches']:
                played = False
                if i['status'] == 'FINISHED':
                    played = True
                output = Match(id= i['id'], date = parse(i['utcDate']).date(), home_goals =i['score']['fullTime']['homeTeam'], away_goals =i['score']['fullTime']['awayTeam'], home_goals_fh =i['score']['halfTime']['homeTeam'], away_goals_fh=i['score']['halfTime']['awayTeam'], home_possession = 50, home_shots_target =0, away_shots_target = 0, is_played = played, away_team_id = i['awayTeam']['id'], home_team_id = i['homeTeam']['id'], time = parse(i['utcDate']).time(), league_slug = slugify(matches['competition']['name']), slug=slugify(i['homeTeam']['name'] + 'v' + i['awayTeam']['name']), matchday = i['matchday'] )
                output.save()



    context = {
        'response' : response,
        # 'teams' : teams
    }

    return render(request, 'teams/index.html', context)

def teamLeagues(request):
    
    leagues = League.objects.order_by('league_name')

    paginator = Paginator(leagues, 6)
    page = request.GET.get('page')
    paged_leagues = paginator.get_page(page)

    context = {
        'leagues': leagues
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
    matches = Match.objects.order_by('-date').filter(Q(home_team__slug = team_slug) | Q(away_team__slug = team_slug)).filter(is_played=True)
    league = get_object_or_404(League, slug=league_slug)
    context = {
        'team': team,
        'matches': matches,
        'league': league
    }
    return render(request, 'teams/team.html', context)

def search(request):
    return render(request, 'teams/search.html')


