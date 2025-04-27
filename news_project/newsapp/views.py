from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleImages, CustomUser, Comment, Category, CustomUser , ArticleTags, Tags
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm
import re
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import json
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm  # if you're using a custom form
from django.contrib.auth.views import PasswordResetView
from django.http import StreamingHttpResponse
from django.core.mail import send_mail, BadHeaderError
from gtts import gTTS
import io
from .models import Category, Subscriber
from django.http import HttpResponse
import random
import time
from django.core.paginator import Paginator
from .utils.perspective import analyze_comment
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timesince import timesince

# def Login(request):
#     if request.method == "POST":
#         login_method = request.POST.get("login_method")  # 'email' or 'phone'
#         password = request.POST.get("password")
#         user = None

#         if login_method == "email":
#             email = request.POST.get("email")
#             try:
#                 user = CustomUser.objects.get(email=email)
#                 if not user.check_password(password):
#                     user = None
#             except CustomUser.DoesNotExist:
#                 user = None
#         else:
#             phone = request.POST.get("phone")
#             try:
#                 user = CustomUser.objects.get(phone=phone)
#                 if not user.check_password(password):
#                     user = None
#             except CustomUser.DoesNotExist:
#                 user = None

#         if user is not None:
#             login(request, user)
#             if user.last_login is None:
#                 messages.success(request, f"Welcome, {user.username}! Login successful.")
#             else:
#                 messages.success(request, f"Welcome back, {user.username}! Login successful.")
#             return redirect("Homepage")
#         else:
#             messages.error(request, "Invalid email/phone or password.")

#     return render(request, "login.html")

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
                else:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
            except CustomUser.DoesNotExist:
                user = None
        else:
            phone = request.POST.get("phone")
            try:
                user = CustomUser.objects.get(phone=phone)
                if not user.check_password(password):
                    user = None
                else:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
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

