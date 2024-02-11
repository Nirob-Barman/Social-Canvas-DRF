from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser

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