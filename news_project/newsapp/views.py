from django.shortcuts import render
from .models import Article, ArticleImages

def Indexpage(request):

    return render(request, "index.html")

def Homepage(request):
    latestnews = Article.objects.order_by('-created_at').first()
    topfivenews = Article.objects.order_by('-created_at').exclude(pk=latestnews.pk)[:5]
    latestnews_images = ArticleImages.objects.filter(article=latestnews) if latestnews else None
    # othernews = Article.objects.order_by('-created_at').exclude(pk=topfivenews.pk)[:5]
    return render(request, 'home.html', {'latestnews': latestnews ,'latestnews_images': latestnews_images,'topfivenews': topfivenews})

def articledetail(request, article_id):
    article = Article.objects.get(article_id=article_id)
    article_images = ArticleImages.objects.filter(article=article)
    return render(request, 'detail-page.html', {'article': article, 'article_images': article_images})

def contactus(request):
    return render(request, 'contact.html')

def loginemail(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration.html')


    