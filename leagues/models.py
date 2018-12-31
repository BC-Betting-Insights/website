from django.db import models

class League(models.Model):
    league_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.league_name
