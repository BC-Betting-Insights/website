from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from leagues.models import League
from .models import Match


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
    print(league.currentMatchday)
    matches = Match.objects.order_by('date').filter(home_team__league_slug=league_slug).filter(is_played=False).filter(matchday = league.currentMatchday + 1)
    

    league = get_object_or_404(League, slug=league_slug)

    paginator = Paginator(matches, 6)
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

    context = {
        'league': league,
        'match' : match
    }
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
            queryset_match = queryset_match.filter(date = date )

    context = {
        'matches': queryset_match,
        'leagues': leagues,
        'values': request.GET
    }

    return render(request, 'matches/search.html', context)


