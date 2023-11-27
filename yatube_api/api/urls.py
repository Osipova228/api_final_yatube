from django.urls import include, path
from rest_framework import routers

from .views import (PostViewSet, FollowViewSet,
                    GroupViewSet, CommentViewSet)


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'posts/(?P<post_id>[1-9]\d*)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
