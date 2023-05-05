from django_filters import rest_framework as filters

from reviews.models import Recipe, Ingredient, Tag


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='in_cart_filter')
    author = filters.CharFilter(field_name='author__id', lookup_expr='exact')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                           queryset=Tag.objects.all())

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


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith', )

    class Meta:
        model = Ingredient
        fields = ('name',)
