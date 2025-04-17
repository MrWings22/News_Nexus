from .models import Article

def breaking_news_processor(request):
    breakingnews = Article.objects.filter(breaking_news=True).first()
    return {'breakingnews': breakingnews}
