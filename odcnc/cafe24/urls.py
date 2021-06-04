from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import Cafe24Provider

urlpatterns = default_urlpatterns(Cafe24Provider)
