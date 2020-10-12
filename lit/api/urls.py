from django.urls import path
from api import views

urlpatterns = [
    path('', views.root_view,),
    path('lit/', views.api_video_view,),
    path('lit/channel/', views.api_channel_view, name='channels'),
    path('lit/channel/<int:slug>/', views.api_channel_video_view, name='channel-detail'),
    path('lit/video/<int:slug>/update/', views.api_update_video_view, name='video-update'),
    path('lit/video/create/', views.api_create_video_view, name='video-create'),
    path('lit/video/watched/create/', views.api_create_watched_video_view, name='watched-video-create'),
    path('lit/video/browsed/create/', views.api_create_browsed_video_view, name='browsed-video-create'),
    path('lit/video/browsed/delete/', views.api_delete_browsed_video_view, name='browsed-video-delete'),
    path('lit/video/<slug>/delete/', views.api_delete_video_view, name='video-delete'),
    path('lit/list/', views.ApiVideoListView.as_view(), name='list'),
    path('lit/list/watched', views.WatchedVideoListView.as_view(), name='watched'),
    path('lit/list/browsed', views.BrowsedVideoListView.as_view(), name='browsed'),
    path('lit/channel/list/<slug>/', views.ApiChannelListView.as_view(), name='channel-detail-list'),
    path('likevideo/<videoId>', views.likeVideo, name='likepost'),
    path('islikedvideo/<videoId>', views.islikedVideo, name='likepost'),
    path('video/<int:pk>/likes/', views.LikeListView.as_view(), name='likes-list'),
    path('dislikevideo/<videoId>', views.dislikeVideo, name='dislikepost'),
    path('isdislikedvideo/<videoId>', views.isdislikedVideo, name='dislikepost'),
    path('video/<int:pk>/dislikes/', views.DislikeListView.as_view(), name='dislikes-list'),
    path('likescount/<videoId>', views.videoLikes, name='likes'),
    path('dislikescount/<videoId>', views.videoDislikes, name='dislikes'),
]