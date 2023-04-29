from django.contrib import admin

from reviews.models import (Cart, Favorite, Follow, Ingredient,
                            IngredientsAmount, Recipe, Tag)


class IngredientsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']


class RecipesModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']
    readonly_fields = ['added_to_favorites']

    def added_to_favorites(self, obj):
        return obj.favorite_recipe.count()
    added_to_favorites.short_description = 'Добавлен в избранное'


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(Recipe, RecipesModelAdmin)
admin.site.register(Follow)
admin.site.register(Ingredient, IngredientsModelAdmin)
admin.site.register(IngredientsAmount)
