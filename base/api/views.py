from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import UserProfile, VideoSession
from django.shortcuts import get_object_or_404

from django.core.files.storage import FileSystemStorage
from rest_framework import status
import os
from django.core.exceptions import ObjectDoesNotExist
from .blah import facial



@api_view(['POST'])
def learning(request):
    unique_string = request.POST.get('unique_string')
    print(f"Received unique_string: {unique_string}")
    if unique_string:
        try:
            # Check if a profile with the given identifier exists in the database
            user_profile = UserProfile.objects.get(unique_string=unique_string)
        except ObjectDoesNotExist:
            print("No identifier found")
            return Response({'message': 'No identifier found'}, status=status.HTTP_404_NOT_FOUND)

        # Save the uploaded file to the specified directory
        fs = FileSystemStorage(location=os.path.join(os.path.expanduser('~'), 'Downloads'))
        file = request.FILES.get('video')
        filename = fs.save(file.name, file)
        saved_file_path = fs.path(filename)
        print(f"Saved file: {filename}")

        video_session = VideoSession(user_profile=user_profile)
        video_session.save()

        print("hello")
        facial(user_profile, saved_file_path, video_session)

        return Response({'message': 'File saved successfully'})


