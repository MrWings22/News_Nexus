from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.Indexpage,  name="Indexpage"),
    path('', views.Homepage,  name="Homepage"),
    path('article/<int:article_id>', views.articledetail, name='articledetail'),
    path('contact/', views.contactus, name='contactus'),
    path('login/', views.Login, name='login'),
    path('register/', views.Registration, name='register'),
    path('logout/', views.Logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
