from django.urls import path
from .views import (
    PostListView,
    PostListViewSet,
    PostDetailView,
    CommentView,
    MyPostsView,
    AddPostView,
    UpdatePostView,
    DeletePostView,
    LikeView
    # like_unlike_post,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'all_posts', PostListViewSet, basename='post')

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/<int:pk>', LikeView.as_view(), name='like-post'),
    # path('like/<int:pk>/', like_unlike_post, name='like-post'),
    # path('like/<int:pk>/', LikePostView.as_view(), name='like-post'),
    # path('comment/<int:pk>', CommentView.as_view(), name='comment-post'),
    path('comment/<int:post_id>', CommentView.as_view(), name='comment-post'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('my-posts/update/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('my-posts/delete/<int:pk>', DeletePostView.as_view(), name='update-post')
]

urlpatterns += router.urls
