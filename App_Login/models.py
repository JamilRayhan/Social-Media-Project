from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField( User, related_name='user_profile', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    full_name = models.CharField(max_length=264,blank=True)
    description = models.TextField(blank=True ,max_length=264)
    permanent_address = models.CharField(max_length=264,blank=True)
    present_address = models.CharField(max_length=264,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    facebook = models.URLField(blank=True)
    website=models.URLField(blank=True)
    
    
 
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
