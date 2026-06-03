from django.db import models


class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.name


class UserProfile(models.Model):  # Evitamos llamarla 'User' para no chocar con el sistema de Django
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    weight = models.FloatField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
