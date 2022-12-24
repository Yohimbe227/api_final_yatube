from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('follow', FollowViewSet)
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
