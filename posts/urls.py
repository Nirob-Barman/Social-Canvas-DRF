from django.urls import path
from .views import (
    PostListView,
    PostListViewSet,
    PostDetailView,
    LikeCreateView,
    UserHasLikedView,
    UnlikePostView,
    UserLikedPostsView,
    AllLikedPostsView,
    TopLikedPostsView,
    LeastLikedPostsView,
    CommentCreateView,
    UserCommentsListView,
    AllCommentsListView,
    PostCommentCountView,
    PostCommentsListView,
    CommentUpdateView,
    CommentDeleteView,
    MyPostsView,
    AddPostView,
    UpdatePostView,
    DeletePostView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'all_posts', PostListViewSet, basename='post')

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/create/<int:post_id>/', LikeCreateView.as_view(), name='create_like'),
    path('like/check/<int:post_id>/', UserHasLikedView.as_view(), name='user_has_liked'),
    path('like/unlike/<int:post_id>/', UnlikePostView.as_view(), name='unlike_post'),
    path('user/liked-posts/', UserLikedPostsView.as_view(), name='user_liked_posts'),
    path('liked-posts/all/', AllLikedPostsView.as_view(), name='all_liked_posts'),
    path('liked-posts/top/', TopLikedPostsView.as_view(), name='top_liked_posts'),
    path('liked-posts/least/', LeastLikedPostsView.as_view(), name='least_liked_posts'),
    path('comments/<int:post_id>/', CommentCreateView.as_view(), name='create_comment'),
    path('user/comments/', UserCommentsListView.as_view(), name='user_comments'),
    path('comments/all/', AllCommentsListView.as_view(), name='all_comments'),
    path('comments/count/<int:post_id>/', PostCommentCountView.as_view(), name='post_comment_count'),
    path('comments/post/<int:post_id>/', PostCommentsListView.as_view(), name='post_comments_list'),
    path('comments/update/<int:comment_id>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/delete/<int:comment_id>/', CommentDeleteView.as_view(), name='delete_comment'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('add-post/', AddPostView.as_view(), name='add-post'),
    path('my-posts/update/<int:pk>', UpdatePostView.as_view(), name='update-post'),
    path('my-posts/delete/<int:pk>', DeletePostView.as_view(), name='update-post')
]

urlpatterns += router.urls
