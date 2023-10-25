from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Comment, Post, Category, Tag

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )


# 우리가 직접 필드를 정의할 거기 때무넹 Serializer를 상속받는다
class CateTagSerializer(serializers.Serializer):
    cateList = CategorySerializer(many=True)
    tagList = TagSerializer(many=True)
    