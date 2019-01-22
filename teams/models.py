from django.db import models
from django.db.models import Q, F, Sum
from leagues.models import League
from matches.models import Match
from django.template.defaultfilters import slugify
from datetime import datetime
# from django.apps import apps
# Matches = apps.get_model('app1', 'Matches')

class Team(models.Model):
    name = models.CharField(max_length=200)
    division = models.ForeignKey(League, related_name='league', on_delete=models.DO_NOTHING)
    slug = models.SlugField()
    league_slug = models.SlugField()
    position = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
            self.league_slug = slugify(self.division.league_name)
        super(Team, self).save(*args, **kwargs)

    def games(self):
        games = self.home_games() + self.away_games()
        return games

    def home_games(self):
        count_home = Match.objects.filter(home_team = self.id, is_played = True).count()
        return count_home

    def away_games(self):
        count_away = Match.objects.filter(away_team = self.id, is_played = True).count()
        return count_away
    
    def goals_for(self):
        goals_scored = self.home_goals_for() + self.away_goals_for()
        return goals_scored

    def home_goals_for(self):
        sum_home = Match.objects.filter(home_team = self.id, is_played = True).aggregate(Sum('home_goals'))
        return int(sum_home['home_goals__sum'] or 0)

    def away_goals_for(self):
        sum_away = Match.objects.filter(away_team = self.id, is_played = True).aggregate(Sum('away_goals'))
        return int(sum_away['away_goals__sum'] or 0)

    def goals_for_per_game(self):
        if self.games() > 0:
            goals_pg = (self.goals_for()) / (self.games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def home_goals_for_per_game(self):
        if self.home_games() > 0:
            goals_pg = (self.home_goals_for()) / (self.home_games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def away_goals_for_per_game(self):
        if self.away_games() > 0:
            goals_pg = (self.away_goals_for()) / (self.away_games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def goals_against(self):
        goals_against = self.home_goals_against() + self.away_goals_against()
        return goals_against

    def home_goals_against(self):
        sum_home = Match.objects.filter(home_team = self.id, is_played = True).aggregate(Sum('away_goals'))
        return int(sum_home['away_goals__sum'] or 0)
        
    def away_goals_against(self):
        sum_away = Match.objects.filter(away_team = self.id, is_played = True).aggregate(Sum('home_goals'))
        return int(sum_away['home_goals__sum'] or 0)

    def goals_against_per_game(self):
        if self.games() > 0:
            goals_pg = (self.goals_against()) / (self.games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def home_goals_against_per_game(self):
        if self.home_games() > 0:
            goals_pg = (self.home_goals_against()) / (self.home_games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def away_goals_against_per_game(self):
        if self.away_games() > 0:
            goals_pg = (self.away_goals_against()) / (self.away_games())
            return round(goals_pg,2)
        else:
            return 'N/A'

    def clean_sheets(self):
        output = self.home_clean_sheets() + self.away_clean_sheets()
        return output

    def home_clean_sheets(self):
        count = Match.objects.filter(home_team = self.id, is_played = True, away_goals=0).count()
        return count

    def away_clean_sheets(self):
        count = Match.objects.filter(away_team = self.id, is_played = True, home_goals=0).count()
        return count
    
    def __str__(self):
        return self.name
