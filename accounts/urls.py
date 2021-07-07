from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('profile/change/', ChangeUserInfoView.as_view(template_name='accounts/profile_change.html'), name='profile_change'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('password_change/',
         AccountsPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/',
         PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                   subject_template_name='accounts/reset_subject.txt',
                                   email_template_name='accounts/reset_email.txt',
                                   success_url='/accounts/password_reset/done/'),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='accounts/email_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/confirm_password.html',
         success_url='/accounts/reset/done/'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_confirmed.html'),
         name='password_reset_camplete'),
]

urlpatterns += staticfiles_urlpatterns()