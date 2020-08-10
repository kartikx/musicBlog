from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import default_storage as storage

from PIL import Image
import io

class Genre(models.Model):
    name = models.CharField(max_length=50, blank= True, null= True)
    desc = models.TextField(default="")
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
    changed_profile_photo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save()

        profile_photo_name = self.profile_photo.name.split('/')[1]

        """
        If this Object is being Created for the first time,
        then don't resize, it's using the Default Image.
        """
        if not self.changed_profile_photo:
            return;

        img_read = storage.open(self.profile_photo.name, 'r')
        img = Image.open(img_read)

        """
        I feel like this approach can be optimized, if
        I resize before Uploading
        """
        if img.height > 260 or img.width > 240:
            img = img.resize((240, 260))
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.profile_photo.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()
        

        img_read.close()