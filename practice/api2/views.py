# from django.shortcuts import render
# from django.contrib.auth.models import User
# from rest_framework import viewsets

# from api2.serializers import CommentSerializer, PostSerializer, UserSerializer
# from blog.models import Comment, Post

# # Create your views here.
# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
    
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import  RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView, ListAPIView
from api2.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer , CateTagSerializer

from blog.models import Category, Comment, Post, Tag


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


# 상속받은 클래스가 다르기 때문에
# 코드가 동일해도 다르게 동작
class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer
    
#     # PATCH meethod
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         # data는 무조건 딕셔너리로 보내야 하고
#         data = {'like' : instance.like + 1}
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         # 화면에 표시되는 걸 바꾸고 싶다면 Response에 담아서 보내야 한다
#         return Response(data['like'])


# get_object()를 사용하려면 GenericAPIView를 상속받아야 한다
class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()
    
    # GET meethod
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
        
        return Response(instance.like)
    

# genericView들은 GetQuerySet, GetObject와 같은 테이블 처리 메서드들이 잇음
# 이런 메서드를 재사용할 거면 genericView를 상속받는거고
# 새로 코딩하는게 목적이라면 APIView를 상속받아야 한다

# genericView는 db에 관련된 처리를 하는 뷰에 붙인 용어
class CateTagAPIView(APIView):

    def get(self, request, *args, **kwargs):
       cateList = Category.objects.all()
       tagList = Tag.objects.all()
       data = {
           'cateList': cateList, 
           'tagList': tagList,
       } 
       serializer = CateTagSerializer(instance=data)
       return Response(serializer.data)
   
   
class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))
    
    
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
        
    