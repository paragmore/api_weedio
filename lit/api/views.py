from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView
from django.views.generic import ListView
from random import shuffle
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.dispatch import receiver, Signal
from django.core.signals import request_finished
from rest_framework_tracking.mixins import LoggingMixin
from django.contrib.auth.decorators import login_required



from api.models import Video, Channel, Like, Dislike, Watched, Browser
from api.serializers import VideoSerializer,ChannelVideoSerializer,ChannelSerializer, LikeSerializer, DislikeSerializer, WatchedVideoSerializer, BrowsedVideoSerializer
from accounts.serializers import UserSerializer




def root_view(request):
    now = datetime.now()
    html = "<html><body>Welcome to the Lit API. It is now %s.</body></html>" % now
    return HttpResponse(html)


@api_view(['GET',])
def api_video_view(request):
    if request.method == 'GET':
        videos = Video.objects.all()
        
        serializer = VideoSerializer(videos,context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET',])
def api_channel_view(request):
    if request.method == 'GET':
        channels = Channel.objects.all()
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data)


@api_view(['GET',])
def api_channel_video_view(request,slug):
    if request.method == 'GET':
        videos = Channel.objects.filter(id=slug)
        serializer = ChannelVideoSerializer(videos, many=True)
        return Response(serializer.data)

@api_view(['PUT',])
def api_update_video_view (request,slug):
    if request.method == 'PUT':
        video = Video.objects.filter(id=slug)
        serializer = VideoSerializer(video, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]= "update successful"
            return Response(data=data)
        return Response(serializer.errors,)
    
@api_view(['DELETE',])
def api_delete_video_view (request,slug):
    if request.method == 'DELETE':
        video = Video.objects.filter(videoId=slug)
        operation= video.delete()
        data={}
        if operation:
            data["success"]= "delete successful"
        else:
            data["failure"]= "delete failed" 
        return Response(data=data)

@api_view(['POST',])
def api_create_video_view (request):
    if request.method == 'POST':
        video = Video()
        serializer = VideoSerializer(video, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]= "update successful"
            return Response(serializer.data)
        return Response(serializer.errors,)

@api_view(['POST',])
def api_create_watched_video_view (request):
    if request.method == 'POST':
        watched = Watched()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        if request.user.id:
            serializer = WatchedVideoSerializer(watched, data={**request.data, **{'user': str(request.user.id),},**{'ip':str(ip)}})
        else: 
            serializer = WatchedVideoSerializer(watched, data={**request.data, **{'user':''},**{'ip':str(ip)}})
        print(request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]= "update successful"
            return Response(serializer.data)
        return Response(serializer.errors,)

@api_view(['POST',])
def api_create_browsed_video_view (request):
    if request.method == 'POST':
        browsed = Browser()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        if request.user.id:
            serializer = BrowsedVideoSerializer(browsed, data={**request.data, **{'user': str(request.user.id),},**{'ip':str(ip)}})
        else: 
            serializer = BrowsedVideoSerializer(browsed, data={**request.data, **{'user':''},**{'ip':str(ip)}})
        print(request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]= "update successful"
            return Response(serializer.data)
        return Response(serializer.errors,)

@api_view(['DELETE',])
def api_delete_browsed_video_view (request):
    if request.method == 'DELETE':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        if(request.user.id):
            browsed = Browser.objects.filter(user=request.user)
        else:
            browsed = Browser.objects.filter(ip__contains=ip)
            
        operation= browsed.delete()
        data={}
        if operation:
            data["success"]= "delete successful"
        else:
            data["failure"]= "delete failed" 
        return Response(data=data)
        
class ApiVideoListView(LoggingMixin,ListAPIView):
    serializer_class= VideoSerializer
    pagination_class= PageNumberPagination
    
    def get_queryset(self, **kwargs):
        now= timezone.now()
        earlier= now -timedelta(minutes=45)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        if self.request.user.id:
            queryset= Video.objects.exclude(videoId__in=self.request.user.watched_set.all().values('videoId')).exclude(videoId__in= Browser.objects.filter(user=self.request.user, timestamp__range=(earlier, now)).values('videoId')).order_by("?")
        else:
            queryset= Video.objects.exclude(videoId__in= Watched.objects.filter(ip__contains=ip).values('videoId')).exclude(videoId__in= Browser.objects.filter(ip__contains=ip, timestamp__range=(earlier, now)).values('videoId')).order_by("?")
        return queryset

class WatchedVideoListView(LoggingMixin,ListAPIView):
    serializer_class= WatchedVideoSerializer
    pagination_class = None
    def get_queryset(self, **kwargs):
        queryset= Watched.objects.filter(user=self.request.user)
        return queryset

