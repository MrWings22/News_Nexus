from .models import Article
from .models import Comment

def breaking_news_processor(request):
    breakingnews = Article.objects.filter(breaking_news=True).first()
    return {'breakingnews': breakingnews}

def bad_comment_count(request):
    if request.path.startswith('/admin/'):
        
        count = Comment.objects.filter(toxicity_score__gt=0.7, is_new_inappropriate=True).count()
        return {'bad_comment_count': count}
    return {}