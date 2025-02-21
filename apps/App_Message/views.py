from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageSendForm, MessageReplyForm
from django.contrib.auth.models import User
from django.db.models import Q
from apps.App_Post.context_processors import *

@login_required
def send_message(request, username):
    recipient = User.objects.get(username=username)

    if request.method == 'POST':
        msg_form = MessageSendForm(request.POST)
        if msg_form.is_valid():
            content = msg_form.cleaned_data['content']
            message = Message(sender=request.user,recipient=recipient, content=content)
            message.save()
            return redirect('App_Message:inbox')
    else:
        msg_form = MessageSendForm()
    context = {
        'msg_form': msg_form, 
        'recipient': recipient,
        **base_context(request)  
    }
    return render(request, 'App_Message/send_message.html',context )


@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    unread_messages = received_messages.filter(is_new=False)
    unread_messages_count = unread_messages.count()

    seen_senders = set()
    unique_conversations = []
    for message in received_messages:
        if message.sender not in seen_senders:
            seen_senders.add(message.sender)
            unique_conversations.append(message)

    context = {
        'received_messages': unique_conversations,
        'unread_messages':unread_messages,
        'unread_messages_count': unread_messages_count,
        **base_context(request)
    }
    return render(request, 'App_Message/inbox.html', context)


@login_required
def conversation_view(request, username1, username2):
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    # Get the messages exchanged between user1 and user2
    messages = Message.objects.filter(
        Q(sender=user1, recipient=user2) | Q(sender=user2, recipient=user1)
    ).order_by('timestamp')

    if request.method == 'POST':
        reply_form = MessageReplyForm(request.POST)
        if reply_form.is_valid():
            content = reply_form.cleaned_data['content']
            reply_message = Message(
                sender=request.user, recipient=user2, content=content)
            reply_message.save()
            return redirect('App_Message:conversation', username1=username1, username2=username2)
    else:
        reply_form = MessageReplyForm()

    # Mark messages as read
    unread_messages = messages.filter(recipient=request.user, is_new=True)
    for message in unread_messages:
        message.is_new = False
        message.save()

    context = {
        'messages': messages,
        'user1': user1, 
        'user2': user2, 
        'reply_form': reply_form,
        **base_context(request)  
    }
    return render(request, 'App_Message/conversation.html', context)



@login_required
def delete_conversation(request, username1, username2):
    user1 = User.objects.get(username=username1)
    user2 = User.objects.get(username=username2)

    # Delete the messages exchanged between user1 and user2
    Message.objects.filter(
        Q(sender=user1, recipient=user2) | Q(sender=user2, recipient=user1)
    ).delete()

    return redirect('App_Message:inbox')
