from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null = True , blank = True)
    title = models.CharField(max_length = 200)
    completed = models.BooleanField(default = False)
    
    due_date = models.DateField(null=True , blank=True)
    
    def __str__(self):
        return self.title

