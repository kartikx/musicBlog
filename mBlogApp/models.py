from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Genre(models.Model):
    name = models.CharField(max_length=50, blank= True, null= True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length= 50, blank= False)
    artist = models.CharField(max_length= 50, blank= False)
    content = models.TextField(blank= True, null= True)
    date_posted = models.DateTimeField(blank= False, default= timezone.now)
    author = models.ForeignKey(User, on_delete= models.SET_NULL, blank= True, null= True)
    upvotes = models.IntegerField(blank= True, default= 0)
    upvotedby = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    albumart = models.ImageField(default='album_art/default.jpg', upload_to='album_art', blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank= True)
    spotifylink = models.CharField(max_length=100, blank= True, null= True)

    def __str__(self):
        return f'[{self.title}, {self.artist}]'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    profile_photo = models.ImageField(default='profile_photos/default.jpg', upload_to = 'profile_photos')

    def save(self):
        super().save()

        img = Image.open(self.profile_photo.path)

        if img.height > 260 or img.width > 240:
            img = img.resize((240, 260))
            img.save(self.profile_photo.path)
