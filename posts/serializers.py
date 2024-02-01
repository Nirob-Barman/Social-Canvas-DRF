from rest_framework import serializers
from .models import Post, Like, Comment

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'video_url', 'created_at', 'updated_at', 'like_count', 'comment_count']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
