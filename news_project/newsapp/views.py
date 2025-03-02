from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Article, ArticleImages, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re



def Login(request):
    if request.method == "POST":
        login_method = request.POST.get("login_method")  # 'email' or 'phone'
        password = request.POST.get("password")
        user = None

        if login_method == "email":
            email = request.POST.get("email")
            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    user = None
            except CustomUser.DoesNotExist:
                user = None
        else:
            phone = request.POST.get("phone")
            try:
                user = CustomUser.objects.get(phone=phone)
                if not user.check_password(password):
                    user = None
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("Homepage")
        else:
            messages.error(request, "Invalid email/phone or password.")

    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


def Registration(request):
    if request.method == "POST":
        username = request.POST['username'].strip().lower()
        email = request.POST['email'].strip().lower()
        phone = request.POST['phone'].strip()
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
    
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format! Please enter a valid email address.")
            return redirect('register')

        phone_regex = r"^[6-9]\d{9}$"
        if not re.match(phone_regex, phone):
            messages.error(request, "Invalid phone number! Enter a 10-digit number starting with 6-9.")
            return redirect('register')

        if password != confirmpassword:
            messages.error(request, "Password do not match!")
            return redirect('register')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')
        
        user = CustomUser.objects.create(username=username, email=email, phone=phone)
        user.set_password(password)
        user.save()
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Registration successfull! Welcome to NewsNexus")
            return redirect('Homepage')
        
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    
    return render(request, 'registration.html')





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


    