@csrf_exempt  # Exempt CSRF check for this view
def google_authenticate(request):
    if request.method == 'POST':
        try:
            # Log received data for debugging
            print("Request body:", request.body)
            
            # Parse JSON data
            if not request.body:
                return JsonResponse({'success': False, 'error': 'Empty request body'}, status=400)
            
            data = json.loads(request.body)
            token = data.get('credential')
            if not token:
                return JsonResponse({'success': False, 'error': 'Missing credential token'}, status=400)
            
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            if idinfo['aud'] != settings.GOOGLE_CLIENT_ID:
                return JsonResponse({'success': False, 'error': 'Invalid client ID'}, status=400)
            
            # Get user info
            email = idinfo['email']
            name = idinfo.get('name', '')
            if not name:
                # Use email prefix as username if name not provided
                name = email.split('@')[0]
                
            # Check if user exists, create if not
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={'username': name}
            )
            if created:
                user.set_unusable_password()  # Better than setting password=None
                user.save()
            
            # Log in the user
            login(request, user)
            return JsonResponse({'success': True, 'redirect': 'Homepage'})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
        except ValueError as e:
            return JsonResponse({'success': False, 'error': f'Token validation error: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Google authentication error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    # Handle GET requests (for completeness)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def PostLoginRedirect(request):
    return redirect('Homepage') # Redirect to homepage after login

def Indexpage(request):
    return render(request, 'index.html')

def Homepage(request):
    print(f"User is authenticated: {request.user.is_authenticated}")
    shoppings = Category.objects.filter(category_name="shopping").first()
    sports = Category.objects.filter(category_name="sports").first()
    politics = Category.objects.filter(category_name="politics").first()
    entertainment = Category.objects.filter(category_name="entertainment").first()
    latestnews = Article.objects.order_by('-created_at').exclude(category=shoppings).first()
    topfivenews = Article.objects.order_by('-created_at').exclude(pk=latestnews.pk).exclude(category=shoppings)[:5]
    
    

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
    displayed_article_ids = set(news.pk for news in topfivenews)

    if latestnews:
        displayed_article_ids.add(latestnews.pk)

    shoppingnews = Article.objects.filter(category=shoppings).order_by('-created_at')[:5]
    sportsnews = Article.objects.filter(category=sports).exclude(pk=latestnews.pk).exclude(pk__in=displayed_article_ids).order_by('-created_at')[:3]
    politicsnews = Article.objects.filter(category=politics).exclude(pk=latestnews.pk).exclude(pk__in=displayed_article_ids).order_by('-created_at')[:3]
    entertainmentnews = Article.objects.filter(category=entertainment).exclude(pk=latestnews.pk).exclude(pk__in=displayed_article_ids).order_by('-created_at')[:3]


    displayed_article_ids.update(shoppingnews.values_list('pk', flat=True))
    displayed_article_ids.update(sportsnews.values_list('pk', flat=True))
    displayed_article_ids.update(politicsnews.values_list('pk', flat=True))
    displayed_article_ids.update(entertainmentnews.values_list('pk', flat=True))

    othernews = Article.objects.exclude(pk__in=displayed_article_ids).order_by('-created_at')

    return render(request, 'home.html', {'latestnews': latestnews ,
                                         'latestnews_images': latestnews_images,
                                         'topfivenews': topfivenews,
                                         'comments': comments,
                                         'form': form,
                                         'shoppingnews': shoppingnews,
                                         'sportsnews': sportsnews,
                                         'politicsnews': politicsnews,
                                         'entertainmentnews': entertainmentnews,
                                         'othernews': othernews,
                                         })




def articledetail(request, article_id):
    article = Article.objects.get(article_id=article_id)
    tags = Tags.objects.filter(articletags__article=article)
    article.views += 1
    article.save(update_fields=['views'])

    article_images = ArticleImages.objects.filter(article=article)
    related_news = Article.objects.filter(category=article.category).exclude(article_id=article.article_id).order_by('-created_at')
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    related_news_images = {
        news.article_id: ArticleImages.objects.filter(article=news).first()
        for news in related_news
    }

    
    return render(request, 'detail-page.html', {'article': article, 'article_images': article_images, 'related_news':related_news, 'related_news_images': related_news_images, 'comments':comments, 'tags': tags})

def contactus(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})

def loginemail(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration.html')

def weatherpage(request):
    return render(request, 'weather.html')


def Searchresult(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    

    if query:
        articles = Article.objects.filter(
            Q(head_line__icontains=query) |
            Q(category__category_name__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        articles = Article.objects.all().order_by('-created_at')

    paginator = Paginator(articles, 6)  # 6 articles per page
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if AJAX request
        articles_data = [
            {
                'id': article.article_id,
                'head_line': article.head_line,
                'description': article.description,
                'image_url': article.articleimages_set.first().image.url if article.articleimages_set.exists() else None
            }
            for article in page_obj
        ]
        return JsonResponse({'articles': articles_data, 'has_next': page_obj.has_next()})

    return render(request, 'search_results.html', {'articles': page_obj, 'query': query})



@login_required
@csrf_exempt
def add_comment(request, article_id):
    print("add_comment called with article_id:", article_id)
    if request.method == "POST":
        print("POST data:", request.POST)
        article = get_object_or_404(Article, article_id=article_id)

        comment_text = request.POST.get('comments', '')
        
        # Analyze toxicity of the comment
        score = analyze_comment(comment_text)
        
        if score is not None:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.toxicity_score = score
                comment.is_new_inappropriate = True
                comment.save()

                if score >= 0.7:
                    # If the comment is toxic, save it as an inappropriate comment
                    user_profile_pic_url = ''
                    if request.user.profile_pic:
                        user_profile_pic_url = request.build_absolute_uri(request.user.profile_pic.url)

                    return JsonResponse({
                        'status': 'rejected', 
                        'message': 'Your comment seems inappropriate!',
                        'username': request.user.username,
                        'created_at': timesince(comment.created_at) + " ago",  # Adjusted created_at for rejected comments
                        'user_image': user_profile_pic_url,
                    })
                
                user_profile_pic_url = ''
                if request.user.profile_pic:
                    user_profile_pic_url = request.build_absolute_uri(request.user.profile_pic.url)
                comment_count = Comment.objects.filter(article=article).count()

                return JsonResponse({
                    'success': True,
                    'username': request.user.username,
                    'comment': comment.comments,
                    'created_at': timesince(comment.created_at) + " ago", 
                    'comment_count': comment_count,
                    'user_image': user_profile_pic_url,
                })
            else:
                print("Form errors:", form.errors)
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to analyze comment.'})
        
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
            return render(request, 'profile.html',context)
        
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

def categorypage(request):
    category_name = request.GET.get('category', None)
    categories = Category.objects.all()
    if category_name:
        category = get_object_or_404(Category, category_name=category_name)
        articles = Article.objects.filter(category=category).order_by('-created_at')
    else:
        articles = Article.objects.all().order_by('-created_at')

    return render(request, 'categorysort.html', {'articles': articles, 'category_name': category_name, 'categories': categories})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['email']  # optional
            phone = form.cleaned_data.get('phone', 'No phone number provided')

            # Format the email content
            full_message = f"Name: {name}\nEmail: {sender_email}\nPhone: {phone}\n\nMessage:\n{message}"


            # Use EmailMessage to set the Reply-To header
            email = EmailMessage(
                subject=subject,
                body=full_message,
                from_email=f"NewsNexus {settings.EMAIL_HOST_USER}",
                to=['itzmealbinthomas@gmail.com'],  # Receiver
                headers={'Reply-To': sender_email}  # Allows replying directly to the sender
            )

            email.send(fail_silently=False)
            return render(request, 'contact_success.html')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


#password resent view setup
class CustomPasswordResetView(PasswordResetView):
    email_subject_template_name = "registration/password_reset_subject.txt"
    def get_email_context(self, context):
        context = super().get_email_context(context)
        context['domain'] = settings.DEFAULT_DOMAIN  # Override the domain here
        return context
    
def text_to_speech(request, article_id):
    """Convert text to speech and stream the audio without saving."""
    article = Article.objects.get(article_id=article_id)
    
    tts = gTTS(text=article.description, lang='en', slow=False)  # Adjust speed
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    
    return StreamingHttpResponse(audio_stream, content_type="audio/mpeg")


# Subscribe view
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        category_ids = request.POST.getlist("categories")  # Fetch selected category IDs

        if not category_ids:
            messages.error(request, "Please select at least one category.")
            return redirect("newsletter")

        # Get or create subscriber
        subscriber, created = Subscriber.objects.get_or_create(email=email)

        # Get existing subscribed categories
        existing_categories = set(subscriber.categories.all())
        selected_categories = set(Category.objects.filter(category_id__in=category_ids))

        # Determine new categories to add
        new_categories = selected_categories - existing_categories
        already_subscribed = selected_categories & existing_categories  # Categories already subscribed

        if not new_categories:  
            # If all selected categories are already subscribed
            messages.info(request, f"You are already subscribed to the selected categories.")
            return redirect("newsletter")

        # Add only new categories
        for category in new_categories:
            subscriber.categories.add(category)

        # Send confirmation email only for newly added categories
        category_list = ", ".join(category.category_name for category in new_categories)
        subject = "Newsletter Subscription Update"
        message = f"Dear Subscriber,\n\nYou have successfully subscribed to the following new categories:\n\n{category_list}\n\nStay tuned for updates!"
        from_email = "your-email@gmail.com"  # Update this
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, f"Subscription updated! You have been subscribed to new categories: {category_list}.")
        return redirect("newsletter")

    categories = Category.objects.all()
    return render(request, "newsletter.html", {"categories": categories})

# Subscribe view

def newsletter_view(request):
    categories = Category.objects.all()
    return render(request, "newsletter.html", {"categories": categories})




# Unsubscribe view
def unsubscribe(request):
    email = request.GET.get('email')
    if email:
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            return HttpResponse("You have successfully unsubscribed.")
        except Subscriber.DoesNotExist:
            return HttpResponse("Email not found.")
    return HttpResponse("Invalid request.")

#otp verification setup
otp_store = {}
#Temporary dictionary on your running Django server to store OTPs. In production, use a database or cache.
@csrf_exempt
def send_otp(request):
    data = json.loads(request.body)
    email = data.get('email')
    otp = str(random.randint(100000, 999999))
    
    # ✅ Store OTP in session
    request.session[f'otp_{email}'] = otp

    send_mail(
        subject="Your NewsNexus OTP",
        message=f"""
    NewsNexus OTP Verification
    --------------------
    Hello,

    Your OTP for registration is: {otp}

    - NewsNexus Team
    """,
        from_email="youremail@example.com",
        recipient_list=[email],
        fail_silently=False
    )
    return JsonResponse({'success': True})

# @csrf_exempt  Cross-Site Request Forgery.
# Django uses CSRF tokens to protect users from malicious forms or scripts trying to perform actions on their behalf. use this if not in localhost.
@csrf_exempt
def verify_otp(request):
    data = json.loads(request.body)
    email = data.get('email')
    entered_otp = data.get('otp')
    stored_otp = request.session.get(f'otp_{email}')

    if entered_otp == stored_otp:
        return JsonResponse({'verified': True})
    return JsonResponse({'verified': False})

@staff_member_required
def view_inappropriate_comments(request):
    bad_comments = Comment.objects.filter(toxicity_score__gte=0.7).select_related('user', 'article').order_by('-created_at')
    Comment.objects.filter(is_new_inappropriate=True, toxicity_score__gt=0.5).update(is_new_inappropriate=False)
    return render(request, 'view_innappropriate_comments.html', {'bad_comments': bad_comments})



