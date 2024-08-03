from django.contrib import admin

# Register your models here.

from .models import UserProfile,Account,MultipleImage,PhoneNumber,UserProfileImage, VideoSession


admin.site.register(UserProfile)
admin.site.register(Account)
admin.site.register(MultipleImage)
admin.site.register(PhoneNumber)
admin.site.register(UserProfileImage)
admin.site.register(VideoSession)


