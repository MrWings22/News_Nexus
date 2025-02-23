from django.urls import path
from . import views

urlpatterns = [
    path('jj', views.Indexpage,  name="Indexpage"),
    path('', views.Homepage,  name="Homepage"),
    path('jk', views.Detailedpage,  name="Detailedpage"),
   
]
