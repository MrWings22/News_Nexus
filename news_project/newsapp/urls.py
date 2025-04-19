from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import contact_view
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from .views import CustomPasswordResetView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('index/', views.Indexpage,  name="Indexpage"),
    path('', views.Homepage,  name="Homepage"),
    path('article/<int:article_id>', views.articledetail, name='articledetail'),
    path('login/', views.Login, name='login'),
    path('register/', views.Registration, name='register'),
    path('google-authenticate/', views.google_authenticate, name='google_authenticate'),
    path('logout/', views.Logout, name='logout'),
    path('searchresult/', views.Searchresult, name='searchresults'),
    path('profile/', views.profile, name='profile'),
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),
    path('category/', views.categorypage, name='categorypage'),
    path('weather/', views.weatherpage, name='weather'),
    path('contact/', contact_view, name='contact'),
    path(
        "password_reset/",
        PasswordResetView.as_view(template_name="password_reset.html", extra_context={"view_name": "password_reset"}),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(template_name="password_reset.html", extra_context={"view_name": "password_reset_done"}),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", extra_context={"view_name": "password_reset_confirm"}),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="password_reset_confirm.html", extra_context={"view_name": "password_reset_complete"}),
        name="password_reset_complete",
    ),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path('tts/<int:article_id>/', views.text_to_speech, name='text_to_speech'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path("newsletter/", views.newsletter_view, name="newsletter"),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('admin-inappropriate-comments/', views.view_inappropriate_comments, name='inappropriate_comments'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
