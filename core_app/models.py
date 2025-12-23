from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(max_length=200, verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Посты"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatarURL = models.CharField(max_length=255, verbose_name="Profile picture", default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
