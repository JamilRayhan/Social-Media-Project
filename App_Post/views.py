from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile, Follow
from App_Post.models import Posts, Like, Comment, Notification
from django.contrib.auth.models import User
from .forms import PostForm
from .context_processors import base_context

# Create your views here.


@login_required
def home(request):
    if 'search' in request.GET:
        search_query = request.GET.get('search', '')
        return redirect('App_Post:search_results', search_query=search_query)

    following_list = Follow.objects.filter(follower=request.user)
    follower_list = Follow.objects.filter(following=request.user)
    following_users = following_list.values_list('following', flat=True)
    follower_users = follower_list.values_list('follower', flat=True)

    posts = Posts.objects.filter(author__in=following_users)
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    peoples = User.objects.exclude(id__in=following_users).exclude(id=request.user.id)

    context = {
        'title': 'News Feed',
        'posts': posts,
        'liked_post_list': liked_post_list,
        'peoples': peoples,
        'follower_list': follower_users,
        **base_context(request)
    }

    return render(request, 'App_Post/home.html', context)


@login_required
def search_results(request):
    search_query = request.GET.get('search', '')
    users = User.objects.filter(username__icontains=search_query)
    posts = Posts.objects.filter(caption__icontains=f"#{search_query}")

    context = {
        'title': 'Search Results',
        'search_query': search_query,
        'users': users,
        'posts': posts,
        **base_context(request)
    }

    return render(request, 'App_Post/search_results.html', context)


@login_required
def liked(request, pk):
    post = Posts.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()

        # Create a notification for the author of the post
        if post.author != request.user:
            notification = Notification(
                user=post.author, notification_type='Like', target=request.user, post=post)
            notification.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def unlike(request, pk):
    post = Posts.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Posts, pk=post_id)
        content = request.POST['content']

        comment = Comment(post=post, author=request.user, content=content)
        comment.save()

        # Create a notification for the author of the post
        if post.author != request.user:
            notification = Notification(
                user=post.author, notification_type='Comment', target=request.user, post=post, comment=comment)
            notification.save()

        # Redirect to the previous page
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'App_Post/home.html')


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    unread_notifications = notifications.filter(is_new=True, user=request.user)
    unread_notifications_count = unread_notifications.count()
    for notification in unread_notifications:
        notification.is_new = False
        notification.save()
    context = {
        'notifications': notifications,
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
        **base_context(request)
    }
    return render(request, 'App_Post/notifications.html', context)


@login_required
def delete_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('App_Login:user', username=request.user.username)
    else:
        return HttpResponse("You are not authorized to delete this post.")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('App_Login:user', username=request.user.username)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        **base_context(request)
    }
    return render(request, 'App_Post/edit_post.html', context)


@login_required
def post_details(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    context = {
        'post': post,
        **base_context(request)
    }
    return render(request, 'App_Post/post_details.html', context)
