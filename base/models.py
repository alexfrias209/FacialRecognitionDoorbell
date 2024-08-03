from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,default='account_picture/user-default.png')
    user_email = models.EmailField(max_length=200, blank=True, null=True)
    unique_string = models.CharField(max_length=50, unique=True, null=True, blank=True)
    data_file = models.FileField(upload_to='data_files/', null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username
        super(UserProfile, self).save(*args, **kwargs)


class VideoSession(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='video_sessions')
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.creation_date}"


class UserProfileImage(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video_session = models.ForeignKey(VideoSession, on_delete=models.CASCADE, null=True)  # Make this field nullable
    images = models.ImageField(null=False, blank=False, upload_to='user_profile_images/')

    def __str__(self):
        return str(self.user_profile.user.username)


class Account(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True, null=True)
    account_picture = models.ImageField(upload_to='account_picture/', null=True, blank=True, default='account_picture/user-default.png')


    class Meta:
        unique_together = ('profile', 'username')

    def __str__(self):
        return f"{self.username}"

    
class MultipleImage(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)  # Add null=True
    images = models.ImageField(null=False, blank=False)

    def __str__(self):
        return str(self.account.username)

class PhoneNumber(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(default='+1',error_messages={'invalid': 'Please enter a valid phone number in the format +12125552368.'})

    class Meta:
        unique_together = ('user_profile', 'phone_number')

    def __str__(self):
        return self.name
    
    