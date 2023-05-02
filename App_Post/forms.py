from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from App_Post.models import Posts

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields = ('image','caption',)
