from .models import Like
from django_filters import rest_framework as filters


class LikeFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Like
        fields = ("created_at",)
