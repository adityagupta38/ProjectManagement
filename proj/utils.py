import django
django.setup()
from django.contrib.auth.models import User
from proj.models import Clients, Projects

def is_user_registered(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False


def is_client_registered(name):
    try:
        Clients.objects.get(client_name=name)
        return True
    except:
        return False


def is_project_added(proj):
    try:
        Projects.objects.get(name=proj)
        return True
    except:
        return False