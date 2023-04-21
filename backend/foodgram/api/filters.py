from django_filters import rest_framework as filters
from reviews.models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='in_cart_filter')
    author = filters.CharFilter(field_name='author__id', lookup_expr='exact')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',
                                           lookup_expr='exact')

    def favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite_recipe__user=user)
        if not value and user.is_authenticated:
            return queryset.exclude(favorite_recipe__user=user)
        return queryset

    def in_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(cart_recipe__user=user)
        if not value and user.is_authenticated:
            return queryset.exclude(cart_recipe__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
