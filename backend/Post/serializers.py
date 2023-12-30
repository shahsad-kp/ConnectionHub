from typing import OrderedDict

from rest_framework.fields import CharField, ListField
from rest_framework.serializers import ModelSerializer

from Post.models import Post, Tag, PostImage
from Profile.models import Profile
from Profile.serializers import ProfileSerializer


class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = [
            'id',
            'file_name',
            'get_url'
        ]

    def to_representation(self, instance: PostImage):
        data = super().to_representation(instance)
        profile: Profile = self.context.get('profile')
        if profile and profile.id != instance.post.profile_id:
            data['put_url'] = instance.put_url
        return data


class PostSerializer(ModelSerializer):
    files = ListField(child=CharField(), write_only=True)
    tags = ListField(source='tags.name', child=CharField(), required=True)
    profile = ProfileSerializer(read_only=True)
    images = PostImageSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'profile',
            'caption',
            'tags',
            'location',
            'files',
            'images'
        )

    def create(self, validated_data: OrderedDict) -> Post:
        files = validated_data.pop('files')
        tags = validated_data.pop('tags')
        post = super().create(validated_data)
        tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
        post.tags.add(*tag_objects)
        for image in files:
            PostImage.objects.create(
                file_name=image,
                post=post
            )
        return post
