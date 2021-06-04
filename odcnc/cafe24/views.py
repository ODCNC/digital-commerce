import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import Cafe24Provider
from django.conf import settings

class Cafe24Adapter(OAuth2Adapter):
    provider_id = Cafe24Provider.id
    access_token_url = f'{settings.OAUTH_SERVER_BASEURL}/api/v2/oauth/token'
    authorize_url = f'{settings.OAUTH_SERVER_BASEURL}/api/v2/oauth/authorize'
    profile_url = f'{settings.OAUTH_SERVER_BASEURL}/api/v2/admin/store'
    basic_auth = True
    redirect_uri_protocol = 'https'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': f'Bearer {token.token}'}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json().get('store')
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def parse_token(self, data):
        token = super().parse_token(data)
        token.expires_at = data['expires_at']
        return token


oauth2_login = OAuth2LoginView.adapter_view(Cafe24Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(Cafe24Adapter)
