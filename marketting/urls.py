from django.urls import path
from . import views


urlpatterns = [
    path('settings/email/', views.MarketingPreferenceUpdateView.as_view(), name='market_pref'),
    path('webhook/mailchimp/', views.MailchimpWebhookView.as_view(), name='webhook_mailchimp'),
]
