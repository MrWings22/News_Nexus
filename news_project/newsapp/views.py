from django.shortcuts import render
from .models import Article, ArticleImages
from django.contrib.auth import authenticate, login, logout


# def UserLogin(request):
#     username = request.POST("username")
#     password = request.POST("password")
#     user = authenticate(request, username=username, password=password)

# def Registration(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         password = request.POST['password']
#         confirmpassword = request.POST['confirmpassword']
#         User.objects.create(username=username, email=email, phone=phone, password=password, confirmpassword=confirmpassword)

#     return render(request, 'registration.html')

def Indexpage(request):
    return render(request, "index.html")

def Homepage(request):
    latestnews = Article.objects.order_by('-created_at').first()
    topfivenews = Article.objects.order_by('-created_at').exclude(pk=latestnews.pk)[:5]
    latestnews_images = ArticleImages.objects.filter(article=latestnews) if latestnews else None
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


    