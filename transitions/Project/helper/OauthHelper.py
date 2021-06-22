import requests as requests
from requests.auth import HTTPBasicAuth
import json

from transitions.settings import OAUTH_BASE_URL
# from QC.QC_App.general.ChangeMobileNumberFormat import change_mobile_no_format


class OauthServices:
    __auth_username = '6DDrxG9cS5HWqyMOBV1wJpHjwOCThE1UGInaAYDL'
    __auth_pass = 'M1wpyQK0UjN91WZnU4uMkHo583VKDQGMlwyKk4wELdMC7tMCxcdt0VXX1bKkISvIuKL7TTijwtwXNnQ8wDLJBH01X9xeoAJs83YzvEH75w3ILl6zXbW9fwLYoqeeq712'

    # def login_oauth(self, username, password):
    #     url = 'oauth/token'

    #     body = {
    #         'grant_type': 'password',
    #         'username': username,
    #         'password': password
    #     }

    #     response = requests.post(url, data=body, auth=HTTPBasicAuth(self.__auth_username, self.__auth_pass))
    #     if response:
    #         return response.json()
    #     else:
    #         return None

    def create_user_oauth(self, body):
        url_create_user = OAUTH_BASE_URL + 'api/users/'
        token = self.get_token_oauth().get('access_token')

        headers = {
            'Authorization': 'Bearer ' + str(token),
            'Content-Type': 'Application/Json'
        }

        response = requests.post(url_create_user, json=body, headers=headers)

        return response

    def update_user_oauth(self, body, id):
        url_update_user = OAUTH_BASE_URL + 'api/users/' + id + '/'
        token = self.get_token_oauth().get('access_token')

        headers = {
            'Authorization': 'Bearer ' + str(token),
            'Content-Type': 'Application/Json'
        }

        response = requests.put(url_update_user, json=body, headers=headers)

        return response

    def get_user_by_email_and_mobile_no(self, email=' ', mobile_no=None):
        url = OAUTH_BASE_URL + 'api/users/byemailormobile' + '/' + email
        url = url if mobile_no is None else url + '/' + mobile_no

        token = self.get_token_oauth().get('access_token')

        headers = {
            'Authorization': 'Bearer ' + str(token)
        }

        response = requests.get(url, headers=headers)
        return response.json()['data'] if response.json()['data'] != None else {'detail': ''}

    def get_token_oauth(self):
        url = OAUTH_BASE_URL + 'oauth/token/'

        body = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(url, data=body, auth=HTTPBasicAuth(self.__auth_username, self.__auth_pass))

        if response:
            return response.json()
        else:
            return None

    # def refresh_token(self, token):
    #     url = OAUTH_BASE_URL + 'oauth/token'

    #     body = {
    #         'grant_type': 'refresh_token',
    #         'refresh_token': token
    #     }

    #     response = requests.post(url, data=body, auth=HTTPBasicAuth(self.__auth_username, self.__auth_pass))
    #     if response:
    #         return response.json()
    #     else:
    #         return None

    def check_token(self, token):
        url = OAUTH_BASE_URL + 'oauth/check_token/'

        body = {
            'token': token
        }

        response = requests.post(url, data=body, headers={
                                 'Authorization': 'Bearer {}'.format(self.get_token_oauth().get('access_token'))})
        if response:
            return response.json()
        else:
            return None

    def get_email_by_token(self, request):
        token = request.META['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        result = self.check_token(token)
        try:
            email = result.get('user_email')

            self.role = result.get('authorities')

            return email
        except:
            self.role = []
            return None

    def get_role(self):
        return self.role
