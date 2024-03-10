from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import AnonymousUser, User

from django.middleware.csrf import get_token
from django.contrib.sessions.models import Session

from rest_framework.decorators import api_view, permission_classes

class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user for the new post
        serializer.save(user=self.request.user)

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


# class PostListView(generics.ListAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({'request': self.request})
#         return context


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.create(user=request.user, post=post)
        return Response({'message': 'Post liked successfully'})

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'message': 'Like removed successfully'})
        return Response({'message': 'Like not found'})


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):  # Rename pk to post_id
        post = get_object_or_404(Post, pk=post_id)
        content = request.data.get('content', '')
        Comment.objects.create(user=request.user, post=post, content=content)
        return Response({'message': 'Comment added successfully'})
    


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class UserCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the authenticated user
        user = self.request.user
        # Return all comments by the authenticated user
        return Comment.objects.filter(user=user)


class AllCommentsListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class PostCommentCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, format=None):
        # Retrieve the post based on post_id
        post = get_object_or_404(Post, id=post_id)
        # Count the comments for the post
        comment_count = Comment.objects.filter(post=post).count()
        # Return the comment count in the response
        return Response({'comment_count': comment_count})

# class CommentUpdateView(generics.UpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         comment_id = self.kwargs.get('comment_id')
#         # Retrieve the comment and check if the user is the owner
#         comment = get_object_or_404(Comment, id=comment_id, user=self.request.user)
#         return comment

class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the current user is the owner of the comment
        if comment.user != self.request.user:
            self.permission_denied(self.request)
        
        return comment


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the post based on post_id
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        # Return all comments for the specified post
        return Comment.objects.filter(post=post)


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class AddPostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        # Include the current user in the serializer context
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class UpdatePostView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # Override the default get_object to include user check
#         obj = super().get_object()
#         if obj.user == self.request.user:
#             return obj
#         raise PermissionDenied("You don't have permission to update this post.")


class UpdatePostView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Override the default get_object to include user check
        obj = super().get_object()
        if obj.user == self.request.user:
            return obj
        raise PermissionDenied(
            "You don't have permission to update this post.")

    def get(self, request, *args, **kwargs):
        # Retrieve the current object data
        current_object = self.get_object()
        serializer = self.get_serializer(current_object)
        return Response(serializer.data)


# class DeletePostView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, pk):
#         # Ensure user owns the post
#         post = get_object_or_404(Post, pk=pk, user=request.user)
#         post.delete()
#         return Response({'message': 'Post deleted successfully'}, status=204)

# class DeletePostView(APIView):
#     def delete(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)

#         # Check if the user making the request is the owner of the post
#         if request.user != post.user:
#             return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

#         post.delete()
#         return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class DeletePostView(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Check if the user making the request is the owner of the post
        if request.user != post.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)