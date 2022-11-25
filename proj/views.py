import django
django.setup()
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from proj.forms import UserSignupForm, ClientRegisterForm, ProjectForm, AssignProjectForm
from django.contrib import messages
from proj.utils import is_user_registered, is_client_registered, is_project_added
from django.contrib.auth.decorators import login_required
from proj.models import Clients, Projects
from django.db.models import ObjectDoesNotExist


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not is_user_registered(username=username):
            userform = UserSignupForm(request.POST)
            if userform.is_valid():
                password = userform.cleaned_data.get('password')
                user = userform.save(commit=False)
                user.set_password(password)
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Signup Successfull Log In To Continue')
                return redirect('/')
            error = userform.errors
            userform = UserSignupForm()
            return render(request, 'user_registration.html', {'form': userform, 'errors': error})
        error = 'Username is already Registered Pls try different Username'
        userform = UserSignupForm()
        return render(request, 'user_registration.html', {'form': userform, 'msg': error})
    userform = UserSignupForm()
    return render(request, 'user_registration.html', {'form': userform})


@login_required(login_url='/')
def user_home(request):
    clients = Clients.objects.all()
    return render(request, 'user_home.html', {'clients': clients})

@login_required(login_url='/')
def register_client(request):
    if request.method == 'POST':
        if not is_client_registered(request.POST['client_name']):
            form = ClientRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/userhome')
            return render(request, 'client_register_page.html', {'form': form, 'errors': form.errors})
        return render(request, 'client_register_page.html', {'form': ClientRegisterForm(request.POST), 'dberror': 'Client name already exist'})
    form = ClientRegisterForm()
    return render(request, 'client_register_page.html', {'form': form})

@login_required(login_url='/')
def update_client(request, pk):
    client = Clients.objects.get(id=pk)
    if request.method == 'POST':       
        form = ClientRegisterForm(data=request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('/userhome')
        return render(request, 'client_update.html', {'form': form, 'errors': form.errors})
    form = ClientRegisterForm(instance=client)
    return render(request, 'client_update.html', {'form': form})

@login_required(login_url='/')
def delete_client(request, pk):
    if request.method == 'POST':
        client = Clients.objects.get(id=pk)
        client.delete()
        return redirect('/userhome')
    return render(request, 'confirm_delete_client.html')

@login_required(login_url='/')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if not is_project_added(request.POST['name']):
            if form.is_valid():
                client_obj = Clients.objects.get(client_name=request.POST['client'])
                proj = form.save(commit=False)
                proj.client = client_obj
                proj.save()
                messages.add_message(request, messages.SUCCESS, 'Project added Successfully')
                return redirect('/addproject')
            return render(request, 'add_project.html', {'form': form, 'errors': form.errors})
        return render(request, 'add_project.html', {'form': form, 'dberror': 'Project name already exist'})
    form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@login_required(login_url='/')
def assign_users(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        try:
            proj = Projects.objects.get(name=name)
            user = User.objects.get(username=username)
            proj.users.add(user)
            messages.add_message(request, messages.SUCCESS, 'User Assigned Successfully')
            return redirect('/assignusers')
        except ObjectDoesNotExist:
            return render(request, 'assign_users_projects.html', {'form': AssignProjectForm(request.POST), 'dberror': 'Project or User Does Not Exist'})
    return render(request, 'assign_users_projects.html', {'form': AssignProjectForm()})

@login_required(login_url='/')
def user_projects(request):
        user = User.objects.get(username=request.user)
        projects = user.projects.all()
        return render(request, 'user_assigned_projects.html', {'projects': projects})