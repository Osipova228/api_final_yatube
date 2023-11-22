from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import PostViewSet, FollowViewSet, GroupViewSet, api_comments, api_comment_detail


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/posts/<int:post_id>/comments/', api_comments),
    path('v1/posts/<int:post_id>/comments/<int:pk>/', api_comment_detail),
    path('v1/', include('djoser.urls.jwt')),
]
