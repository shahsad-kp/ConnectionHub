from rest_framework.fields import CharField, ListField, FileField
from rest_framework.serializers import ModelSerializer

from Post.models import Post, Tag


class PostSerializer(ModelSerializer):
    posts = ListField(child=FileField())
    tags = ListField(source='tags.name', child=CharField(), required=True)

    class Meta:
        model = Post
        fields = (
            'profile',
            'caption',
            'tags',
            'location',
            'posts'
        )
        extra_kwargs = {'profile': {'read_only': True}}

    def create(self, validated_data):
        posts = validated_data.pop('posts')
        tags = validated_data.pop('tags')
        post = super().create(validated_data)
        tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
        post.tags.add(*tag_objects)

