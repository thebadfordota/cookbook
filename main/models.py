from django.db import models
from datetime import datetime
# Create your models here.


class recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,null = False, verbose_name="Имя блюда")
    #user(вторичный ключ)
    public = models.BooleanField()
    class Meta:
        verbose_name_plural = 'рецепты'
        verbose_name = 'рецепт'
        ordering = ['-name']

    def __str__(self):
        return self.name
class user(models.Model):
    id = models.AutoField(primary_key=True)
    fist_name = models.CharField(max_length=50,null = False, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=50, null = False,verbose_name="Фамилия пользователя")
    email = models.CharField(max_length=150,null = False, verbose_name="Электронная почта")
    admin_status = models.BooleanField()
    class Meta:
        verbose_name_plural = 'пользователи'
        verbose_name = 'пользователь'
        ordering = ['-last_name']

    def __str__(self):
        return self.last_name
class rating(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('user',
                                null = False, on_delete= models.CASCADE, verbose_name="ID пользователя")
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
    name_and_value = models.CharField(max_length=200,
                                      null = False,verbose_name="Название и кол-во одного ингрижиента блюда")
    class Meta:
        verbose_name_plural = 'ингридиенты'
        verbose_name = 'ингридиент'
        ordering = ['-name_and_value']

    def __str__(self):
        return self.name_and_value
class favorite_dishes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('user', null=False, on_delete=models.CASCADE, verbose_name="ID пользователя")
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

class description_recipe(models.Model):
    recipe_id = models.ForeignKey('recipe', null=False, on_delete=models.CASCADE, verbose_name="ID блюда")
    url_video = models.CharField(max_length=400,
                                      null = True,verbose_name="Ссылка на ютую видео",default="NUll")
    text = models.CharField( max_length=5000,null=False, verbose_name="Описание самого рецепта с ссылками на картинки")

    class Meta:
        verbose_name_plural = "описании рецептов"
        verbose_name = 'описании рецепта'
        ordering = ['-recipe_id']

    def __str__(self):
        return self.recipe_id


class comments(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_id = models.ForeignKey('recipe', null=False, on_delete=models.CASCADE, verbose_name="ID блюда")
    user = models.ForeignKey('user', null=False, on_delete=models.CASCADE, verbose_name="ID пользователя")
    datatime = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата время")
    text = models.CharField(max_length=200,
                                      null = False,verbose_name="Сам коментарий")

    class Meta:
        verbose_name_plural = "коментарии"
        verbose_name = 'коментарий'
        ordering = ['-text']

    def __str__(self):
        return self.text