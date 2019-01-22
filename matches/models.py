from django.db import models
from django.db.models import Q, F
from datetime import datetime
from django.template.defaultfilters import slugify


class Match(models.Model):
    home_team = models.ForeignKey('teams.Team', related_name='home_team', on_delete=models.DO_NOTHING)
    away_team = models.ForeignKey('teams.Team', related_name='away_team', on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.TimeField(default = '15:00:00')
    home_goals = models.IntegerField(null=True)
    away_goals = models.IntegerField(null=True)
    home_goals_fh = models.IntegerField(null=True)
    away_goals_fh = models.IntegerField(null=True)
    home_goals_sh = models.IntegerField(null=True)
    away_goals_sh = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    goals_fh = models.IntegerField(null=True)
    goals_sh = models.IntegerField(null=True)
    result_fh = models.CharField(max_length=200, null=True)
    result_sh = models.CharField(max_length=200, null=True)
    result = models.CharField(max_length=200, null=True)
    loser = models.CharField(max_length=200, null=True)
    loser_fh = models.CharField(max_length=200, null=True)
    loser_sh = models.CharField(max_length=200, null=True)
    home_possession = models.IntegerField()
    home_shots_target = models.IntegerField()
    away_shots_target = models.IntegerField()
    is_played = models.BooleanField(default=True)
    list_date = models.DateTimeField(default = datetime.now)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    
    slug = models.SlugField(max_length=200)
    league_slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title())
            self.league_slug = slugify(self.home_team.division.league_name)
        self.home_goals_sh = int(self.home_goals or 0) - int(self.home_goals_fh or 0)
        self.away_goals_sh = int(self.away_goals or 0) - int(self.away_goals_fh or 0)
        self.goals = int(self.home_goals or 0) + int(self.away_goals or 0)
        self.goals_fh = int(self.home_goals_fh or 0) + int(self.away_goals_fh or 0)
        self.goals_sh = int(self.home_goals_sh or 0) + int(self.away_goals_sh or 0)
        if int(self.home_goals_fh or 0) > int(self.away_goals_fh or 0):
            self.result_fh = self.home_team.name
            self.loser_fh = self.away_team.name
        elif int(self.home_goals_fh or 0) < int(self.away_goals_fh or 0):
            self.result_fh = self.away_team.name
            self.loser_fh = self.home_team.name
        else:
            self.result_fh = 'Draw'
            self.loser_fh = 'Draw'

        if int(self.home_goals_sh or 0) > int(self.away_goals_sh or 0):
            self.result_sh = self.home_team.name
            self.loser_sh = self.away_team.name
        elif int(self.home_goals_sh or 0) < int(self.away_goals_sh or 0):
            self.result_sh = self.away_team.name
            self.loser_sh = self.home_team.name
        else:
            self.result_sh = 'Draw'
            self.loser_sh = 'Draw'
        
        if int(self.home_goals or 0) > int(self.away_goals or 0):
            self.result = self.home_team.name
            self.loser = self.away_team.name
        elif int(self.home_goals or 0) < int(self.away_goals or 0):
            self.result = self.away_team.name
            self.loser = self.home_team.name
        else:
            self.result = 'Draw'
            self.result = 'Draw'
        super(Match, self).save(*args, **kwargs)

    def slugif(self):
        title = self.title()
        slug = self.slug = slugify(title)
        self.save()
        return slug
    
    def home_goals_second_half(self):
        home_goals =  self.home_goals - self.home_goals_fh
        self.home_goals_sh = home_goals  
        self.save()
        return home_goals

    def away_goals_second_half(self):
        away_goals =  self.away_goals - self.away_goals_fh
        self.away_goals_sh = away_goals
        self.save()
        return away_goals

    def away_possession(self):
        away_posession = 100-self.home_possession
        return away_posession

    def title(self):
        output = self.home_team.name + ' v ' + self.away_team.name
        return output

    def first_half_score(self):
        output = str(self.home_goals_first_half) + ' - ' + str(self.away_goals_first_half)
        return output

    def score(self):
        output = str(self.home_goals) + ' - ' + str(self.away_goals)
        return output

    def first_half_goals(self):
        if self.home_goals_first_half != None:
            output = self.home_goals_first_half + self.away_goals_first_half
            return output
    
    def second_half_goals(self):
        if self.first_half_goals() != None:
            fhg = self.first_half_goals()
            output = self.home_goals + self.away_goals  - fhg
            shg = models.IntegerField()
            return output

    def played(self):
        if self.date <= datetime.now:
            self.is_played = True
        else: 
           self.is_played = False
    
    def home_team_games(self):
        count = Match.objects.filter(Q(home_team = self.home_team, is_played=True ) | Q(away_team = self.home_team, is_played=True )).count()
        return count
    
    def away_team_games(self):
        count = Match.objects.filter(Q(home_team = self.away_team, is_played = True ) | Q(away_team = self.away_team, is_played=True )).count()
        return count

    def prob_goal_fh_home(self):
        count = Match.objects.filter(is_played = True, home_goals_fh__gt=0, home_team = self.home_team).count()
        games = Match.objects.filter(home_team = self.home_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_fh_away(self):
        count = Match.objects.filter(is_played = True, away_goals_fh__gt=0, away_team = self.away_team).count()
        games = Match.objects.filter(away_team = self.away_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_sh_home(self):
        count = Match.objects.filter(is_played = True, home_goals__gt=F('home_goals_fh'), home_team = self.home_team).count()
        games = Match.objects.filter(home_team = self.home_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_sh_away(self):
        count = Match.objects.filter(is_played = True, away_goals__gt=F('away_goals_fh'), away_team = self.away_team).count()
        games = Match.objects.filter(away_team = self.away_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'
    
    def __hash__(self):
        return hash((self.home_team, self.away_team))

    def __eq__(self, other):
        return self.home_team == other.home_team and self.away_team == other.away_team

    def __str__(self):
        output = self.home_team.name + ' v ' + self.away_team.name
        return output
