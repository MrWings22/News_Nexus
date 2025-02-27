from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('jj', views.Indexpage,  name="Indexpage"),
    path('', views.Homepage,  name="Homepage"),
    path('article/<int:article_id>', views.articledetail, name='articledetail'),
    path('contact/', views.contactus, name='contactus'),
    path('loginemail/', views.loginemail, name='loginemail'),
    path('register/', views.register, name='register')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
