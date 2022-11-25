import django
django.setup()
from django import forms
from django.contrib.auth.models import User
from proj.models import Clients, Projects


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
    password2 = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=155, required=True)
    last_name = forms.CharField(max_length=155, required=True)

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Password Doesn't Match")


class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    client = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    class Meta:
        model = Projects
        fields = "__all__"

class AssignProjectForm(forms.Form):
    name = forms.CharField(max_length=155)
    username = forms.CharField(max_length=155)