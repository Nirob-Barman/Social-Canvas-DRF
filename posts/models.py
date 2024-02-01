from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(
        upload_to='posts/media/post_images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Post-{self.id} - {self.content} ({self.created_at})"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.like_count = Like.objects.filter(post=self.post).count()
        self.post.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.post.like_count = Like.objects.filter(post=self.post).count()
        self.post.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.comment_count = Comment.objects.filter(post=self.post).count()
        self.post.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.post.comment_count = Comment.objects.filter(post=self.post).count()
        self.post.save()