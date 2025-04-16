from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps  # ✅ Prevents circular import issues
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(post_save, sender="newsapp.Article")  # ✅ Correct app reference
def send_newsletter(sender, instance, created, **kwargs):
    if created:  # ✅ Only trigger on new article creation
        Subscriber = apps.get_model("newsapp", "Subscriber")  # ✅ Dynamically get model
        subscribers = Subscriber.objects.filter(categories=instance.category)

        recipient_list = [subscriber.email for subscriber in subscribers]
        if recipient_list:  # ✅ Ensure there are subscribers
            subject = f"New Article: {instance.head_line}"  # ✅ Use 'head_line'
            
            # Render the email template with dynamic content
            html_message = render_to_string("newsletter_email.html", {
                "article": instance,
                "subscriber": subscribers.first()  # Pass any subscriber for personalization
            })
            
            # Extract plain text version
            plain_message = strip_tags(html_message)  

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                html_message=html_message  # ✅ Send HTML version
            )
