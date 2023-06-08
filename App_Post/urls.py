from App_Post import views
from django.urls import path

app_name = 'App_Post'

urlpatterns = [
    path('', views.home, name='home'),
    path('liked/<pk>', views.liked, name='liked'),
    path('unlike/<pk>', views.unlike, name='unlike'),
    path('add-comment/<post_id>', views.add_comment, name='add_comment'),  
    path('notifications/', views.notifications, name='notifications'),
    path('delete-post/<post_id>/', views.delete_post, name='delete_post'),
    path('edit-post/<post_id>/', views.edit_post, name='edit_post'),
    path('post-details/<post_id>/', views.post_details, name='post_details'),
]
