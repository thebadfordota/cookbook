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
            if not (len(name_count) >= 3 and len(name_count) <=40) :
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
                self.old_result['url_video'] =  "https://www.youtube.com/embed/" + str(url[1])
        except:
            return "NULL"

    def check_text(self):
        try:
            text = self.request.POST.get('text')
            text_count = re.findall(r"[А-яA-z]{1}", text)
            if len(text_count) < 50 or len(text_count) > 4000:
                1/0

            self.old_result['text'] = text
        except Exception:
            self.error.append("Недопустимое описание рецепта, минимальное кол-во символов 50 максимальное 4000")

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
            id_name = 'N' + str(a)
            id_value = 'V' + str(a)
            if name != "" and value != "":
                ingredients.append({'id_name':id_name,'name': name,
                                    'id_value':id_value,'value': value})
                len += 1

            else:
                break
        if len == 0:
            self.error.append("Минимальное кол-во ингридентов одна ")
        else:
            len -= 1
        new_input = []
        for a in range(len+1, 30):
            new_input.append({'id_tr':"T" + str(a),
                              'id_name':'N' + str(a),
                              'id_value':'V' + str(a)})

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
            value = self.request.POST.get('V' + str(a))
            if name != "" and value != "":
                ingredients = Ingredients(recipe_id=one_recipe, name=name, value=value)
                ingredients.save()
            else:
                break