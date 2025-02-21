from django.shortcuts import render, redirect
from .models import Article, ArticleImages

def Indexpage(request):
    return render(request, "index.html")

def Homepage(request):
    latestnews = Article.objects.all()
    return render(request, 'home.html', {'latestnews': latestnews})

def Detailedpage(request):
    return render(request, "detail-page.html")

def NewsImages(request):
    images = ArticleImages.objects.all()
    return render(request, 'home.html', {'images': images})
    