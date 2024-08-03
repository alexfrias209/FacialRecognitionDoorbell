from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('update/<str:pk>/', views.updateForm, name='updateForm'),
    path('history_vid/<str:pk>/', views.history_vid, name='history_vid'),
    path('history_gallery/<int:video_session_pk>/', views.history_gallery, name='history_gallery'),
    path('viewing/<str:pk>/', views.viewing, name='viewing'),
    path('delete/<str:pk>/', views.deleteForm, name='deleteForm'),
    path('deletenum/<str:pk>/', views.deleteNum, name='deleteNum'),
    path('number/', views.numbers_page, name='num'),
    path('updateUser/<str:pk>/', views.updateUser, name='updateUser'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)