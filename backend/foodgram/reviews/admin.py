from django.contrib import admin
from reviews.models import (Tag, Favorite, Cart, Recipe, Follow, Ingredient,
                            IngredientsAmount)


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(Recipe)
admin.site.register(Follow)
admin.site.register(Ingredient)
admin.site.register(IngredientsAmount)
