from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

class Machine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """RF_1 (CU_01b) -  Ejercicio ligado a una máquina."""
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Routine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=20, unique=True)
    series_multiplier = models.FloatField()
    reps_multiplier = models.FloatField()

    def __str__(self):
        return self.name


class Goal_Routine(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.goal.name} - {self.routine.name}"


class Routine_Exercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    series = models.IntegerField()
    reps = models.IntegerField()
    load = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.exercise.name} - {self.series}x{self.reps}"

class User_Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    time = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.routine.name} ({self.level.name})"

class User_Area_Level(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.area.name} ({self.level.name})"