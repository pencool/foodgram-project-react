import base64
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import serializers
from users.models import User
from reviews.models import (Tag, Ingredient, Recipe, Favorite, Follow, Cart,
                            IngredientsAmount)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            frmt, image = data.split(';base64,')
            ext = frmt.split('/')[-1]
            data = ContentFile(base64.b64decode(image), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='user_is_subscribed')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'password',
            'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def user_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsAmountSerializer(read_only=True, many=True,
                                              source='ingredientsamount_set')
    image = Base64ImageField(required=True, allow_null=False)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='recipe_is_in_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='recipe_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def recipe_is_in_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj.id).exists()

    def recipe_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user=user, recipe=obj.id).exists()

    def validate(self, attrs):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not tags:
            serializers.ValidationError('Добавьте хотя бы один тег.')
        attrs['tags'] = tags
        if not ingredients:
            raise serializers.ValidationError(
                'Нельзя добавлять рецепты без ингредиентов.')
        attrs['ingredients'] = []
        for ing in ingredients:
            ingredient = get_object_or_404(Ingredient, id=ing['id'])
            if ingredient in attrs['ingredients']:
                raise serializers.ValidationError(
                    'Вы уже добавляли этот ингредиент.')
            attrs['ingredients'].append(ing)
        return attrs

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ing in ingredients:
            IngredientsAmount.objects.create(
                recipe=recipe,
                ingredient_id=ing['id'],
                amount=ing['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.tags.clear()
        instance.tags.set(self.initial_data.get('tags'))
        IngredientsAmount.objects.filter(recipe=instance).all().delete()
        for ing in validated_data.get('ingredients'):
            IngredientsAmount.objects.create(
                recipe=instance,
                ingredient_id=ing['id'],
                amount=ing['amount']
            )
        instance.save()
        return instance


class AddFavoriteCartShowSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='users.email', read_only=True)
    id = serializers.CharField(source='users.id', read_only=True)
    username = serializers.CharField(source='users.username', read_only=True)
    firs_name = serializers.CharField(source='users.first_name',
                                      read_only=True)
    last_name = serializers.CharField(source='users.last_name', read_only=True)
    is_subscribed = serializers.SerializerMethodField(
        method_name='user_is_subscribed')
    recipes = serializers.SerializerMethodField(
        method_name='recipes_limit')
    recipes_count = serializers.SerializerMethodField(
        method_name='ecipes_counter')

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def user_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author).exists()

    def recipes_limit(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filted(author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        return AddFavoriteCartShowSerializer(recipes, many=True).data

    def recipes_counter(self, obj):
        return Recipe.objects.filter(author=obj.author).count


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')