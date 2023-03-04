from typing import List, Union

from django.urls import reverse

from MainPosts.models import Post
from MainUsers.models import User


def get_suggested_posts(user: User) -> List[Post]:
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
    return suggested_posts


def get_saved_posts_context(user: User) -> list[list[dict[str, str]]]:
    saved_posts = user.saved_posts.all().order_by('-saved_at')
    post_rows = [[], []]
    for index, saved_post in enumerate(
            iterable=saved_posts,
            start=0
    ):
        post_rows[index % 2].append(saved_post.post.get_context(user))
    return post_rows


def get_posts_context(posts: Union[List[Post], Post], user: User) -> Union[dict[str, str], List[dict[str, str]]]:
    def create_post_context(post: Post) -> dict[str, str]:
        return {
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

    if isinstance(posts, Post):
        return create_post_context(posts)
    else:
        return [
            create_post_context(post)
            for post in posts
        ]



