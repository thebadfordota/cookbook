from django.shortcuts import render, redirect
from .forms import *
from .models import *
from accounts.models import *
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
from . import services
from PIL import Image
from django.core.paginator import Paginator

#данный фильтр возврощает ноль
@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_range_without_zero(value):
    return range(1,value+1)


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
    # поиск по игридиентам
    search_result =  services.search_in_main(request, all_recipe)
    if search_result[0] != None:
        all_recipe = search_result[0]
        old_ingredients = search_result[1]
    else:
        old_ingredients = ""
    #вывод только публичных рецептов
    buffer = []
    for a in range(len(all_recipe)):
        if all_recipe[a].public == True:
            buffer.append(all_recipe[a])
    all_recipe = buffer

    #пагинация
    paginations = Paginator(all_recipe, 4)
    try:
        request_page = int(request.GET.get('page'))
        if request_page <= paginations.num_pages and (not request_page <= 0):
            page = request_page
        else:
             0/0
    except Exception:
        page = 1
    #конец пагинации

    #Записываем время и рейтинг
    for a in range(len(all_recipe)):
        all_minutes = all_recipe[a].cooking_time
        all_recipe[a].hours = services.rounding_up_hours(all_minutes)
        all_recipe[a].minutes = int(all_minutes)%60
        all_recipe[a].rating = services.get_rating(all_recipe[a], request.user)


    context = {
        'info': "Выберите категорию для фильтрации поиска:",
        'title': title,
        'heading': title,
        'all_recipe':  paginations.page(page),
        'all_rating': all_rating,
        'form': form,
        'paginations':paginations,
        'old_ingredients':old_ingredients,
    }
    return render(request, "main/index.html", context)

def view_chosen_recipes(request):
    title = 'Избранные рецепты'
    all_recipe = Recipe.objects.order_by('id')
    all_rating = Rating.objects.order_by('id')
    buffer = []
    a = FavoriteDishes.objects.filter(user = request.user)
    for a in range(len(all_recipe)):
        try:
            FavoriteDishes.objects.get(user = request.user, recipe_id = all_recipe[a])
            all_recipe[a].hours = services.rounding_up_hours(all_recipe[a].cooking_time)
            all_recipe[a].minutes = int(all_recipe[a].cooking_time) % 60
            all_recipe[a].rating = services.get_rating(all_recipe[a], request.user)
            buffer.append(all_recipe[a])
        except Exception:
            pass
    all_recipe = buffer
    context = {
        'info': "Выберите категорию для фильтрации поиска:",
        'title': title,
        'heading': title,
        'all_recipe': all_recipe,
        'all_rating': all_rating,
    }
    return render(request, "main/chosen_recipes.html", context)

def view_yours_recipe(request):
    title = 'Мои рецепты'
    all_recipe = Recipe.objects.order_by('id')
    all_rating = Rating.objects.order_by('id')
    buffer = []
    a = FavoriteDishes.objects.filter(user = request.user)
    for a in range(len(all_recipe)):
        try:
            if all_recipe[a].user == request.user:
                all_recipe[a].hours = services.rounding_up_hours(all_recipe[a].cooking_time)
                all_recipe[a].minutes = int(all_recipe[a].cooking_time) % 60
                all_recipe[a].rating = services.get_rating(all_recipe[a], request.user)
                buffer.append(all_recipe[a])
        except Exception:
            pass
    all_recipe = buffer
    context = {
        'info': "Выберите категорию для фильтрации поиска:",
        'title': title,
        'heading': title,
        'all_recipe': all_recipe,
        'all_rating': all_rating,
    }
    return render(request, "main/chosen_recipes.html", context)

def get_one_recipe(request, id_recipe):
    get_one_recipe = services.get_one_recipe(request, id_recipe)
    return get_one_recipe.get()

