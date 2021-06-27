from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import *
from accounts.models import *
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
from . import services


@register.filter
def get_range(value):
    return range(value)


def home_page(request):
    recipe_type = ''
    if request.method == 'POST':
        form = FilteringRecipes(request.POST)
        if form.is_valid():
            if form.cleaned_data['selection_meal'] == 'Завтрак':
                recipe_type = 'Завтрак'
            elif form.cleaned_data['selection_meal'] == 'Обед':
                recipe_type = 'Обед'
            elif form.cleaned_data['selection_meal'] == 'Ужин':
                recipe_type = 'Ужин'
            elif form.cleaned_data['selection_meal'] == 'Напиток':
                recipe_type = 'Напиток'
            elif form.cleaned_data['selection_meal'] == 'Десерт':
                recipe_type = 'Десерт'
    else:
        form = FilteringRecipes()
    if recipe_type == '':
        all_recipe = Recipe.objects.order_by('id')
        all_rating = Rating.objects.order_by('id')
        title = "Все рецепты"
    else:
        all_recipe = Recipe.objects.filter(meal_type=recipe_type)
        all_rating = Rating.objects.order_by('id')
        if recipe_type == 'Ужин' or recipe_type == 'Обед' or recipe_type == 'Десерт':
            title = "Все " + str(recipe_type) + "ы"
        elif recipe_type == 'Напиток':
            title = "Все Напитки"
        else:
            title = "Все " + str(recipe_type) + "и"
    context = {
        'info': "Выберите категорию для фильтрации поиска:",
        'title': title,
        'heading': title,
        'all_recipe': all_recipe,
        'all_rating': all_rating,
        'form': form,
    }
    return render(request, "main/index.html", context)


def get_one_recipe(request, id_recipe):

    def rounding_up_hours(minutes):
        if minutes < 60:
            return 0
        else:
            return round(minutes/60)

    try:
        one_recipe = Recipe.objects.get(id = id_recipe)
    except Exception:
        return redirect("/error.html")
    #нужно получить коментарий
    coment_recipe = Comments.objects.filter(recipe_id = id_recipe)
    ingredients = Ingredients.objects.filter(recipe_id = one_recipe)
    try:
        user = AdvUser.objects.get(id = request.user.id)
        favorite_status = FavoriteDishes.objects.get(user = user, recipe_id = one_recipe)

    except Exception:
        favorite_status = None

    def get_rating():
        rating = Rating.objects.filter(recipe_id = one_recipe)
        count = 0
        all = 0
        for a in rating:
            all += int(a.rating)
            count += 1
        try:
            here_rating = Rating.objects.get(recipe_id = one_recipe, user = user)
        except Exception:
            here_rating = "zero"
        if count == 0:# Это нужно чтобы он не поделил на ноль
            return {'rating': 0,
                    'here_rating': here_rating,
                    'count': str(count),
                    }
        else:
            return {'rating':str(round(all/count,2)),
                    'here_rating':here_rating,
                    'count':str(count),
                    }

    context = {
        'autor':str(one_recipe.user.username),
        'heading': str(one_recipe.name),
        'title':  str(one_recipe.name),
        'text':str(one_recipe.text).replace('',''),
        'video_url':str(one_recipe.url_video),
        'images':one_recipe.image,
        'comments':coment_recipe,
        'id_recipe':str(id_recipe),
        'user': request.user, #id пользоватля, который запрашивает страницу
        'complexity':one_recipe.complexity,
        'hours':rounding_up_hours(one_recipe.cooking_time),
        'minutes':int(one_recipe.cooking_time)%60,
        'ingredients':ingredients,
        'favorite_status':favorite_status,
        'meal':str(one_recipe.meal_type),
        'rating':get_rating(),
    }
    return render(request, "main/resipe.html", context)
@csrf_exempt
def add_coment(request, id_recipe):
    user = AdvUser.objects.get(id = request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    text = request.POST.get('text_coment')
    coment = Comments(recipe_id = one_recipe,user = user,text = text )
    coment.save()
    user = AdvUser.objects.get(id=request.user.id)
    #Получаем его
    return render(request, "main/coment.html", {'coment':coment,
                                                'id_recipe':id_recipe,
                                                'user':user,
                                                })


@csrf_exempt
def delete_coment(request, id_coment, id_recipe):
    one_coment = Comments.objects.get(id = id_coment)
    if request.user.id == one_coment.user.id:
        one_coment.delete()
    return HttpResponse(status = 200)



def add_favorite(request, id_recipe):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    favorite_recipe = FavoriteDishes(user = user, recipe_id = one_recipe )
    favorite_recipe.save()
    return redirect("/recipe/" + str(id_recipe))


def delete_favorite(request, id_recipe):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    favorite_recipe = FavoriteDishes.objects.get(user = user, recipe_id = one_recipe )
    favorite_recipe.delete()
    return redirect("/recipe/" + str(id_recipe))


def push_rating(request, id_recipe, rating):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    # пробуем получить о обновить
    try:
        buffer = Rating.objects.get(user=user, recipe_id = one_recipe)
        buffer.rating = str(rating)
        buffer.save()

    except Exception:
        buffer = Rating(user=user, recipe_id=one_recipe, rating = str(rating))
        buffer.save()

    return redirect("/recipe/" + str(id_recipe))


def add_page(request):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    context = {
        'title':'Добавить рецепт',
        'meal':['Завтрак', 'Обед','Ужин','Напиток','Десерт'],
        'count_ingredients':0,
        'hours':0,
        'minutes':0,
    }
    return render(request, "main/add_recipe.html", context)


@csrf_exempt
def add_ricipe(request):
    if not request.user.is_authenticated:
        return redirect("/error.html")

    check = services.checking_data_registration(request)
    check_recip_recult = check.recipe_check() #возврощает old_result error как словарь

    if len(check_recip_recult.get('error')) != 0:
        old_ingredients = check.check_ingredients_for_error() #словарь
        context = {
            'title': 'Добавить рецепт',
            'meal': ['Завтрак', 'Обед', 'Ужин', 'Напиток', 'Десерт'],
        }

        return render(request, "main/add_recipe.html",{**context, **old_ingredients, **check_recip_recult} )

    registration = services.data_normalization_during_registration(request)
    #добовляем сам рецепт
    one_recipe = Recipe(name = registration.name(), user = registration.user(),
                        public = registration.public(), url_video = registration.url_video(),
                        text = registration.text(), meal_type = registration.meal_type(),
                        image = registration.image(),complexity = registration.complexity(),
                        cooking_time = registration.cooking_time(),
                        )
    one_recipe.save()
    # добоаляем ингридиенты
    registration.add_ingredients(one_recipe)

    return redirect("/recipe/" + str(one_recipe.id))


def error(request):
    return render(request, "main/error.html")