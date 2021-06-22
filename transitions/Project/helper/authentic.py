from django.contrib.auth.models import User, Permission, Group
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.scopes import SettingsScopes
from rest_framework.authentication import BaseAuthentication
from oauth2_provider.views import AuthorizedTokensListView, AuthorizationView, TokenView
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.settings import ACCESS_TOKEN_MODEL, APPLICATION_MODEL,oauth2_settings
from transitions.Project.helper.Oauth2 import oauth
from django import forms
class IsAuth(BaseAuthentication):
    def authenticate(self, request):
        # if Object == '':
        #     return ('no user',None)
        # print(request.get_permissions())
        # tu = User.objects.all().values('id')
        # tt = Token.objects.get().values('user')
        print("check token")
        print(oauth2_settings._SCOPES)
        # print(oauth().check_token(id_user=2))

        # print(tt)
        # print(tu)
        perms = Permission.objects.get(codename='can_view_customer_message')
        # print(Permission.objects.all().values())
        users = User.objects.all().values()
        # print(users)
        # x=users.get(username='Fadhel_10')
        # print(x.email)
        print("pass")
        # print(users.get(username='Fadhel_10').data)
        # print(users)
        user, created = User.objects.get_or_create(username="Fadhel")
        print(type(user))
        # user.user_permissions.remove(perms)
        return ("Fadhel", None)
        # try:
        #     token = request.META['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        #     oauth = OauthServices()
        #     response = oauth.check_token(token)
        #
        #     if response is not None:
        #         allow_role = ['QC_ADMIN', 'QC_USER', 'C1_CUSTOMER']
        #
        #         role = response.get('authorities')
        #
        #         if len(set(allow_role).intersection(set(role))) > 0:
        #             return (len(set(allow_role).intersection(set(role))),token)
        #     return Response({"test":"test"},status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return False
