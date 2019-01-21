from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from leagues.models import League
from .models import Match
from markets.models import Market
from django.db.models import Q, F, Sum
from itertools import chain
import numpy as np


def index(request):
    return render(request, 'matches/index.html')

def matchLeagues(request):
    leagues = League.objects.order_by('league_name')

    paginator = Paginator(leagues, 6)
    page = request.GET.get('page')
    paged_leagues = paginator.get_page(page)

    context = {
        'leagues': leagues
    }
    return render(request, 'matches/leagues.html', context)
    

def matchLeague(request, league_slug):
    league = get_object_or_404(League, slug=league_slug)
    matches = Match.objects.order_by('date').filter(home_team__league_slug=league_slug).filter(is_played=False).filter(matchday = league.currentMatchday + 1)
    

    league = get_object_or_404(League, slug=league_slug)

    paginator = Paginator(matches, 10)
    page = request.GET.get('page')
    paged_matches = paginator.get_page(page)

    context = {
        'matches': paged_matches,
        'league': league
    }

    return render(request, 'matches/league.html', context)

def match(request, league_slug, match_slug):
    league = get_object_or_404(League, slug=league_slug)
    match = get_object_or_404(Match, slug=match_slug)
    markets = Market.objects.order_by('name')

    # filter for the teams involved
    queryset_prob = Match.objects.filter(is_played=True).filter(Q(away_team__name__icontains = match.away_team) | Q(home_team__name__icontains = match.home_team) | Q(away_team__name__icontains = match.home_team) | Q(home_team__name__icontains = match.away_team))
    if 'home' in request.GET:
        home = request.GET['home']
        away = request.GET['away']
        if home == 'home' and away == 'away':
            queryset_prob = queryset_prob.filter(Q(home_team__name__icontains = match.home_team) | Q(away_team__name__icontains = match.away_team))

        elif home == 'home' and away == 'all':
            queryset_prob = queryset_prob.filter(Q(away_team__name__icontains = match.away_team) | Q(home_team__name__icontains = match.home_team) | Q(home_team__name__icontains = match.away_team))

        elif home == 'home' and away == 'none':
            queryset_prob = queryset_prob.filter(home_team__name__icontains = match.home_team)

        elif home == 'all' and away == 'away':
            queryset_prob = queryset_prob.filter(Q(away_team__name__icontains = match.away_team) | Q(home_team__name__icontains = match.home_team) | Q(away_team__name__icontains = match.home_team))

        elif home == 'all' and away == 'all':
            queryset_prob = queryset_prob.filter(Q(away_team__name__icontains = match.away_team) | Q(home_team__name__icontains = match.home_team) | Q(away_team__name__icontains = match.home_team) | Q(home_team__name__icontains = match.away_team))

        elif home == 'all' and away == 'none':
            queryset_prob = queryset_prob.filter(Q(home_team__name__icontains = match.home_team) | Q(away_team__name__icontains = match.home_team))

        elif home == 'none' and away == 'away':
            queryset_prob = queryset_prob.filter(away_team__name__icontains = match.away_team)

        elif home == 'none' and away == 'all':
            queryset_prob = queryset_prob.filter(Q(away_team__name__icontains = match.away_team) | Q(home_team__name__icontains = match.away_team))

        elif home == 'none' and away == 'none':
            queryset_prob = queryset_prob.filter(~Q(away_team__name__icontains = match.away_team) & ~Q(home_team__name__icontains = match.home_team) & ~Q(away_team__name__icontains = match.home_team) & ~Q(home_team__name__icontains = match.away_team))

    if 'previous_games' in request.GET:
        previous_games = request.GET['previous_games']
        if previous_games == 'all':
            previous_games = league.currentMatchday
        if previous_games:
            x= int(league.currentMatchday) - int(previous_games)
            queryset_prob = queryset_prob.filter(matchday__gt= x)
    
    if 'league_position_dir' in request.GET:
        league_position = request.GET['league_position']
        league_position_dir = request.GET['league_position_dir']
        if league_position_dir == 'below':
            queryset_prob = queryset_prob.filter(Q(Q(home_team__position__gte= league_position) & Q(away_team__id = match.home_team.id)) | Q(Q(away_team__position__gte= league_position) & Q(home_team__id = match.home_team.id)) | Q(Q(home_team__position__gte= league_position) & Q(away_team__id = match.away_team.id)) | Q(Q(away_team__position__gte= league_position) & Q(home_team__id = match.away_team.id)))
        if league_position_dir == 'above':
            queryset_prob = queryset_prob.filter(Q(Q(home_team__position__lte= league_position) & Q(away_team__id = match.home_team.id)) | Q(Q(away_team__position__lte= league_position) & Q(home_team__id = match.home_team.id)) | Q(Q(home_team__position__lte= league_position) & Q(away_team__id = match.away_team.id)) | Q(Q(away_team__position__lte= league_position) & Q(home_team__id = match.away_team.id)))

    if 'half_time' in request.GET:
        if request.GET['half_time'] == 'win':
             queryset_prob = queryset_prob.filter(Q(result_fh = match.home_team) | Q(result_fh = match.away_team))
        if request.GET['half_time'] == 'draw':
            queryset_prob = queryset_prob.filter(result_fh = 'Draw')
        if request.GET['half_time'] == 'lose':
            queryset_prob = queryset_prob.filter(Q(loser_fh = match.home_team) | Q(loser_fh = match.away_team))
        if request.GET['half_time'] == 'no_goals':
            queryset_prob = queryset_prob.filter(goals_fh = 0)

    context = {
        'league': league,
        'match' : match,
        'markets' : markets,
        'values': request.GET,
        'range' : range(1, league.currentMatchday),
        'number_teams': range(1, league.count+1),
    }

    queryset_prob_result = queryset_prob
    if 'BTTS' in request.GET:
        BTTS = request.GET['BTTS']
        if BTTS =='yes':
            queryset_prob_result = queryset_prob_result.filter(Q(home_goals__gt= 0) & Q(away_goals__gt= 0))
        elif BTTS == 'no':
            queryset_prob_result = queryset_prob_result.filter(Q(home_goals= 0) | Q(away_goals= 0))
        elif BTTS =='home':
            queryset_prob_result = queryset_prob_result.filter(Q(Q(home_team__name__icontains = match.home_team) &  Q(away_goals = 0)) | Q(Q(away_team__name__icontains = match.home_team) & Q(home_goals = 0)))
        elif BTTS =='away':
            queryset_prob_result = queryset_prob_result.filter(Q(Q(home_team__name__icontains = match.away_team) &  Q(away_goals = 0)) | Q(Q(away_team__name__icontains = match.away_team) & Q(home_goals = 0)))
        elif BTTS =='home_f':
            queryset_prob_result = queryset_prob_result.filter(Q(Q(home_team__name__icontains = match.home_team) &  Q(home_goals = 0)) | Q(Q(away_team__name__icontains = match.home_team) & Q(away_goals = 0)))
        elif BTTS =='away_f':
            queryset_prob_result = queryset_prob_result.filter(Q(Q(home_team__name__icontains = match.away_team) &  Q(home_goals = 0)) | Q(Q(away_team__name__icontains = match.away_team) & Q(away_goals = 0)))

    if 'result' in request.GET:
        result = 'result'
        loser = 'loser'
        if request.GET['period'] == 'FH':
            result = 'result_fh'
            loser = 'loser_fh'
        if request.GET['period'] == 'SH':
            result = 'result_sh'
            loser = 'loser_sh'
        Qwin = Q(**{'%s' % result: match.home_team}) | Q(**{'%s' % result: match.away_team})
        Qlose = Q(**{'%s' % loser: match.home_team}) | Q(**{'%s' % loser: match.away_team})
        Qdraw = Q(**{'%s' % result: 'Draw'})
        
        if request.GET['result'] == 'win':
            queryset_prob_result = queryset_prob_result.filter(Qwin)
        if request.GET['result'] == 'lose':
            queryset_prob_result = queryset_prob_result.filter(Qlose)
        if request.GET['result'] == 'draw':
            queryset_prob_result = queryset_prob_result.filter(Qlose)
    

    if 'over_under' in request.GET:
        if request.GET['over_under'] in ('Over', 'Under'):
            if request.GET['over_under'] == 'Over':
                number_goals = int(float(request.GET['number_goals']))
                compare = 'gt'
            elif request.GET['over_under'] == 'Under':
                number_goals = number_goals = round(float(request.GET['number_goals']),1)
                compare = 'lt'
            if request.GET['period'] == 'Full':
                home_goals = Q(**{'%s' % 'home_goals__' + compare: number_goals })
                away_goals = Q(**{'%s' % 'away_goals__' + compare: number_goals})
                number_goals = Q(**{'%s' % 'goals__' + compare: number_goals})
            elif request.GET['period'] == 'FH':
                home_goals = Q(**{'%s' % 'home_goals_fh__' + compare: number_goals})
                away_goals = Q(**{'%s' % 'away_goals_fh__' + compare: number_goals})
                number_goals = Q(**{'%s' % 'goals_fh__' + compare: number_goals})
            elif request.GET['period'] == 'SH':
                home_goals = Q(**{'%s' % 'home_goals_sh__' + compare: number_goals })
                away_goals = Q(**{'%s' % 'away_goals_sh__' + compare: number_goals})
                number_goals = Q(**{'%s' % 'goals_sh__' + compare: number_goals})

            goals = request.GET['goals']
            if goals == 'Total':
                queryset_prob_result = queryset_prob_result.filter(number_goals)

            if goals == 'Score':
                queryset_prob_result_home= queryset_prob_result.filter(home_goals).filter(Q(home_team__name__icontains = match.home_team.name) | Q(home_team__name__icontains = match.away_team.name))
                queryset_prob_result_away= queryset_prob_result.filter(away_goals).filter(Q(away_team__name__icontains = match.home_team.name) | Q(away_team__name__icontains = match.away_team.name))
                queryset_prob_result = list(chain(queryset_prob_result_home, queryset_prob_result_away))

            if goals == 'Concede':
                queryset_prob_result_home= queryset_prob_result.filter(away_goals).filter(Q(home_team__name__icontains = match.home_team.name) | Q(home_team__name__icontains = match.away_team.name))
                queryset_prob_result_away= queryset_prob_result.filter(home_goals).filter(Q(away_team__name__icontains = match.home_team.name) | Q(away_team__name__icontains = match.away_team.name))
                queryset_prob_result = list(chain(queryset_prob_result_home, queryset_prob_result_away))

    if request.GET:
        games = queryset_prob.count()
        results = len(queryset_prob_result)

        if games ==0:
            prob = 1
        else:
            prob = int(results)/int(games)
        context['games'] = games
        context['prob'] = prob
        queryset_prob_result = list(chain(queryset_prob_result))
        queryset_prob_result.sort(key = lambda match: match.date, reverse = True)
        context['matches'] = queryset_prob_result
        queryset_prob = list(chain(queryset_prob))
        queryset_prob.sort(key = lambda match: match.date, reverse = True)
        criteria_not = [obj for obj in queryset_prob if obj not in queryset_prob_result]
        context['matches_not'] = criteria_not

    return render(request, 'matches/match.html', context)

def matchSearch(request):
    leagues = League.objects.order_by('league_name')
    queryset_match = Match.objects.order_by('-list_date').filter(is_played=False)
    
    # Teams
    if 'team' in request.GET:
        team = request.GET['team']
        if team:
            queryset_match = queryset_match.filter(home_team__name__icontains = team)
        
    # League
    if 'league' in request.GET:
        league = request.GET['league']
        if league:
            queryset_match = queryset_match.filter(home_team__division__league_name__iexact = league)

    # Date 
    if 'date' in request.GET:
        date = request.GET['date']
        if date:
            queryset_match = queryset_match.filter(date = date)

    context = {
        'matches': queryset_match,
        'leagues': leagues,
        'values': request.GET
    }

    return render(request, 'matches/search.html', context)


