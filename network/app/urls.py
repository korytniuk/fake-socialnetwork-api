from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"posts", views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/", views.LikeListView.as_view(), name="analytics"),
    path("user/<int:pk>/", views.UserActivityView.as_view(), name="user_activity"),
    # path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("post/", views.PostCreateView.as_view(), name="create_post"),
    path("register/", views.RegisterAPI.as_view(), name="register"),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/access/", TokenRefreshView.as_view(), name="token_get_access"),
]
