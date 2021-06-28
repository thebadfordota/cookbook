from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import *
from accounts.models import *
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
from . import services
from PIL import Image


@register.filter
def get_range(value):
    return range(value)


def home_page(request):
    recipe_type = ''
    complexity_type = ''
    cooking_time_type = ''
    if request.method == 'POST':
        form = FilteringRecipes(request.POST)
        if form.is_valid():
            if not form.cleaned_data['selection_meal'] == 'Все категории':
                recipe_type = form.cleaned_data['selection_meal']
            if not form.cleaned_data['selection_complexity'] == '6':
                complexity_type = form.cleaned_data['selection_complexity']
            if not form.cleaned_data['selection_cooking_time'] == '9':
                cooking_time_type = form.cleaned_data['selection_cooking_time']
    else:
        form = FilteringRecipes()
    if recipe_type == '':
        all_recipe = Recipe.objects.order_by('id')
        title = "Все рецепты"
    else:
        all_recipe = Recipe.objects.filter(meal_type=recipe_type)
        if recipe_type == 'Ужин' or recipe_type == 'Обед' or recipe_type == 'Десерт':
            title = "Все " + str(recipe_type) + "ы"
        elif recipe_type == 'Напиток':
            title = "Все Напитки"
        else:
            title = "Все " + str(recipe_type) + "и"
    if not complexity_type == '':
        all_recipe = all_recipe.filter(complexity=int(complexity_type))
    if not cooking_time_type == '':
        all_recipe = all_recipe.filter(cooking_time__lte=int(cooking_time_type))
    all_rating = Rating.objects.order_by('id')
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
    get_one_recipe = services.get_one_recipe(request, id_recipe)
    return get_one_recipe.get()

def update_recipe(request, id_recipe):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
    except:
        return redirect("/error.html")

    if one_recipe.user != request.user:
        return redirect("/error.html")

    check = services.checking_data_registration(request)
    check_recip_recult = check.update_recipe_check() #возврощает old_result error как словарь
    old_ingredients = check.check_ingredients_for_error()
    if len(check_recip_recult.get('error')) != 0:
         #словарь
        context = {

            'title': 'Редактировать',
            'meal': ['Завтрак', 'Обед', 'Ужин', 'Напиток', 'Десерт'],
            'action':'/recipe/update_recipe/'+str(one_recipe.id),
        }

        return render(request, "main/add_recipe.html",{**context, **old_ingredients, **check_recip_recult} )

    registration = services.data_normalization_during_registration(request)
    #добовляем сам рецепт
    one_recipe.name = registration.name()
    one_recipe.public = public = registration.public()
    one_recipe.url_video = registration.url_video()
    one_recipe.text = registration.text()
    one_recipe.meal_type = registration.meal_type()
    one_recipe.complexity = registration.complexity()
    one_recipe.cooking_time = registration.cooking_time()
    try:
        img = Image.open(request.FILES['image'])
        for a in img.size:
            if (a < 300) and (a > 3000):
                1 / 0
        one_recipe.image = request.FILES['image']
    except Exception:
        pass

    one_recipe.save()

    # добоаляем ингридиенты
    for a in Ingredients.objects.filter(recipe_id = one_recipe):
        buffer = Ingredients.objects.get(id = a.id)
        buffer.delete()

    registration.add_ingredients(one_recipe)

    return redirect("/recipe/" + str(one_recipe.id))

def delete_recipe(request, id_recipe):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
    except:
        return redirect("/error.html")

    if one_recipe.user != request.user:
        return redirect("/error.html")
    one_recipe.delete()
    return redirect("/")
@csrf_exempt
def edit_page(request, id_recipe):

    def check_ingredients_for_error():
        len = 0
        ingredients = []
        a = 0
        for b in Ingredients.objects.filter(recipe_id = one_recipe):
            name = b.name
            value = b.value
            id_name = 'N' + str(len)
            id_value = 'V' + str(len)
            if name != "" and value != "":
                ingredients.append({'id_name':id_name,'name': name,
                                    'id_value':id_value,'value': value})
                len += 1

            else:
                break


        len -= 1
        new_input = []
        for a in range(len+1, 30):
            new_input.append({'id_tr':"T" + str(a),
                              'id_name':'N' + str(a),
                              'id_value':'V' + str(a)})

        return {'len':len,
                'ingredients':ingredients,
                'new_input':new_input, }

    def rounding_up_hours(minutes):
        if minutes < 60:
            return 0
        else:
            return round(minutes / 60)

    if not request.user.is_authenticated:
        return redirect("/error.html")
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
    except:
        return redirect("/error.html")

    if one_recipe.user != request.user:
        return redirect("/error.html")

    if one_recipe.public == True:
        public = "checked"
    else:
        public = ""
    if one_recipe.url_video == "NULL":
        url_video = ""
    else:
        url_video = one_recipe.url_video

    old_result = {
        'name':one_recipe.name,
        'public':public,
        'url_video':url_video,
        'meal_type':one_recipe.meal_type,
        'image':one_recipe.image,
        'text': one_recipe.text,
        'hours':rounding_up_hours(one_recipe.cooking_time),
        'minutes':int(one_recipe.cooking_time) % 60,
        'complexity':one_recipe.complexity,
        'count_ingredients': 0,

    }
    context = {
        'title': 'Редактировать рецепт',
        'button_info': 'Изменить',
        'meal': ['Завтрак', 'Обед', 'Ужин', 'Напиток', 'Десерт'],
        'old_result':old_result,
        'action': '/recipe/update_recipe/' + str(one_recipe.id),
    }
    return render(request, "main/add_recipe.html", {**context,**check_ingredients_for_error()})

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


@csrf_exempt
def add_favorite(request, id_recipe):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    favorite_recipe = FavoriteDishes(user = user, recipe_id = one_recipe )
    favorite_recipe.save()
    return redirect("/recipe/" + str(id_recipe))

@csrf_exempt
def delete_favorite(request, id_recipe):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    favorite_recipe = FavoriteDishes.objects.get(user = user, recipe_id = one_recipe )
    favorite_recipe.delete()
    return redirect("/recipe/" + str(id_recipe))

@csrf_exempt
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

@csrf_exempt
def add_page(request):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    context = {
        'title': 'Добавить рецепт',
        'button_info': 'Добавить',
        'meal': ['Завтрак', 'Обед', 'Ужин', 'Напиток', 'Десерт'],
        'count_ingredients': 0,
        'hours': 0,
        'minutes': 0,
        'action': '/recipe/add_ricipe',

    }
    return render(request, "main/add_recipe.html", context)


@csrf_exempt
def add_ricipe(request):
    if not request.user.is_authenticated:
        return redirect("/error.html")

    check = services.checking_data_registration(request)
    check_recip_recult = check.recipe_check() #возврощает old_result error как словарь
    old_ingredients = check.check_ingredients_for_error()  # словарь
    if len(check_recip_recult.get('error')) != 0:

        context = {

            'title': 'Добавить рецепт',
            'meal': ['Завтрак', 'Обед', 'Ужин', 'Напиток', 'Десерт'],
            'action':'/recipe/add_ricipe',
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