from django.db import models

class Market(models.Model):
     name = models.CharField(max_length=250)

     def __str__(self):
        output = self.name
        return output
