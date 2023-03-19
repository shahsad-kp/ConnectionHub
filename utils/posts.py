from typing import List, Dict

from Posts.models import Post
from Users.models import User


def get_suggested_post(user: User) -> List[Post]:
    followings = user.get_all_followings()
    suggested_posts = []
    for following_user in followings:
        suggested_posts.extend(
            following_user.posts.all()
        )
    suggested_posts.extend(
        user.posts.all()
    )
    suggested_posts.sort(
        key=lambda x: x.created_at,
        reverse=True
    )
    return suggested_posts


def get_saved_posts_context(user: User) -> list[list[Dict[str, str]]]:
    saved_posts = user.saved_posts.all().order_by('-saved_at')
    post_rows = [[], []]
    for index, saved_post in enumerate(
            iterable=saved_posts,
            start=0
    ):
        post_rows[index % 2].append(saved_post.post.get_context(user))

    return post_rows
