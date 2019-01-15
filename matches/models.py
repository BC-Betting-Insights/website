from django.db import models
from django.db.models import Q, F
from datetime import datetime


class Match(models.Model):
    home_team = models.ForeignKey('teams.Team', related_name='home_team', on_delete=models.DO_NOTHING)
    away_team = models.ForeignKey('teams.Team', related_name='away_team', on_delete=models.DO_NOTHING)
    date = models.DateField()
    time = models.TimeField(default = '15:00:00')
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    home_goals_first_half = models.IntegerField()
    away_goals_first_half = models.IntegerField()
    home_possession = models.IntegerField()
    home_shots_target = models.IntegerField()
    away_shots_target = models.IntegerField()
    is_played = models.BooleanField(default=True)
    list_date = models.DateTimeField(default = datetime.now)

    def slug(self):
        slug = self.title.replace(" ", "-")
        return slug

    def away_possession(self):
        away_posession = 100-self.home_possession
        return away_posession
    
    def home_goals_second_half(self):
        home_goals_second_half = self.home_goals - self.home_goals_first_half
        return home_goals_second_half

    def away_goals_second_half(self):
        away_goals_second_half = self.away_goals = self.away_goals_first_half
        return away_goals_second_half

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
        output = self.home_goals_first_half + self.away_goals_first_half
        return output
    
    def second_half_goals(self):
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
        count = Match.objects.filter(is_played = True, home_goals_first_half__gt=0, home_team = self.home_team).count()
        games = Match.objects.filter(home_team = self.home_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_fh_away(self):
        count = Match.objects.filter(is_played = True, away_goals_first_half__gt=0, away_team = self.away_team).count()
        games = Match.objects.filter(away_team = self.away_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_sh_home(self):
        count = Match.objects.filter(is_played = True, home_goals__gt=F('home_goals_first_half'), home_team = self.home_team).count()
        games = Match.objects.filter(home_team = self.home_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def prob_goal_sh_away(self):
        count = Match.objects.filter(is_played = True, away_goals__gt=F('away_goals_first_half'), away_team = self.away_team).count()
        games = Match.objects.filter(away_team = self.away_team, is_played = True).count()
        if games > 0:
            prob = int(count)/games
            return prob
        else:
            return 'N/A'

    def __str__(self):
        output = self.home_team.name + ' v ' + self.away_team.name
        return output
