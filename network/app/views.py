from django.core.validators import ValidationError
from rest_framework import generics, permissions, status, viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Like, Post, User
from .serializers import (
    CreateUserSerializer,
    UserActivitySerializer,
    PostSerializer,
    UserSerializer,
    LikeSerializer,
)
from .services import like_post, unlike_post
from .filters import LikeFilter


class RegisterAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response("Invalid params", status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserActivityView(generics.RetrieveAPIView):
    serializer_class = UserActivitySerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikeListView(generics.ListAPIView):
    queryset = Like.objects.order_by("-created_at").all()
    serializer_class = LikeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeFilter


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        like_post(self.get_object(), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=True)
    def unlike(self, request, pk=None):
        unlike_post(self.get_object(), request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
