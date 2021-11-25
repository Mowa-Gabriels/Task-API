
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False, blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE, default = 1)
 

    def __str__(self):
        return self.title

