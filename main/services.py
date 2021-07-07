from django.shortcuts import render, redirect, HttpResponse
import re
from PIL import Image
from accounts.models import *
from .models import *
class checking_data_registration:
    def __init__(self, django_request):
        self.request = None
        self.old_result = {}
        self.error = []
        self.request = django_request


    def check_name(self):
        try:
            name = self.request.POST.get('name')
            name_count = re.findall(r"[А-яA-z]{1}", name)
            if not (len(name_count) >= 3 and len(name_count) <=130) :
                #Вызаваем ошибку
                1/0
            self.old_result['name'] = name
        except Exception:
            self.error.append("Недопустимое имя блюда")

    def check_public(self):
        try:
            public = self.request.POST.get('public')
            if public == "on":
                public = True
                self.old_result['public'] = "checked"
            else:
                public = False
        except:
            public = False

    def check_url_video(self):
        try:
            url = str(self.request.POST.get('url_video'))
            url = url.split("=")
            if len(url) == 0:
                return "NULL"
            else:
                
                self.old_result['url_video'] =  self.request.POST.get('url_video')
        except:
            return "NULL"

    def check_text(self):
        try:
            text = self.request.POST.get('text')
            text_count = re.findall(r"[А-яA-z]{1}", text)
            if len(text_count) < 5 or len(text_count) > 4000:
                1/0

            self.old_result['text'] = text
        except Exception:
            self.error.append("Недопустимое описание рецепта, минимальное кол-во символов 5 максимальное 4000")

    def check_meal_type(self):
        try:
            meal_type = self.request.POST.get('meal')
            if "Завтрак Обед Ужин Напиток Десерт".find(meal_type) == -1:
                1 / 0
            self.old_result['meal_type'] = meal_type
        except:
            self.error.append("Недопустимый тип трапезы")

    def check_image(self):
        try:
            img = Image.open(self.request.FILES['image'])
            for a in img.size:
                if (a < 300) and (a > 3000):
                    1/0
        except Exception:
            self.error.append("Необходимо добавить изображение или недопустимый формат")

    def check_complexity(self):
        try:
            complexity = self.request.POST.get('complexity')
            if int(complexity) < 1 and int(complexity) > 5:
                1/0
            self.old_result['complexity'] = complexity
        except Exception:
            self.error.append("Необходимо выбрать сложность")

    def check_cooking_time(self):
        def rounding_up_hours(minutes):
            if minutes < 60:
                return 0
            else:
                return round(minutes / 60)

        def get_minutes():
            try:
                time_hour = int(self.request.POST.get('time_hour'))
            except Exception:
                time_hour = 0
            try:
                time_minutes = int(self.request.POST.get('time_minutes'))
            except Exception:
                time_minutes = 0

            if time_hour == 0:
                return time_minutes
            if time_minutes == 0:
                return time_hour * 60
            return (time_hour * 60) + time_minutes


        try:
            cooking_time = get_minutes()
            if int(cooking_time) < 5:
                1/0
            self.old_result['hours'] = rounding_up_hours(cooking_time)
            self.old_result['minutes'] = int(cooking_time) % 60
        except Exception:
            def zero_time():
                self.old_result['hours'] = 0
                self.old_result['minutes'] = 0
            zero_time()
            self.error.append("Минимальное допустимое время 5 минут")

    def update_recipe_check(self):
        self.check_name()
        self.check_public()
        self.check_url_video()
        self.check_text()
        self.check_meal_type()
        self.check_complexity()
        self.check_cooking_time()

        return {'old_result': self.old_result,
                'error': self.error, }

    def recipe_check(self):
        self.check_name()
        self.check_public()
        self.check_url_video()
        self.check_text()
        self.check_meal_type()
        self.check_image()
        self.check_complexity()
        self.check_cooking_time()

        return {'old_result':self.old_result,
                'error':self.error,}

    def check_ingredients_for_error(self):
        len = 0
        ingredients = []
        for a in range(30):
            name = self.request.POST.get('N' + str(a))
            value = self.request.POST.get('V' + str(a))
            units = self.request.POST.get('U' + str(a))
            id_name = 'N' + str(a)
            id_value = 'V' + str(a)
            id_units = 'U' + str(a)
            if name != "" and units != "":
                ingredients.append({'id_name':id_name,'name': name,
                                    'id_value':id_value,'value': value,
                                    'id_units':id_units,'units': units})
                len += 1
            else:
                break
        if len == 0:
            self.error.append("Минимальное кол-во ингридентов одна ")
            ingredients.append({'id_name': 'N0', 'name': "",
                                'id_value': 'V0', 'value': "",
                                'id_units':'U0','units': ""})
        else:
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

class data_normalization_during_registration:
    request = None
    def __init__(self,django_request):

        self.request = django_request



    def name(self):
        return self.request.POST.get('name')
    def user(self):
        return AdvUser.objects.get(id=self.request.user.id)
    def public(self):
        public = self.request.POST.get('public')
        if public == "on":
            return True
        else:
            return False
    def url_video(self):
        try:
            url = str(self.request.POST.get('url_video'))
            url = url.split("=")
            if len(url) != 0:
               return "https://www.youtube.com/embed/" + str(url[1])
        except Exception:
            return "NULL"
    def text(self):
        return self.request.POST.get('text')
    def meal_type(self):
        return self.request.POST.get('meal')
    def image(self):
        return self.request.FILES['image']
    def complexity(self):
        return self.request.POST.get('complexity')
    def cooking_time(self):
        def get_minutes():
            try:
                time_hour = int(self.request.POST.get('time_hour'))
            except Exception:
                time_hour = 0
            try:
                time_minutes = int(self.request.POST.get('time_minutes'))
            except Exception:
                time_minutes = 0

            if time_hour == 0:
                return time_minutes
            if time_minutes == 0:
                return time_hour * 60
            return (time_hour * 60) + time_minutes
        return get_minutes()
    def add_ingredients(self,one_recipe):
        for a in range(30):
            name = self.request.POST.get('N' + str(a))

            units = self.request.POST.get('U' + str(a))
            if name != "" and units != "" :
                ingredients = Ingredients(recipe_id=one_recipe, name=name, units=units)
                try:
                    value = int(self.request.POST.get('V' + str(a)))
                    value = value + 1 - 1
                    ingredients.value = value
                except Exception:
                    ingredients.value = -1
                ingredients.save()
            else:
                break

