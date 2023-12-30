from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from Post.serializers import PostSerializer


class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: PostSerializer):
        serializer.save(profile=self.request.user.profile)
