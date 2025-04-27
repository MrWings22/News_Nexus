from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name
    
class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    head_line = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0,)
    breaking_news = models.BooleanField(default=False)

    def __str__(self):
        return self.head_line
    def save(self, *args, **kwargs):
        # Ensure only one article is marked as breaking news
        if self.breaking_news:
            # Unmark all other articles as breaking news
            Article.objects.filter(breaking_news=True).exclude(article_id=self.article_id).update(breaking_news=False)
        super().save(*args, **kwargs)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comments = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    toxicity_score = models.FloatField(null=True, blank=True)
    is_new_inappropriate = models.BooleanField(default=False)
    
    def __str__(self):
        return self.comments[:20]

class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag_name
    
class ArticleTags(models.Model):
    articletag_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.article.head_line} - {self.tag.tag_name}"
        
class ArticleImages(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img/')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_name


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.email