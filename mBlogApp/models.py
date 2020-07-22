from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length= 50, blank= False)
    artist = models.CharField(max_length= 50, blank= False)
    content = models.TextField(blank= True, null= True)
    date_posted = models.DateField(blank= False, default= timezone.now)
    author = models.ForeignKey(User, on_delete= models.SET_NULL, blank= True, null= True)

    def __str__(self):
        return f'[{self.title}, {self.artist}]'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    profile_photo = models.ImageField(default='default.jpg', upload_to = 'profile_photos')
