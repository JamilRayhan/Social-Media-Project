from django.urls import path
from . import views

app_name = 'App_Message'

urlpatterns = [
    path('send/<username>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<username1>/<username2>/', views.conversation_view, name='conversation'),
    path('delete_conversation/<username1>/<username2>/', views.delete_conversation, name='delete_conversation'),
]
