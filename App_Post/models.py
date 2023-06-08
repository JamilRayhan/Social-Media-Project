from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=264, blank= True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-upload_date',]
        
        
class Like(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='liked_post')
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}:{}'.format(self.user,self.post)
    
    
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-date_created']
        
    
    def __str__(self):
        return f'{self.notification_type} notification for {self.user}'