class get_one_recipe:
    request = None
    id_recipe = None
    def __init__(self, request, id_recipe):
        self.request = request
        self.id_recipe = id_recipe

    def rounding_up_hours(self,minutes):
        if minutes < 60:
            return 0
        else:
            return round(minutes/60)
    def get(self):
        def get_rating():
            rating = Rating.objects.filter(recipe_id=one_recipe)
            count = 0
            all = 0
            for a in rating:
                all += int(a.rating)
                count += 1
            try:
                here_rating = Rating.objects.get(recipe_id=one_recipe, user=user)
            except Exception:
                here_rating = "zero"
            if count == 0:  # Это нужно чтобы он не поделил на ноль
                return {'rating': 0,
                        'here_rating': here_rating,
                        'count': str(count),
                        }
            else:
                return {'rating': str(round(all / count, 2)),
                        'here_rating': here_rating,
                        'count': str(count),
                        }

        try:
            one_recipe = Recipe.objects.get(id = self.id_recipe)
        except Exception:
            return redirect("/error.html")
        #нужно получить коментарий
        coment_recipe = Comments.objects.filter(recipe_id = self.id_recipe)
        ingredients = Ingredients.objects.filter(recipe_id = one_recipe)
        try:
            user = AdvUser.objects.get(id = self.request.user.id)
            favorite_status = FavoriteDishes.objects.get(user = self.request.user, recipe_id = one_recipe)
        except Exception:
            favorite_status = None


        context = {
            'autor':str(one_recipe.user.username),
            'heading': str(one_recipe.name),
            'title':  str(one_recipe.name),
            'text':str(one_recipe.text).replace('\r\n',' <br>'),
            'video_url':str(one_recipe.url_video),
            'images':one_recipe.image,
            'comments':coment_recipe,
            'id_recipe':str(self.id_recipe),
            'user': self.request.user, #id пользоватля, который запрашивает страницу
            'complexity':one_recipe.complexity,
            'hours':self.rounding_up_hours(one_recipe.cooking_time),
            'minutes':int(one_recipe.cooking_time)%60,
            'ingredients':ingredients,
            'favorite_status':favorite_status,
            'meal':str(one_recipe.meal_type),
            'rating':get_rating(),
            'recipe':one_recipe,
            'complexity_range': range(one_recipe.complexity)
        }
        if one_recipe.public == False:
            if self.request.user != one_recipe.user:
                return redirect("/error.html")
        return render(self.request, "main/resipe.html", context)

def check_authenticated_recipe_user(request, id_recipe):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
    except:
        return redirect("/error.html")

    if one_recipe.user != request.user:
        return redirect("/error.html")

    return None

def check_authenticated_recipe(request, id_recipe):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    try:
        one_recipe = Recipe.objects.get(id=id_recipe)
    except:
        return redirect("/error.html")

    return None

def delete_coment(request, id_coment):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        one_coment = Comments.objects.get(id=id_coment)
    except Exception:
        return HttpResponse(status=400)

    if request.user.id == one_coment.user.id:
        one_coment.delete()
    return HttpResponse(status=200)

def search_in_main(request,all_recipe ):
    try:
        old_ingredients = ""
        if request.method != 'POST':
            0/0

        ingredients_for_search = str(request.POST.get('ingredients')).lower()
        if ingredients_for_search == "":
            0 / 0
        old_ingredients = ingredients_for_search
        ingredients_for_search = ingredients_for_search.split(',')
        for a in range(len(ingredients_for_search)):
            ingredients_for_search[a] = ingredients_for_search[a].strip()

        buffer = []
        for a in all_recipe:
            search_ok = True
            ingredients_str = ""
            for b in Ingredients.objects.filter(recipe_id = a):
                ingredients_str += " " + b.name.lower()
            for b in range(len(ingredients_for_search)):
                if ingredients_str.find(ingredients_for_search[b]) == -1:
                    search_ok = False
            if search_ok == True:
                buffer.append(a)
        #конец поиска по ингрилиентам
        return buffer, old_ingredients
    except Exception:
        return None, ""

def rounding_up_hours(minutes):
    if minutes < 60:
       return 0
    else:
       return round(minutes/60)


def get_rating(one_recipe, user):
    rating = Rating.objects.filter(recipe_id=one_recipe)
    count = 0
    all = 0
    for a in rating:
        all += int(a.rating)
        count += 1
    try:
        here_rating = Rating.objects.get(recipe_id=one_recipe, user=user)
        here_rating =   here_rating.rating
    except Exception:
        here_rating = "0"
    if count == 0:  # Это нужно чтобы он не поделил на ноль
        return {'rating': 0,
                'here_rating': here_rating,
                }
    else:
        return {'rating': str(round(all / count, 2)),
                'here_rating': here_rating,
                }