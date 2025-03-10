from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleImages, CustomUser, Comment, Category, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm
import re
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

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
            if user.last_login is None:
                messages.success(request, f"Welcome, {user.username}! Login successful.")
            else:
                messages.success(request, f"Welcome back, {user.username}! Login successful.")
            return redirect("Homepage")
        else:
            messages.error(request, "Invalid email/phone or password.")

    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("Homepage")


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
    category_name = request.GET.get('category', None)

    if category_name:
        category = get_object_or_404(Category, category_name=category_name)
        latestnews = Article.objects.filter(category=category).order_by('-created_at').first()
        topfivenews = Article.objects.filter(category=latestnews.category).order_by('-created_at').exclude(pk=latestnews.pk)[:5]
    else:
        latestnews = Article.objects.order_by('-created_at').first()
        topfivenews = Article.objects.order_by('-created_at').exclude(pk=latestnews.pk)[:5]

    if latestnews:
        latestnews.views += 1
        latestnews.save(update_fields=['views'])

        latestnews_images = ArticleImages.objects.filter(article=latestnews) 
        comments = Comment.objects.filter(article=latestnews).order_by('-created_at')
    else:
        latestnews = []
        comment = []
        topfivenews = []
        latestnews_images =[]

    form = CommentForm()
    categories = Category.objects.all()

    return render(request, 'home.html', {'latestnews': latestnews ,'latestnews_images': latestnews_images,'topfivenews': topfivenews,'comments': comments,'form': form,'selected_category': category_name, 'categories': categories})




def articledetail(request, article_id):
    article = Article.objects.get(article_id=article_id)

    article.views += 1
    article.save(update_fields=['views'])

    article_images = ArticleImages.objects.filter(article=article)
    related_news = Article.objects.filter(category=article.category).exclude(article_id=article.article_id).order_by('-created_at')
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    related_news_images = {
        news.article_id: ArticleImages.objects.filter(article=news).first()
        for news in related_news
    }
    return render(request, 'detail-page.html', {'article': article, 'article_images': article_images, 'related_news':related_news, 'related_news_images': related_news_images, 'comments':comments})

def contactus(request):
    return render(request, 'contact.html')

def loginemail(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration.html')

def Searchresult(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        articles = Article.objects.filter(
            Q(head_line__icontains=query) |  # Search in headline
            Q(category__category_name__icontains=query)  # Search in category name
        ).distinct()
    else:
        articles = Article.objects.all()
    
    return render(request, 'search_results.html', {'articles': articles, 'query': query})


@login_required
@csrf_exempt
def add_comment(request, article_id):
    print("add_comment called with article_id:", article_id)
    if request.method == "POST":
        print("POST data:", request.POST)
        article = get_object_or_404(Article, article_id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            print("Comment saved:", comment.comments)
            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'comment': comment.comments,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def profile(request):
    # Create a context variable to track if we should show the edit form (back side)
    context = {'show_edit_form': False}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_pic = request.FILES.get('profile_pic')
        
        # Flag to track if there are validation errors
        has_errors = False
        user = request.user

        # Validate username
        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already taken!')
            has_errors = True
        
        # Validate email
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already registered!')
            has_errors = True
        
        # Validate phone
        phone_regex = r"^[6-9]\d{9}$"
        if not re.match(phone_regex, phone):
            messages.error(request, 'Invalid phone number! Enter a 10-digit number starting with 6-9.')
            has_errors = True
        
        # Validate password match
        if password or confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                has_errors = True
        
        # If there are errors, show the edit form again
        if has_errors:
            context['show_edit_form'] = True
            return render(request, 'profile.html', context)
        
        # No errors, proceed with update
        user.username = username
        user.email = email
        user.phone = phone

        # Update password if provided and matches confirmation
        if password and confirm_password and password == confirm_password:
            user.set_password(password)

        # Update profile picture if provided
        if profile_pic:
            # Delete old profile picture if it exists
            if user.profile_pic and user.profile_pic.name != 'default.jpg':
                default_storage.delete(user.profile_pic.path)
            user.profile_pic = profile_pic

        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        
        # Re-authenticate if password was changed
        if password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
        
        return redirect('profile')

    return render(request, 'profile.html', context)