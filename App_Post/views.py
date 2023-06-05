from django.shortcuts import HttpResponse,HttpResponseRedirect, redirect,render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile,Follow
from App_Post.models import Notification, Posts,Like,Comment
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
def liked(request, pk):
    post = Posts.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
        
        # Create a new notification for the post owner
        notification = Notification(user=post.author, post=post, liked_by=request.user)
        notification.save()
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

        comment = Comment(user=request.user, post=post, content=content)
        comment.save()
        
        # Create a new notification for the post owner
        notification = Notification(user=post.author, post=post, commented_by=request.user)
        notification.save()
        
        return redirect('App_Post:home')

    return render(request, 'App_Post/home.html')


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)
    return render(request, 'App_Post/notifications.html', {'notifications': notifications})
