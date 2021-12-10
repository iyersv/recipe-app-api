from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(many=True,queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True,queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_in_minutes', 'price', 'ingredients', 'tags', 'link']
        read_only_fields = ['id']
