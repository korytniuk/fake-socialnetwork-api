from .models import User, Like, Post


def like_post(post: Post, user: User) -> Like:
    like, created = Like.objects.get_or_create(user=user, liked_post=post)

    return like


def unlike_post(post: Post, user: User):
    post.likes.remove(user)
