"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView

from main import views, json_views
from main.forms import RegistrationForm
from simple_votings import settings

handler403 = views.e_handler403

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index_page, name='index'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'pagename': 'Авторизация'
            }
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('votings/', views.votings_list_page, name='votings'),

    path('voting/<int:voting_id>/', views.voting_page, name='voting'),
    path('voting/<int:voting_id>/add_favourite/', json_views.add_favourite, name='api-add_favourite'),
    path('voting/<int:voting_id>/delete_favourite/', json_views.delete_favourite, name='api-delete_favourite'),
    path('voting/<int:voting_id>/cancel_vote/', json_views.cancel_vote, name='api-cancel_vote'),
    path('voting/<int:voting_id>/vote/', json_views.vote, name='api-vote'),

    path('voting/<int:voting_id>/edit/', views.edit_voting_page, name='edit_page'),
    path('voting/<int:voting_id>/edit/<str:anchor>', views.edit_voting_page, name='edit_page-anchor'),

    path('voting/<int:voting_id>/edit/main_settings/', json_views.edit_main_settings, name='api-edit_main_settings'),
    path('voting/<int:voting_id>/edit/add_vote_variant/', json_views.add_vote_variant, name='api-add_vote_variant'),
    path('voting/<int:voting_id>/edit/save_vote_variant/', json_views.save_vote_variant, name='api-save_vote_variant'),
    path('voting/<int:voting_id>/edit/delete_vote_variant/', json_views.delete_vote_variant,
         name='api-delete_vote_variant'),
    path('voting/<int:voting_id>/edit/reload/', json_views.reload_edit_forms, name='api-reload_edit_forms'),
    path('voting/<int:voting_id>/edit/upload_image/', json_views.vote_upload_image, name='api-vote_upload_image'),
    path('voting/<int:voting_id>/edit/delete_image/', json_views.voting_delete_image, name='api-delete_voting_image'),

    path('accounts/register/',
         RegistrationView.as_view(form_class=RegistrationForm),
         name='django_registration_register'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/forgotten_password.html"), name="password_reset"),
    path("accounts/password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/reset_done.html"), name="password_reset_done"),
    path("accounts/password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/reset_confirm.html"), name="password_reset_confirm"),
    path("accounts/password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/reset_complete.html"), name="password_reset_complete"),
    url(r'^password/change/$', auth_views.PasswordChangeView.as_view(template_name="registration/change_password.html"), name='password_change'),
    url(r'^password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name="registration/change_password_done.html"),
        name='password_change_done'),
    path('add/', views.add, name='add'),
    path('favorites/<int:profile_id>', views.favorites_page, name='favorites'),
    path('history/', views.history_page, name='history'),
    path('my_votings/<int:profile_id>/', views.my_votings_page, name='my_votings'),
    path('voting/<int:id>/add_complain', views.AddComplaints, name='complaints_add'),
    path('my_complaints/', views.complaint, name='my_complaints'),
    path('profile/<int:profile_id>/', views.user_profile, name='user_profile'),
    path('profile/<int:profile_id>/edit_profile/', views.redact_profile, name='redact_profile'),
    path('profile/<int:profile_id>/edit_profile/upload_image/', json_views.profile_upload_image,
         name='api-profile_upload_image'),
    path('folover/', views.folover, name='my_folover'),
    path('folovers/', views.folovers, name='my_folovers'),
    path('users/', views.ListUsers, name='user'),
    path('search/', views.search_page, name='search_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
