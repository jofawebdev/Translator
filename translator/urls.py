from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from translator import views as translator_views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('register/', translator_views.register, name='register'),
    
    # Profile display and update views
    path('profile/', translator_views.profile, name='profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Translation history view for logged-in users
    path('history/', translator_views.translation_history, name='translation_history'),

    path('history/delete/<int:translation_id>/', translator_views.delete_translation, name='delete_translation'),
]