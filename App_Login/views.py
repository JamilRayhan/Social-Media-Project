from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import CreateNewUser,AuthForm
from App_Login.models import UserProfile
# Create your views here.


def sign_up(request):
    form= CreateNewUser()
    registered= False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile= UserProfile(user=user)
            return HttpResponseRedirect(reverse('App_Login:login'))
    dict= {'title':'Sign up . Instagram','form':form,'registered':registered}
    return render(request,'App_Login/signup.html',context=dict)

def login_page(request):
    form=AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            
            if user is not None:
                login(request, user)
                pass
                #return HttpResponseRedirect(reverse('index'))
    return render(request, 'App_Login/login.html',context={'title':'Login','form':form} )


@login_required
def edit_profile(request):
    pass

