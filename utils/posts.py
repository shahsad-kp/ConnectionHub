from typing import List

from django.urls import reverse

from MainPosts.models import Post
from MainUsers.models import User


def get_suggested_posts_context(user: User) -> List[dict[str, str]]:
    followings = user.get_all_followings()
    suggested_posts = []
    for following_user in followings:
        suggested_posts.extend(
            following_user.get_posts()
        )
    suggested_posts.sort(
        key=lambda x: x.created_at,
        reverse=True
    )
    return get_posts_context(suggested_posts, user)


def get_posts_context(posts: List[Post], user: User) -> List[dict[str, str]]:
    return [
        {
            'id': post.id,
            'user': {
                'username': post.user.username,
                'profile_picture': post.user.profile_picture.url,
            },
            'image': post.image.url,
            'caption': post.caption,
            'likes': post.likes_count,
            'dislikes': post.dislikes_count,
            'liked': post.reactions.filter(user=user, reaction='like').exists(),
            'disliked': post.reactions.filter(user=user, reaction='dislike').exists(),
            'comments': post.comments_count,
            'saved': post.saved_by.filter(user=user).exists(),
            'url': reverse(
                'post-detail',
                kwargs={
                    'post_id': post.id
                }
            )
        }
        for post in posts
    ]