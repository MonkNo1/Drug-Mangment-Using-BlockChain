from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('blogsingle', views.blogsingle, name='blogsingle'),
    path('features', views.features, name='features'),
    path('pricing', views.pricing, name='pricing'),
]
