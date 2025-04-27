from .models import Article
from .models import Comment
from .models import Category

def breaking_news_processor(request):
    breakingnews = Article.objects.filter(breaking_news=True).first()
    return {'breakingnews': breakingnews}

def bad_comment_count(request):
    if request.path.startswith('/admin/'):
        
        count = Comment.objects.filter(toxicity_score__gt=0.7, is_new_inappropriate=True).count()
        return {'bad_comment_count': count}
    return {}

def user_profile_context(request):
    if request.user.is_authenticated:
        return {
            'user_username': request.user.username,
            'user_email': request.user.email,
            'user_profile_pic': request.user.profile_pic.url if request.user.profile_pic else None
        }
    return {}
def category_list(request):
    categories = Category.objects.all()
    return {'categories': categories} 