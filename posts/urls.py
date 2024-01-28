from django.urls import path
from .views import PostListView, PostDetailView, LikeView, CommentView, MyPostsView, AddPostView, UpdatePostView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# app_name = 'posts'

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/<int:pk>', LikeView.as_view(), name='like-post'),
    path('comment/<int:pk>', CommentView.as_view(), name='comment-post'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('my-posts/update/<int:pk>', UpdatePostView.as_view(), name='update-post')
]

urlpatterns += router.urls
