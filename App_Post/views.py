from django.shortcuts import HttpResponse,HttpResponseRedirect, redirect,render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile,Follow
from App_Post.models import Posts,Like,Comment
from django.contrib.auth.models import User
# Create your views here.
@login_required
def home(request):
    following_list=Follow.objects.filter(follower=request.user)
    posts=Posts.objects.filter(author__in=following_list.values_list('following'))
    liked_post= Like.objects.filter(user=request.user)
    liked_post_list=liked_post.values_list('post', flat=True)
    if request.method=='GET':
        search = request.GET.get('search',  ' ')
        result= User.objects.filter(username__icontains=search)
    return render(request,'App_Post/home.html',context={'title':'News Feed','search':search,'result':result,'posts':posts,'liked_post_list':liked_post_list})

@login_required
def liked(request,pk):
    post = Posts.objects.get(pk=pk)
    already_liked=Like.objects.filter(post=post,user=request.user)
    if not already_liked:
        liked_post= Like(post=post,user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unlike(request,pk):
    post = Posts.objects.get(pk=pk)
    already_liked=Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = Posts.objects.get(pk=post_id)
        author = request.user
        content = request.POST['content']

        comment = Comment(post=post, author=author, content=content)
        comment.save()
        return redirect('App_Post:home')

    return render(request, 'App_Post/home.html')
