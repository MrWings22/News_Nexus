from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('jj', views.Indexpage,  name="Indexpage"),
    path('', views.Homepage,  name="Homepage"),
    path('article/(?P<article_id>[0-9]+)/\Z', views.articledetail, name='articledetail'),
    path('article_images/(?P<article_id>[0-9]+)/\Z', views.articledetail, name='articledetail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
