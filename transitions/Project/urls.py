from django.urls import path, include
from rest_framework.routers import DefaultRouter
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from transitions.Project.Oauth2.Oauth import AuthorizedTokensListView
from transitions.Project.views.CustomerEmailViews import CustomerEmailSendemailView
from transitions.Project.views.CustomerMessageViews import CustomerMessageSendSMSView, CustomerMessageSendWhatsappView, \
    CustomerMessageSendWhatsappNoTemplateView, CustomerMessageSendSMSNoTemplateView, web_page
from transitions.Project.views.LogViews import LogView
from transitions.Project.views.TemplateViews import TemplateView
# from oauth2_provider.urls import
# from oauth2_provider.templates
import oauth2_provider.urls
router = DefaultRouter()
router.register(r'api/sendwhatsappnotemplate', CustomerMessageSendWhatsappNoTemplateView)
router.register(r'api/sendsms', CustomerMessageSendSMSView)
router.register(r'api/sendwhatsapp', CustomerMessageSendWhatsappView)
router.register(r'api/sendsmsnotemplate', CustomerMessageSendSMSNoTemplateView)
router.register(r'api/sendemail', CustomerEmailSendemailView)
urlpatterns = [
    path('', include(router.urls)),
    path('oauth/', include('oauth2_provider.urls', namespace="oauth")),
    path('api/template/', TemplateView.as_view()),
    path('api/Log/', LogView.as_view()),
    path('api/web_login/', web_page),
    path('oauth/authorize_list/', AuthorizedTokensListView.as_view(), name="token_list")

]