class BrowsedVideoListView(LoggingMixin,ListAPIView):
    serializer_class= BrowsedVideoSerializer
    pagination_class = None
    def get_queryset(self, **kwargs):
        now= timezone.now()
        earlier= now -timedelta(minutes=45)
        queryset= Browser.objects.filter(timestamp__range=(earlier, now))
        return queryset


class ApiChannelListView(LoggingMixin,ListAPIView):
 
    def get_queryset(self, **kwargs):
        now= timezone.now()
        earlier= now -timedelta(minutes=45)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        if self.request.user.id:
            queryset= Video.objects.filter(channel_id=self.kwargs['slug']).exclude(videoId__in=self.request.user.watched_set.all().values('videoId')).exclude(videoId__in= Browser.objects.filter(user=self.request.user, timestamp__range=(earlier, now)).values('videoId')).order_by("?")
        else:
            queryset= Video.objects.filter(channel_id=self.kwargs['slug']).exclude(videoId__in= Watched.objects.filter(ip__contains=ip).values('videoId')).exclude(videoId__in= Browser.objects.filter(ip__contains=ip, timestamp__range=(earlier, now)).values('videoId')).order_by("?")
        return queryset
        # queryset =Video.objects.filter(channel_id=self.kwargs['slug'])
        # return queryset
    
    serializer_class= VideoSerializer
    pagination_class= PageNumberPagination

class LikeListView(LoggingMixin,ListAPIView):
    model = Like
    permission_classes = [
    permissions.IsAuthenticated,
  ]

    def get_queryset(self, **kwargs):
        # org qs
        queryset = Like.objects.all()
        # filter by var from captured url
        return queryset.filter(video__pk=self.kwargs['pk'])
    serializer_class= LikeSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def likeVideo(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        likedvideo = Video.objects.get(videoId=video_id)  # getting the liked post

        if Like.objects.filter(video=likedvideo, liker=request.user).exists():
            Like.objects.filter(video=likedvideo, liker=request.user).delete()
            return HttpResponse(likedvideo.likes.count())
        else:
            m = Like(video=likedvideo, liker=request.user)  # creating like object
            m.save()  # saves into database
            return HttpResponse(likedvideo.likes.count())
    else:
        return HttpResponse("Request method is not a GET")

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dislikeVideo(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        dislikedvideo = Video.objects.get(videoId=video_id)  # getting the liked post

        if Dislike.objects.filter(video=dislikedvideo, disliker=request.user).exists():
            Dislike.objects.filter(video=dislikedvideo, disliker=request.user).delete()
            return HttpResponse(dislikedvideo.dislikes.count())
        else:
            m = Dislike(video=dislikedvideo, disliker=request.user)  # creating like object
            m.save()  # saves into database
            return HttpResponse(dislikedvideo.dislikes.count())
    else:
        return HttpResponse("Request method is not a GET")

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def islikedVideo(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        likedvideo = Video.objects.get(videoId=video_id)  # getting the liked post

        if Like.objects.filter(video=likedvideo, liker=request.user).exists():
            return JsonResponse({'likecount': likedvideo.likes.count(), 'isliked': 'liked'})
        else:  # saves into database
            return JsonResponse({'likecount': likedvideo.likes.count(), 'isliked': 'not liked'})
    else:
        return HttpResponse("Request method is not a GET")

class DislikeListView(LoggingMixin,ListAPIView):
    model = Dislike
    permission_classes = [
    permissions.IsAuthenticated,
  ]

    def get_queryset(self, **kwargs):
        # org qs
        queryset = Dislike.objects.all()
        # filter by var from captured url
        return queryset.filter(video__pk=self.kwargs['pk'])
    serializer_class= DislikeSerializer



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def isdislikedVideo(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        dislikedvideo = Video.objects.get(videoId=video_id)  # getting the liked post

        if Dislike.objects.filter(video=dislikedvideo, disliker=request.user).exists():
            return JsonResponse({'dislikecount': dislikedvideo.dislikes.count(), 'isdisliked': 'disliked'})
        else:  # saves into database
            return JsonResponse({'dislikecount': dislikedvideo.dislikes.count(), 'isdisliked': 'not disliked'})
    else:
        return HttpResponse("Request method is not a GET")

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def videoDislikes(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        dislikedvideo = Video.objects.get(videoId=video_id)  # getting the liked post
        return JsonResponse({'dislikescount': dislikedvideo.dislikes.count()})
    else:
        return HttpResponse("Request method is not a GET")

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def videoLikes(request, **kwargs):
    serializer= UserSerializer()
    if request.method == 'GET':
        video_id = kwargs['videoId']
        likedvideo = Video.objects.get(videoId=video_id)  # getting the liked post
        return JsonResponse({'likescount': likedvideo.likes.count()})
    else:
        return HttpResponse("Request method is not a GET")













