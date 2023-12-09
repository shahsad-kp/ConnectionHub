from rest_framework.serializers import ModelSerializer

from Profile.models import Profile, Follow


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'about',
            'first_name',
            'full_name',
            'last_name',
            'profile_picture',
        )


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'followee']

    def save(self):
        self.instance = self.Meta.model(
            **self.validated_data
        )
