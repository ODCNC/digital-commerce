from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class Cafe24Account(ProviderAccount):
    pass


class Cafe24Provider(OAuth2Provider):
    id = 'cafe24'
    name = 'Cafe24'
    account_class = Cafe24Account

    def extract_uid(self, data):
        return str(data['mall_id'])

    def extract_common_fields(self, data):
        return dict()

    def extract_email_addresses(self, data):
        return [EmailAddress(email=data['email'], verified=True, primary=True)]

    def get_default_scope(self):
        return ['mall.read_store']


providers.registry.register(Cafe24Provider)
