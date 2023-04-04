from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blogsingle', views.blogsingle, name='blogsingle'),
    path('features', views.features, name='features'),
    path('pricing', views.pricing, name='pricing'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
]
