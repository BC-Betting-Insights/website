from django.db import models
from django.template.defaultfilters import slugify

class League(models.Model):
    league_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    slug = models.SlugField()
    currentMatchday = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.league_name)
        super(League, self).save(*args, **kwargs)

    def slugif(self):
        title = self.league_name
        slug = self.slug = slugify(title)
        self.save()
        return slug

    def __str__(self):
        return self.league_name
