from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Comment, Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff'] 
        
        
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'like', 'category', )


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('create_dt', )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('like', )

        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'