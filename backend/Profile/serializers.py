from rest_framework.serializers import ModelSerializer

from Profile.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'about',
            'first_name',
            'full_name'
            'last_name',
            'profile_picture',
        )

