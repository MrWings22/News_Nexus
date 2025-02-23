from django.shortcuts import render
from .models import Article, ArticleImages

def Indexpage(request):
    return render(request, "index.html")

def Homepage(request):
    latestnews = Article.objects.order_by('-created_at').first()
    topfivenews = Article.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'latestnews': latestnews ,'topfivenews': topfivenews})
def Detailedpage(request):
    return render(request, "detail-page.html")


    