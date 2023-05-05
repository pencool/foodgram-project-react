from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.filters import RecipeFilter, IngredientsFilter
from api.permissions import (IsOwnerOrReadOnlyPermission, )
from api.serializers import (AddFavoriteCartShowSerializer, FollowSerializer,
                             IngredientSerializer,
                             RecipeSerializer, TagSerializer, UserSerializer)
from reviews.models import (Cart, Favorite, Follow, Ingredient,
                            IngredientsAmount, Recipe, Tag)
from users.models import User


def add(model, cur_user, pk, word, serializer=None):
    recipe = get_object_or_404(Recipe, id=pk)
    value = model.objects.filter(user=cur_user.id, recipe=pk)
    if value.exists():
        return Response({'error': f'Этот рецепт уже в {word}.'})
    model.objects.create(
        user=cur_user, recipe=recipe)
    return Response(serializer(recipe).data, status=status.HTTP_201_CREATED)


def delete(model, cur_user, pk, word):
    value = model.objects.filter(user=cur_user.id, recipe=pk)
    if value.exists():
        value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': f'Рецепта нет в {word}'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete']

    @action(methods=['get'], detail=False,
            queryset=User.objects.all(),
            permission_classes=(IsAuthenticated,)
            )
    def me(self, request):
        cur_user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(cur_user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True,
            queryset=Follow.objects.all(),
            url_path='subscribe',
            serializer_class=FollowSerializer,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk):
        cur_user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=pk)
        value = Follow.objects.filter(user=cur_user.id, author=pk)
        if request.method == 'POST':
            serializer = self.serializer_class(author, data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if value.exists():
                value.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Вы не подписаны на этого автора.'})

    @action(methods=['get'], detail=False,
            queryset=Follow.objects.all(),
            url_path='subscriptions',
            serializer_class=FollowSerializer,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        value = Follow.objects.filter(user=user)
        results = self.paginate_queryset(value)
        serializer = self.serializer_class(
            results, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsOwnerOrReadOnlyPermission, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True,
            queryset=Favorite.objects.all(),
            url_path='favorite',
            serializer_class=AddFavoriteCartShowSerializer,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        cur_user = get_object_or_404(User, id=request.user.id)
        if request.method == 'POST':
            return add(Favorite, cur_user, pk, 'избранном',
                       self.serializer_class)
        if request.method == 'DELETE':
            return delete(Favorite, cur_user, pk, 'избранном')

    @action(methods=['post', 'delete'], detail=True,
            queryset=Cart.objects.all(),
            url_path='shopping_cart',
            serializer_class=AddFavoriteCartShowSerializer,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        cur_user = get_object_or_404(User, id=request.user.id)
        if request.method == 'POST':
            return add(Cart, cur_user, pk, 'списке покупок',
                       self.serializer_class)
        if request.method == 'DELETE':
            return delete(Cart, cur_user, pk, 'списке покупок')

    @action(methods=['get'], detail=False,
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        cur_user = get_object_or_404(User, id=request.user.id)
        recipes = Cart.objects.filter(user=cur_user).values_list('recipe')
        ingredients = IngredientsAmount.objects.filter(
            recipe__id__in=recipes).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount')
        ingredients_for_shop = {}
        for ingredient in ingredients:
            ingr, mesur, amount = ingredient
            ingredients_for_shop.setdefault(ingr, [0, mesur])[0] += amount
        print(ingredients_for_shop)
        pdfmetrics.registerFont(TTFont('DejaVuSerif',
                                       'api/DejaVuSerif.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        p = canvas.Canvas(response)
        p.setFont('DejaVuSerif', 20)
        p.drawString(20, 800, f'{cur_user.get_full_name().title()}'
                              f' вот ваш список покупок!')
        p.setFont('DejaVuSerif', 18, )
        top = 776
        paragraph = 1
        for ingredient, params in ingredients_for_shop.items():
            p.drawString(20, top, f'{paragraph}) {ingredient.capitalize()}'
                                  f'({params[1]}) - {params[0]}')
            top -= 18
            paragraph += 1
        p.showPage()
        p.save()
        return response
