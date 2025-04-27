# newsapp/adapters.py
# newsapp/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        return HttpResponse("Custom adapter is running!")