from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Article(models.Model):
#     article_id = models.AutoField(primary_key=True)
#     head_line = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class Comments(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     comments = models.TextField()
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
    

# class Tags(models.Model):
#     tag_id = models.AutoField(primary_key=True)
#     tag_name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class ArticleTags(models.Model):
#     articletag_id = models.AutoField(primary_key=True)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
#     created_at  = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class ArticleImages(models.Model):
#     image_id = models.AutoField(primary_key=True)
#     image_name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='images/')
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    
      
