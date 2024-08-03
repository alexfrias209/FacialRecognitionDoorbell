from django.shortcuts import render,redirect
from .models import UserProfile
from .models import Account, MultipleImage, PhoneNumber, VideoSession, UserProfileImage
from .forms import uploadForm, uploadNumber, userUpdate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.utils import IntegrityError
from django.conf import settings
from django.db import IntegrityError
from .forms import UserProfileSelectionForm
from .api.blah import create_embeddings  # Import the create_embeddings function from blah.py
from django.core.files.base import ContentFile



@login_required(login_url='login')
def history_gallery(request, video_session_pk):
    video_session = VideoSession.objects.get(pk=video_session_pk)
    images = UserProfileImage.objects.filter(video_session=video_session)
    uProfile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileSelectionForm(uProfile, request.POST)
        if form.is_valid():
            selected_account = form.cleaned_data['account']
            if selected_account != '':
                # Add all images from the video session to the selected account
                for image in images:
                    MultipleImage.objects.create(account=selected_account, images=image.images)
                user_profile = request.user.userprofile
                data_path = user_profile.data_file.path    
                create_embeddings(user_profile, data_path)  # No need to return data
            images.delete()
            video_session.delete()
            return redirect('home')  # Redirect to the desired view
    else:
        form = UserProfileSelectionForm(uProfile)


    context = {'images': images, 'form': form}
    return render(request, 'base/historyGal.html', context)

@login_required(login_url='login')
def history_vid(request, pk):
    uProfile = UserProfile.objects.get(user=request.user)
    video_sessions = uProfile.video_sessions.all()
    video_sessions_with_images = []
    for session in video_sessions:
        if UserProfileImage.objects.filter(video_session=session).exists():
            video_sessions_with_images.append(session)
        else:
            session.delete()

    context = {'uProfile': uProfile, 'video_sessions': video_sessions_with_images}
    return render(request, 'base/videoGal.html', context)


def loginPage(request):
    page = 'login'
    form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            pass
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html',context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occured during registration')
    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def home(request):
    uProfile = UserProfile.objects.get(user=request.user)
    images = MultipleImage.objects.all()
    form = uploadForm()
    if request.method == 'POST':
        form = uploadForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.profile = uProfile
            try:
                account.save()
            except IntegrityError:
                messages.error(request, 'An account with that username already exists for this user.')
            return redirect('home')
    context = {'uProfile':uProfile, 'images':images, 'form':form,'MEDIA_URL': settings.MEDIA_URL,}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def updateForm(request, pk):
    uAccount = Account.objects.get(id=pk)
    form = uploadForm(instance=uAccount)
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES, instance=uAccount)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room.html', context)



@login_required(login_url='login')
def updateUser(request, pk):
    uProfile = UserProfile.objects.get(user=request.user)
    form = userUpdate(instance=uProfile)
    if request.method == 'POST':
        form = userUpdate(request.POST, request.FILES, instance=uProfile)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/userRoom.html', context)


@login_required(login_url='login')
def upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        account_id = request.POST.get('account_id')
        account = Account.objects.get(id=account_id)
        for image in images:
            MultipleImage.objects.create(account=account, images=image)

        # Call create_embeddings() to update the data file in the user profile
        user_profile = request.user.userprofile
        data_path = user_profile.data_file.path  
        create_embeddings(user_profile, data_path)  # No need to return data

        messages.success(request, 'Pictures saved!')
        return redirect('home')
    else:
        # rooms = Room.objects.all()
        images = MultipleImage.objects.all()
        context = { 'images': images}
        return render(request, 'base/home.html', context)




@login_required(login_url='login')
def viewing(request, pk):
    uAccount = Account.objects.get(id=pk)

    # Get all the MultipleImage objects related to the uAccount.
    uAccount_images = MultipleImage.objects.filter(account=uAccount)

    # Pass the uAccount_images to the template.
    context = {'uAccount': uAccount, 'uAccount_images': uAccount_images}
    return render(request, 'base/pictureGal.html', context)


@login_required(login_url='login')
def deleteForm(request, pk):
    uAccount = Account.objects.get(id=pk)
    context = {'uAccount':uAccount}
    if request.method == 'POST':
        print("baby")
        uAccount.delete()
        user_profile = request.user.userprofile
        data_path = user_profile.data_file.path
        create_embeddings(user_profile, data_path)  # No need to return data
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteNum(request, pk):
    nums = PhoneNumber.objects.get(id=pk)
    if request.method == 'POST':
        nums.delete()
        return redirect('num')
    
    return render(request, 'base/delete.html', {})

@login_required(login_url='login')
def numbers_page(request):
    uProfile = UserProfile.objects.get(user=request.user)
    form = uploadNumber()
    if request.method == 'POST':
        form = uploadNumber(request.POST)
    if form.is_valid():
        phone_number = form.cleaned_data['phone_number']
        existing_phone_number = PhoneNumber.objects.filter(user_profile=uProfile, phone_number=phone_number).first()
        if existing_phone_number:
            messages.error(request, 'A phone number with that phone number already exists for this user.')
        else:
        # phone number does not exist for the user, create a new record
            nums = form.save(commit=False)
            nums.user_profile_id = uProfile.id
            nums.save()
            messages.success(request, 'Number created successfully!')
            return redirect('num')


    context = {"uProfile":uProfile,'form':form}
    return render(request, 'base/numbers.html', context)


