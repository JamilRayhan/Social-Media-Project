from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile,Follow
from App_Post.models import Posts
from django.contrib.auth.models import User
# Create your views here.
@login_required
def home(request):
    following_list=Follow.objects.filter(follower=request.user)
    posts=Posts.objects.filter(author__in=following_list.values_list('following'))
    if request.method=='GET':
        search = request.GET.get('search',  ' ')
        result= User.objects.filter(username__icontains=search)
    return render(request,'App_Post/home.html',context={'title':'News Feed','search':search,'result':result,'posts':posts})