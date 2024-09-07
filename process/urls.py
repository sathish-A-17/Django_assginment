from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('search/', views.search, name='search'),
]