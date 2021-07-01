from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import BadSignature
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from .models import AdvUser
from .forms import ChangeUserinfoForm, RegisterUserForm
from .utilities import signer


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect("/error.html")
    user_info = AdvUser.objects.order_by('id')
    context = {
        'title': 'Профиль  пользователя',
        'heading': 'Профиль  пользователя',
    }
    return render(request, 'accounts/profile.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView) :
    model = AdvUser
    template_name = 'accounts/change_user_info.html'
    form_class = ChangeUserinfoForm
    # success_url = '/accounts/profile/'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/error.html")
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'accounts/register_user.html'
    form_class = RegisterUserForm
    # success_url = '/accounts/register/done/'
    success_url = reverse_lazy('accounts:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'accounts/register_done.html'


class AccountsPasswordChangeView(PasswordChangeView):
    # success_url = '/accounts/profile/'
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/password_change.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)