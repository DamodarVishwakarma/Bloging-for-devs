from django.urls import path
from django.views.generic import TemplateView
from .views import ActivateAccount, SignUpView, contact, UserProfileView
from django.contrib.auth import views as auth_views
from core.views import DocumentView

app_name='core'

urlpatterns = [
    path('join/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    path('login/', auth_views.LoginView.as_view(next_page='core:home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),

    # Change Password
    path('change-password/', auth_views.PasswordChangeView.as_view( template_name='core/change-password.html', success_url='/'), name='change_password'),

    # Forget Password
    path('password-reset/', auth_views.PasswordResetView.as_view( template_name='core/password-reset/password_reset.html', subject_template_name='core/password-reset/password_reset_subject.html', email_template_name='core/password-reset/password_reset_email.html', success_url='/login/' ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='core/password-reset/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name='core/password-reset/password_reset_confirm.html' ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view( template_name='core/password-reset/password_reset_complete.html' ), name='password_reset_complete'),
    
    # Main Page
    path('about/', TemplateView.as_view(template_name='commons/about.html'), name='about'),
    path("contact/", contact, name="contact_us"),
    path('', DocumentView.as_view(), name='home')
]
