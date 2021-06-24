from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import AdvUser


class Recipe(models.Model):
    MEAL_CHOICES = (
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
        ('Напиток', 'Напиток'),
        ('Десерт', 'Десерт'),
    )
    name = models.CharField(max_length=150, verbose_name="Название блюда")
    user = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField()
    url_video = models.CharField(max_length=400, verbose_name="Ссылка на видео", default="NUll", null=True)
    text = models.CharField(max_length=4000, verbose_name="Инструкция")
    image = models.ImageField(null=True)
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES, default='завтрак',
                                 verbose_name="Название трапезы")

    class Meta:
        verbose_name_plural = 'рецепты'
        verbose_name = 'рецепт'
        ordering = ['-name']

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    rating = models.IntegerField(
        verbose_name="Пользовательский рейтинг блюда",
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="ID блюда")

    class Meta:
        verbose_name_plural = 'рейтинги'
        verbose_name = 'рейтинг'
        ordering = ['-recipe_id']

    def __str__(self):
        return str(self.recipe_id)


class Ingredients(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="ID блюда")
    name = models.CharField(max_length=200, verbose_name="Название ингредиента")
    value = models.IntegerField(verbose_name="Вес ингредиента в граммах")

    class Meta:
        verbose_name_plural = 'ингредиенты'
        verbose_name = 'ингредиент'
        ordering = ['-name']

    def __str__(self):
        return self.name


class FavoriteDishes(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="ID блюда")

    class Meta:
        verbose_name_plural = 'любимые блюда'
        verbose_name = 'Любимые блюдо'

    def __str__(self):
        return str(self.recipe_id)


class Typing(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="ID блюда", null=True)
    complexity = models.IntegerField(
        verbose_name="Сложность приговления блюда",
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    cooking_time = models.IntegerField(verbose_name="Время приготовления в секундах")

    class Meta:
        verbose_name_plural = 'типизации'
        verbose_name = 'типизация'
        ordering = ['-recipe_id']

    def __str__(self):
        return str(self.recipe_id)


class Comments(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="ID блюда")
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True)
    data_time = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата время")
    text = models.CharField(max_length=200, verbose_name="Коментарий пользователя")

    class Meta:
        verbose_name_plural = 'комментарии'
        verbose_name = 'комментарий'
        ordering = ['-data_time']

    def __str__(self):
        return str(self.data_time) + " " + str(self.user)