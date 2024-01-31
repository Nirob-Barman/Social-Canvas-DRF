from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like, Comment
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser

from django.middleware.csrf import get_token
from django.contrib.sessions.models import Session

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


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

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        content = request.data.get('content', '')
        Comment.objects.create(user=request.user, post=post, content=content)
        return Response({'message': 'Comment added successfully'})


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

# class MyPostsView(generics.ListAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         # Get CSRF token
#         csrf_token = get_token(request)
#         # Get session ID
#         session_id = request.session.session_key

#         # Get the queryset
#         queryset = self.get_queryset()

#         # Serialize the queryset
#         serializer = self.get_serializer(queryset, many=True)

#         # Create the response data
#         data = {
#             'csrf_token': csrf_token,
#             'session_id': session_id,
#             'posts': serializer.data,
#         }

#         return Response(data)

# class MyPostsView(generics.ListAPIView):
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         user = self.request.user

#         # Check if the user is authenticated
#         if isinstance(user, AnonymousUser):
#             return Post.objects.none()

#         return Post.objects.filter(user=user)



# class AddPostView(generics.CreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
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
