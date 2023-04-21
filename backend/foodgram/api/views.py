from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from reviews.models import Tag, Ingredient, Recipe, Favorite, Follow, Cart
from users.models import User
from api.serializers import (UserSerializer, TagSerializer,
                             IngredientSerializer, RecipeSerializer,
                             FavoriteSerializer, AddFavoriteCartShowSerializer,
                             FollowSerializer)


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
    lookup_field = 'id'
    search_fields = ('username',)

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
    def subscribe(self, request, id):
        cur_user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=id)
        value = Follow.objects.filter(user=cur_user.id, author=id)
        if request.method == 'POST':
            if value.exists():
                return Response(
                    {'error': f'Вы уже подписаны на этого автора.'})
            if cur_user == author:
                return Response({'error': f'Нельзя подписаться на себя.'})
            follow = Follow.objects.create(user=cur_user, author=author)
            serializer = self.serializer_class(follow,
                                               context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if value.exists():
                value.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': f'Вы не подписаны на этого автора.'})

    @action(methods=['get'], detail=False,
            queryset=Follow.objects.all(),
            url_path='subscriptions',
            serializer_class=FollowSerializer,
            pagination_class=PageNumberPagination,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):



class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

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
