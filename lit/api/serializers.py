from rest_framework import serializers

from api.models import Video, Channel, Like, Dislike, Watched, Browser

class VideoSerializer(serializers.ModelSerializer):
    channel_id= serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all(),source='channel.channelName')
    class Meta:
        model = Video
        fields = ['id', 'videoId', 'caption', 'channel_id']

class WatchedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = ['id', 'videoId', 'user', 'ip']

class BrowsedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Browser
        fields = ['id', 'videoId', 'user', 'ip']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'liker', 'video', 'date_created']

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id', 'disliker', 'video', 'date_created']

class ChannelVideoSerializer(serializers.ModelSerializer):
    videos= VideoSerializer(many=True)

    class Meta:
        model = Channel
        fields = ['id', 'channelName', 'videos']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'channelName']