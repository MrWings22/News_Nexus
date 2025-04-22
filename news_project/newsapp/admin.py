from django.contrib import admin
from .models import Category, Article, Comment, Tags, ArticleTags, ArticleImages, CustomUser, Subscriber

class ArticlAdmin(admin.ModelAdmin):
    list_display = ['head_line', 'category', 'user', 'created_at', 'updated_at','breaking_news']
    list_filter = ['category', 'user', 'created_at', 'updated_at']
    search_fields = ['head_line', 'description', 'user__username', 'category__category_name']
    list_per_page = 10
    readonly_fields = ["views","user"]
    actions = ['mark_as_breaking_news']
    fields = ['head_line', 'description', 'category', 'user', 'views', 'breaking_news']

    def save_model(self, request, obj, form, change):
        if not change or not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj is None:
            # this is the Add form, populate user field manually
            fields.remove('user')
        return fields

    def get_changeform_initial_data(self, request):
        return {'user': request.user}

    def mark_as_breaking_news(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one article to mark as breaking news.", level='error')
            return
        Article.objects.filter(breaking_news=True).update(breaking_news=False)
        queryset.update(breaking_news=True)
        self.message_user(request, "Selected article has been marked as breaking news.")

    mark_as_breaking_news.short_description = "Mark selected article as breaking news"

    # Optional: Add a method to display a user-friendly icon or text for breaking_news
    def breaking_news_icon(self, obj):
        return "✅" if obj.breaking_news else "❌"
    breaking_news_icon.short_description = "Pinned"
    breaking_news_icon.admin_order_field = 'breaking_news'

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'comments', 'user', 'created_at']  # Customize display fields
#     actions = ['delete_selected_comments']

#     def delete_selected_comments(self, request, queryset):
#         """Deletes the selected comments."""
#         deleted_count = queryset.delete()[0]
#         self.message_user(request, f"Successfully deleted {deleted_count} comments.", level='SUCCESS')

#     delete_selected_comments.short_description = "Delete selected comments"

admin.site.register(Category)
admin.site.register(Article, ArticlAdmin)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(ArticleTags)
admin.site.register(ArticleImages)
admin.site.register(CustomUser)
admin.site.register(Subscriber)

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)  # Show emails in the admin panel
    search_fields = ('email',)  # Enable search by email
    filter_horizontal = ('categories',)  


    

