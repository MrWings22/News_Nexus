from django.shortcuts import render, redirect
from .models import Article

def Indexpage(request):
    return render(request, "index.html")

def Homepage(request):
    latestnews = Article.objects.order_by('-created_at').first()
    return render(request, 'home.html', {'latestnews': latestnews})

def Detailedpage(request):
    return render(request, "detail-page.html")

