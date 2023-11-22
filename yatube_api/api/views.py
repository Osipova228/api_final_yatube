# TODO:  Напишите свой вариант
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post, Follow, User, Comment, Group
from .permissions import AllowAnyPermission, IsGetRequest, IsAuthorOrReadOnly
from .serializers import FollowSerializer, PostSerializer, CommentSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('group',)
    permission_classes = (IsAuthorOrReadOnly, IsGetRequest)

    def perform_create(self, serializer):
        try:
            if self.request.user.is_authenticated:
                serializer.save(author=self.request.user)
            else:
                serializer.save(author=None)
        except IntegrityError:
            return Response({"error": "Author is required for creating a post"}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer):
        following_username = self.request.data.get('following')
        try:
            following_user = User.objects.get(username=following_username)
        except ObjectDoesNotExist:
            raise ValidationError('Пользователь не найден!')

        existing_follow = Follow.objects.filter(user=self.request.user, following=following_user).first()
        if existing_follow:
            raise ValidationError('Вы уже подписаны на этого пользователя.')

        if self.request.user == following_user:
            raise ValidationError('Невозможно подписаться на самого себя.')

        serializer.save(
            user=self.request.user,
            following=following_user
        )
        response_data = serializer.data
        response_data['following'] = following_username
        return Response(response_data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = get_object_or_404(
            User,
            username=self.request.user.username
        )
        return Follow.objects.filter(user=user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAnyPermission]


@api_view(['GET', 'POST'])
@permission_classes([IsGetRequest])
def api_comments(request, post_id):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsGetRequest])
def api_comment_detail(request, post_id, pk):
    comment = get_object_or_404(Comment, post_id=post_id, id=pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if comment.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommentSerializer(
            comment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
