from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Comment, Post, Category, Tag

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff'] 
        
        
class PostListSerializer(serializers.ModelSerializer):
    # category가 pk로 나오는 이유는 PrimaryKeyRelatedField로 잡아놔서 그렇고
    # 여기서 오버라이딩하면 됨
    # source에 넣어주면 이 값을 category필드에 반영해준다!
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'like', 'category', )


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('create_dt', )


# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('like', )

        
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
# class CateTagSerializer(serializers.Serializer):
#     cateList = CategorySerializer(many=True)
#     tagList = TagSerializer(many=True)


class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())


class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title')


class CommentSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'updated_at')

class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub()
    nextPost = PostSerializerSub()
    commentList = CommentSerializerSub(many=True)