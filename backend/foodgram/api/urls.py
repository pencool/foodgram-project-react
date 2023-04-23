from django.urls import include, path
from djoser.views import UserViewSet as UV
from rest_framework import routers
from api.views import (UserViewSet, TagViewSet,
                                        IngredientViewSet,
                                        RecipeViewSet)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('users/set_password/', UV.as_view({'post': 'set_password'})),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
