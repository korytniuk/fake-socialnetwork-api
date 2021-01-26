from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: True


class User(AbstractUser):
    last_request = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


class Post(TimeStampMixin):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, through="Like")

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Like(TimeStampMixin):
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("liked_post", "user")