def update_recipe(request, id_recipe):

    if services.check_authenticated_recipe_user(request, id_recipe) != None:
        return services.check_authenticated_recipe_user(request, id_recipe)
    one_recipe = Recipe.objects.get(id=id_recipe)

    check = services.checking_data_registration(request)
    check_recip_recult = check.update_recipe_check() #возврощает old_result error как словарь
    old_ingredients = check.check_ingredients_for_error()
    if len(check_recip_recult.get('error')) != 0:
         #словарь
        context = {
            'button_info': 'Изменить',
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

    # удаляем ингридиенты
    for a in Ingredients.objects.filter(recipe_id = one_recipe):
        buffer = Ingredients.objects.get(id = a.id)
        buffer.delete()
    # добоаляем ингридиенты
    registration.add_ingredients(one_recipe)

    return redirect("/recipe/" + str(one_recipe.id))

def delete_recipe(request, id_recipe):
    if services.check_authenticated_recipe_user(request, id_recipe) != None:
        return services.check_authenticated_recipe_user(request, id_recipe)
    one_recipe = Recipe.objects.get(id=id_recipe)

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
            units = b.units
            id_name = 'N' + str(len)
            id_value = 'V' + str(len)
            id_units = 'U' + str(len)
            if name != "" and value != "":
                ingredients.append({'id_name':id_name,'name': name,
                                    'id_value':id_value,'value': value,
                                    'id_units':id_units,'units': units})
                len += 1

            else:
                break


        len -= 1
        new_input = []
        for a in range(len+1, 30):
            new_input.append({'id_tr':"T" + str(a),
                              'id_name':'N' + str(a),
                              'id_value':'V' + str(a),
                              'id_units':'U' + str(a)})

        return {'len':len,
                'ingredients':ingredients,
                'new_input':new_input, }

    def rounding_up_hours(minutes):
        if minutes < 60:
            return 0
        else:
            return round(minutes / 60)

    if services.check_authenticated_recipe_user(request, id_recipe) != None:
        return services.check_authenticated_recipe_user(request, id_recipe)

    one_recipe = Recipe.objects.get(id=id_recipe)
    #видео
    try:
        buffer = str(one_recipe.url_video)
        buffer = buffer.split("/embed/")
        one_recipe.url_video  = "https://www.youtube.com/watch?v="+buffer[1]
    except Exception:
        pass
    old_result = {
        'name':one_recipe.name,
        'public':str(one_recipe.public),
        'url_video':one_recipe.url_video,
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
    if services.check_authenticated_recipe(request, id_recipe) != None:
        return services.check_authenticated_recipe(request, id_recipe)
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
        text = request.POST.get('text_coment')
        coment = Comments(recipe_id = one_recipe,user = request.user,text = text )
        coment.save()
    except Exception:
        return redirect("/error.html")

    return render(request, "main/coment.html", {'coment':coment,
                                                'id_recipe':id_recipe,
                                                'user':request.user,
                                                })


@csrf_exempt
def delete_coment(request, id_coment, id_recipe):
    return services.delete_coment(request, id_coment)



@csrf_exempt
def add_favorite(request, id_recipe):
    if services.check_authenticated_recipe(request, id_recipe) != None:
        return services.check_authenticated_recipe(request, id_recipe)


    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
        try:
            FavoriteDishes.objects.get(user = request.user, recipe_id = one_recipe)
            return redirect("/error.html")
        except Exception:
            favorite_recipe = FavoriteDishes(user = request.user, recipe_id = one_recipe)
            favorite_recipe.save()
            return redirect("/recipe/" + str(id_recipe))
    except Exception:
        return redirect("/error.html")


@csrf_exempt
def delete_favorite(request, id_recipe):
    if services.check_authenticated_recipe(request, id_recipe) != None:
        return services.check_authenticated_recipe(request, id_recipe)
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
        favorite_recipe = FavoriteDishes.objects.get(user=request.user.id, recipe_id=one_recipe)
        favorite_recipe.delete()
    except Exception:
        return redirect("/error.html")
    return redirect("/recipe/" + str(id_recipe))

@csrf_exempt
def push_rating(request, id_recipe, rating):
    if services.check_authenticated_recipe(request, id_recipe) != None:
        return services.check_authenticated_recipe(request, id_recipe)
    one_recipe = Recipe.objects.get(id=id_recipe)

    try:
        buffer = Rating.objects.get(user=request.user, recipe_id = one_recipe)
        buffer.rating = str(rating)
        buffer.save()

    except Exception:
        buffer = Rating(user=request.user, recipe_id=one_recipe, rating = str(rating))
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
            'button_info':'Добавить',
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