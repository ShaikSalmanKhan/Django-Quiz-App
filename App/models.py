from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    manager         =  models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    trivia_api_link =  models.URLField(max_length=200,blank=True)
    score           =  models.IntegerField()
    time_taken      =  models.CharField(max_length=20)
    user_answers    =  models.TextField()
    created_date    =  models.DateTimeField(auto_now_add=True)

    def result(self):
        if self.score >= 7:
            return "Win"
        else:
            return "Lose"
