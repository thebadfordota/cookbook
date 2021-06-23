from django.db import models
from datetime import datetime

from accounts.models import AdvUser
# Create your models here.



class recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,null = False, verbose_name="Имя блюда")
    user = models.ForeignKey(AdvUser,on_delete = models.SET_NULL, null = True )
    public = models.BooleanField()
    url_video = models.CharField(max_length=400,
                                 null=True, verbose_name="Ссылка на ютую видео", default="NUll")
    text = models.CharField(max_length=4000, null=False, verbose_name="Инструкция")
    image = models.ImageField(null = True)
    class Meta:
        verbose_name_plural = 'рецепты'
        verbose_name = 'рецепт'
        ordering = ['-name']

    def __str__(self):
        return self.name

class rating(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE )
    rating = models.IntegerField(null = False,
                                 verbose_name="Рейтинг блюда поставленное пользователем по 5 бальной шкале" )
    recipe_id = models.ForeignKey('recipe',
                                  null = False, on_delete= models.CASCADE, verbose_name="ID блюда")
    class Meta:
        verbose_name_plural = 'рейтинги'
        verbose_name = 'рейтинг'
        ordering = ['-recipe_id']

    def __str__(self):
        return self.recipe_id
class ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_id = models.ForeignKey('recipe', null=False, on_delete=models.CASCADE, verbose_name="ID блюда")
    name = models.CharField(max_length=200, null = False,verbose_name="Название ингредиента")
    value = models.IntegerField(null=False, verbose_name="Вес ингредиента в граммах")
    class Meta:
        verbose_name_plural = 'ингридиенты'
        verbose_name = 'ингридиент'
        ordering = ['-name']

    def __str__(self):
        return self.name
class favorite_dishes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AdvUser,on_delete = models.CASCADE)
    recipe_id = models.ForeignKey('recipe', null = False, on_delete= models.CASCADE, verbose_name="ID блюда")

    class Meta:
        verbose_name_plural = 'любимые блюда'
        verbose_name = 'Любимые блюдо'

    def __str__(self):
        return self.id

class typing(models.Model):
    recipe_id = models.ForeignKey('recipe', null = False, on_delete= models.CASCADE, verbose_name="ID блюда")
    complexity = models.IntegerField(null = False,
                                     verbose_name="Сложность приговления по 5 бальной шкале")
    cooking_time = models.IntegerField(null=False,
                                     verbose_name="Время приготовления в секундах")
    meal = models.ForeignKey('meal',
                             null=False, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "типизации"
        verbose_name = 'типизация'
        ordering = ['-recipe_id']

    def __str__(self):
        return self.recipe_id
class meal(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, null=False,
                                      verbose_name="Название трапезы")
    models.CharField(max_length=200, null=False, verbose_name="Название и кол-во одного ингрижиента блюда")

    class Meta:
        verbose_name_plural = "трапезы"
        verbose_name = 'трапеза'
        ordering = ['-type']

    def __str__(self):
        return self.type



class comments(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_id = models.ForeignKey('recipe', null=False, on_delete=models.CASCADE, verbose_name="ID блюда")
    user = models.ForeignKey(AdvUser,on_delete = models.CASCADE, null = True )
    datatime = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата время")
    text = models.CharField(max_length=200,null = False,verbose_name="Сам коментарий")
