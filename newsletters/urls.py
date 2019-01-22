from django.conf.urls import url

from .views import Newsletter_signup
from .views import Newletter_unsubscribe

urlpatterns= [
    url(r'sign_up/$', Newsletter_signup, name="newsletter_signup"),
    url(r'unsubscribe/$', Newletter_unsubscribe, name="newsletter_unsubscribe"),
]
