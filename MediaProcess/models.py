from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images_manipulated = models.IntegerField(default=0)
    video_manipulated = models.IntegerField(default=0)
    credits = models.IntegerField(default=10)

    def __str__(self) :
        return self.user.username


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    process_type = models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return self.title