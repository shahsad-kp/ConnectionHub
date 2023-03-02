from MainUsers.models import User


def get_suggestion_users_context(user: User):
    suggestions = user.get_suggestions()
    return [
        {
            'username': suggestion.username,
            'profile_picture': suggestion.profile_picture.url,
            'fullname': suggestion.full_name,
        }
        for suggestion in suggestions
    ]


def get_following_users_context(user: User):
    followings = user.get_all_followings()
    return [
        {
            'username': following.username,
            'profile_picture': following.profile_picture.url,
            'fullname': following.full_name,
        }
        for following in followings
    ]
