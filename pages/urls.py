from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact', views.contact, name = 'contact'),
    path('faq', views.faq, name = 'faq'),
    path('about', views.about, name = 'about'),
    path('blog', views.blog, name = 'blog'),
    path('subscription', views.subscription, name = 'subscription'),
    path('tips', views.tips, name = 'tips'),
]