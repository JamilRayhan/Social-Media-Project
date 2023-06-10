from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import CreateNewUser,AuthForm,EditProfile
from App_Login.models import UserProfile,Follow

from App_Post.forms import PostForm
from django.contrib.auth.models import User

from App_Post.models import Notification
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
            user_profile.save()
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
                return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request, 'App_Login/login.html',context={'title':'Login','form':form} )


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form= EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES,instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form=EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/profile.html',context={'form':form,'title':'Edit Profile . Social'})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    follower_list = [follower.follower.username for follower in Follow.objects.filter(following=user)]
    following_list = [following.following.username for following in Follow.objects.filter(follower=user)]  
    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'App_Login/user.html', context={'title':request.user.username, 'post':post_form, 'follower_list': follower_list, 'following_list': following_list})


@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    follower_list = [follower.follower.username for follower in Follow.objects.filter(following=user_other)]
    following_list = [following.following.username for following in Follow.objects.filter(follower=user_other)]  

    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/other_user.html', context={'user_other': user_other, 'title': user_other.username, 'already_followed': already_followed, 'follower_list': follower_list, 'following_list': following_list})



@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)

    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()

        # Create a notification for the user being followed
        notification = Notification(user=following_user, notification_type='Follow', target=follower_user)
        notification.save()

    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username': username}))


@login_required
def unfollow(request,username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user,following= following_user)
    already_followed.delete()
    
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username':username}))

    