from App_Message.models import Message
from App_Post.models import Notification


def base_context(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            user=request.user, is_new=True).count()
        unread_messages_count = Message.objects.filter(
            recipient=request.user, is_new=True).count()
    else:
        unread_notifications_count = 0
        unread_messages_count = 0

    return {
        'unread_notifications_count': unread_notifications_count,
        'unread_messages_count': unread_messages_count
    }
