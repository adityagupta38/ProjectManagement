from django.db import models
from django.contrib.auth.models import User


class Clients(models.Model):
    client_name = models.CharField(max_length=155, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=80)

    
class Projects(models.Model):
    name = models.CharField(max_length=160, unique=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='project', editable=False)
    users = models.ManyToManyField(User, editable=False, related_name='projects')
    updated_on = models.DateTimeField(auto_now_add=True)
