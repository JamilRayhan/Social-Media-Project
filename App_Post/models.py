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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, related_name='liked_notifications', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, related_name='commented_notifications', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Notification for {self.user.username}'
